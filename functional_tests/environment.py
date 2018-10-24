from os import path
import logging
from datetime import datetime
from selenium.common.exceptions import WebDriverException

from functional_tests.lib.test_setup import \
    start_and_configure_new_browser_as_per_run_mode
from functional_tests.lib.test_teardown import TearDown
from functional_tests.lib.util \
     import clean_screenshot_filename
from functional_tests.lib.utils_file_system import\
     check_dir_exists_create_if_not, delete_all_files_within_directory

FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(format=FORMAT)

ENV_URLS = {
    "localhost": "http://localhost:3000",
    "uat": "https://www.uat.whoever.com/"
}


def before_all(context):

    context.data = {}

    # read in the Behave Userdata
    # Note that any '-D' command line args will override userdata in the
    # behave.ini file
    # http://pythonhosted.org//behave/new_and_noteworthy_v1.2.5.html#index-7

    userdata = context.config.userdata

    env = userdata.get('env')
    context.base_url = ENV_URLS[env]
    context.user_data = {}

    context.fail_image_folder =\
        userdata.get('fail_image_folder')

    # use the default browser/mode from behave.ini unless passed in at cmd line
    context.browser_name = userdata.get('browser').lower()
    context.run_mode = userdata['mode']

    # create (if needs be) and clear our required output directories
    output_folders = [context.fail_image_folder]

    for folder in output_folders:
        check_dir_exists_create_if_not(folder)
        delete_all_files_within_directory(folder)


def before_scenario(context, scenario):

    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    logging.info("*** before_scenario *** %s : %s", now, scenario)

    logging.info("Current Behave Scenario is tagged with: %s",
                 str(scenario.tags))

    context.rollback_system = TearDown()

    if 'non-browser' in scenario.tags:
        context.browser = False
        logging.info("non-browser scenario, not starting browser")
    else:
        context.browser =\
            start_and_configure_new_browser_as_per_run_mode(context)


def after_scenario(context, scenario):

    logging.info("*** after_scenario *** result was: %s", scenario.status)

    if context.browser:
        logging.info("after_scenario, our webdriver session ID is : %s",
                     str(context.browser.session_id))

    if scenario.status == "failed":
        logging.info("Scenario FAILED: %s", context.scenario.name)

        save_location = context.fail_image_folder
        check_dir_exists_create_if_not(context.fail_image_folder)

        scenario_name = context.scenario.name
        clean_filename = clean_screenshot_filename(scenario_name)

        clean_filename = clean_filename + ".png"

        # Save screenshots
        logging.info("about to try to capture screenshot as: %s, %s",
                     save_location, str(clean_filename))

        full_path_to_screenshot = \
            path.join(save_location, clean_filename)
        logging.debug("Full save path is: %s", full_path_to_screenshot)

        if context.browser:
            try:
                context.browser.save_screenshot(full_path_to_screenshot)
            except WebDriverException as e:
                logging.warning(
                    "Exception attempting to save screenshot: %s", str(e))
                logging.warning("Saving our screenshot FAILED")
                raise RuntimeError

            logging.info("Saved our screenshot - OK")

    context.rollback_system.teardown()

    if context.browser:

        # close the browser window inbetween each scenario
        try:
            context.browser.quit()
        except WebDriverException as e:  # TimeoutException != grid TIMEOUT
            # just log this, don't fail - can happen due to inactive session
            logging.info("WebDriverException while trying to close driver")
            logging.debug(e)

    # visual marker to seperate scenarios easily in log
    logging.info("-------------------------------------------------------\n")


def after_all(context):

    now = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    logging.info("%s : Time at End of all Behave steps", now)
