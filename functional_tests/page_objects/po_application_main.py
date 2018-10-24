import logging

from functional_tests.page_objects.po_browser_driver\
    import Page
from functional_tests.lib import util

"""
Page objects for application pages
"""


class WeatherStart(Page):

    # Application page title shown on UI
    page_title = '5 Weather Forecast'

    def start(self):
        self.url = ""
        self.open(self.url)

        check_title = self.driver.title
        assert check_title == self.page_title,\
            'Weather application Home page has failed to load'


class WeatherHome(Page):
    # Application page title shown on UI
    page_title = '5 Weather Forecast'

    # IDs of page objects
    city_name_search = "city"

    # selectors based on Class names
    day_class = 'name'

    """
    Each of the prefixes below are the first part of identifiers of elements.
    We substitute out the 'xx' and 'yy'
    in relevant functions e.g. for the day and hour sequence numbers
    """
    # e.g. hour-1-1, hour-1-2, hour-2-3
    hour_summary_prefix = 'hour[data-test="hour-xx-yy"]'

    hour_summary_max_temp_prefix = 'max[data-test="maximum-xx-yy'

    def enter_search_criteria(self, city_name):

        self.set_text_by_id(self.city_name_search, city_name)
        self.press_enter_key()
        logging.info('entered %s in city field' % city_name)

    def check_city_value(self):
        # TODO
        pass

    def return_summary_elements(self):
        all_summaries = self.get_elements_by_class('summary')
        return all_summaries

    def return_details_elements(self):
        all_summaries = self.get_elements_by_class('details')
        return all_summaries

    def click_specified_day(self, day):

        names = self.get_elements_by_class(self.day_class)
        day_index = int(day[:1])-1
        logging.info(day_index)

        our_element = names[day_index]
        this_name = our_element.get_attribute('data-test')
        logging.info('clicking %s for day %s ' % (this_name, day))

        old_page = self.driver.find_element_by_tag_name('html')
        our_element.click()
        self.wait_for_page_load(old_page, timeout=1)

    def check_details_visible(self, day, expected_vis=True):

        # define the element we want to check visibility of ie. day - detail
        this_detail = self.hour_summary_prefix
        this_detail = this_detail.replace('xx', day[:1])
        # we'll just check the first one is visible under each day
        this_detail = this_detail.replace('yy', '1')
        logging.info(this_detail)
        visible_element = self.check_element_visible_by_class(this_detail)

        if visible_element:
            visible = True
        else:
            visible = False
        logging.info('visibility is %s' % visible)

        assert visible == expected_vis

    def get_hourly_maximum_temps(self, day):

        all_values = []
        hour_count = 1

        while hour_count:
            hour_max = self.hour_summary_max_temp_prefix
            hour_max = hour_max.replace('xx', day[:1])
            hour_max = hour_max.replace('yy', str(hour_count))
            logging.debug(hour_max)
            visible_element = self.check_element_visible_by_class(hour_max)

            if visible_element:
                clean_value =\
                    util.clean_text_string_return_ascii(visible_element.text)
                all_values.append(int(clean_value))
                hour_count += 1
            else:
                return all_values

    def get_daily_maximum_temp(self, day):

        day_max = self.hour_summary_max_temp_prefix
        day_max = day_max.replace('xx', day[:1])
        day_max = day_max.replace('-yy', '')

        visible_element = self.check_element_visible_by_class(day_max)

        return visible_element.text
