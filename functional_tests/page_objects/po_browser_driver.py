import logging

from selenium.common.exceptions import WebDriverException, \
    TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import \
    staleness_of
from selenium.webdriver.support.ui import WebDriverWait

from functional_tests.lib.util import log_time_before_and_after


class Page(object):
    "Page class that all page models can inherit from"

    def __init__(self, selenium_driver, base_url=False):
        "Constructor"
        self.base_url = base_url
        self.driver = selenium_driver

        # Initialise specific page
        self.start()

    def start(self):
        # we can override this for specific pages
        pass

    def get_elements_by_class(self, our_class):
        try:
            our_elements = self.driver.find_elements(By.CLASS_NAME, our_class)
        except WebDriverException as e:
            logging.error("Exception trying to identify element with id: %s",
                          our_class)
            raise
        return our_elements

    def wait_for_page_element_to_be_refreshed(
            self, element, selector_id, max_secs=5):
        # check for a WebElement to change in the DOM
        # note that selector_id is only for log readability

        try:
            WebDriverWait(self.driver, max_secs).until(
                EC.staleness_of(element))
        except TimeoutException:
            logging.info('%s is not refreshed' % selector_id)
            return False
        return True

    def check_element_visible_by_class(self, class_name):
        try:
            element = WebDriverWait(self.driver, 2).until(
                EC.visibility_of_element_located((
                    By.CLASS_NAME, class_name)))
        except TimeoutException:
            return False

        return element

    def find_and_print_all_page_ids(self, part_of_tag=False):
        """
        Utility funtion to help map page elements quickly - not used in
        the acutal test code!!
        :return:
        """
        ids = self.driver.find_elements_by_xpath('//*[@id]')
        for ii in ids:
            if part_of_tag:
                if part_of_tag in ii.get_attribute('id'):
                    logging.info("tag: %s , id: %s",
                                 ii.tag_name, ii.get_attribute('id'))
            else:
                logging.info("tag: %s , id: %s",
                             ii.tag_name, ii.get_attribute('id'))

    def get_all_data_test_elements_to_dict(self):
        """
        :return: dict of all data-test items , text value
        """

        elem_dict = {}

        for elem in self.driver.find_elements(By.XPATH, './/span[@data-test]'):

            # if there is data then add it to our dict
            if elem.text:
                # logging.info(elem.text)
                dict_key = elem.get_attribute("data-test")
                elem_dict[dict_key] = elem.text

        return elem_dict

    def open(self, url):
        "Visit the page base_url + url"
        url = self.base_url + url
        self.driver.get(url)

    def click_element_by_id(self, element_id):
        "Click the element supplied"
        link = self.get_element_by_id(element_id)
        if link is not None:
            try:
                link.click()
            except Exception as e:
                logging.warning('Exception when clicking link with id: %s',
                                element_id)
                logging.warning(e)
            else:
                return True

        return False

    def get_element_by_id(self, our_id):
        try:
            our_element = self.driver.find_element(By.ID, our_id)
        except WebDriverException as e:
            logging.error("Exception trying to identify element with id: %s",
                          our_id)
            raise
        return our_element

    # @log_time_before_and_after
    def safe_get_element_by_id(self, our_id, timeout=1):

        try:
            our_element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.ID, our_id))
            )

        except TimeoutException as (e):
            logging.debug("TimeoutException trying to identify element"
                          " with id: %s", our_id)
            logging.info('didnt find %s', our_id)
            our_element = False

        return our_element

    def get_visible_element_by_id(self, element_id, timeout=10):

        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((By.ID, element_id))
        )
        return element

    def set_text_by_id(self, id, value, clear_first=True):
        "Set the value of the text field, by default clearing it first"
        text_field = self.get_element_by_id(id)

        if clear_first:
            try:
                text_field.clear()
            except Exception as e:
                logging.warning('Could not clear the text field: %s', id)
                logging.warning(str(e))

        if value is not None:
            text_field.send_keys(value)

    def get_field_value_by_id(self, field_id):
        field = self.get_element_by_id(field_id)
        try:
            value = field.get_attribute('value')
        except WebDriverException as e:
            raise

        return value

    @log_time_before_and_after
    def wait_for_page_load(self, old_page_html, timeout=30):
        """
        Checks for staleness of the html element (i.e. the current page) -
        treating this event as indication that a new page has loaded.

        example usage:
        start_page = driver.find_element_by_tag_name('html')
        success = wait_for_page_load(driver, start_page, timeout=10)
        if not success:
            ...

        :return: False if not stale within timeout, or True.
        """
        try:
            WebDriverWait(self.driver, timeout).until(
                staleness_of(old_page_html))
        except (TimeoutException, WebDriverException) as e:
            logging.debug("a new page has not loaded when it was expected..")
            return False

        return True

    def press_enter_key(self):
        actions = ActionChains(self.driver)
        actions.send_keys(Keys.ENTER)
        actions.perform()
