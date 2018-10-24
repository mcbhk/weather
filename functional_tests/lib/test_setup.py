import sys
import logging
import json

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def start_and_configure_new_browser_as_per_run_mode(context):

    if context.run_mode == 'grid':
        our_driver = get_grid_browser_driver_by_name(context,
                                                     context.browser_name)
    else:
        our_driver = get_browser_driver_by_name(context.browser_name)

    our_driver.set_window_size(1920, 1080)  # Set to known dimensions

    return our_driver


def get_grid_browser_driver_by_name(context, name):
    """
    Return the grid driver for the passed browser name

    :name: Name of the browser
    """
    logging.info("Starting %s browser- grid mode.. " % name)

    # default grid url (in behave.ini), can be overridden using -Dgrid=
    # e.g. -Dgrid=http://localhost:4444/wd/hub
    grid_url = context.config.userdata['grid']

    logging.info("Grid URL being used is %s" % grid_url)

    if name == 'chrome':
        capability = DesiredCapabilities.CHROME

    elif name == 'firefox':
        capability = DesiredCapabilities.FIREFOX

    elif name == 'ie':
        capability = DesiredCapabilities.INTERNETEXPLORER
    else:
        raise RuntimeError("Browser name not found by: %s" % name)

    # Add ability to keep Browser's Console logging
    capability['loggingPrefs'] = {'browser': 'ALL'}

    # default grid url
    if 'grid' in context.config.userdata:
        grid_url = context.config.userdata['grid']

    driver = webdriver.Remote(grid_url, capability)
    logging.info("driver.capabilities are: %s", str(driver.capabilities))
    return driver


def get_browser_driver_by_name(name):
    """
    Return the driver for the passed browser name

    :name: Name of the browser
    """
    if name == 'chrome':
        args = {}
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("disable-gpu")
        args['chrome_options'] = chrome_options
        driver = webdriver.Chrome(**args)

    elif name == 'firefox':
        capability = DesiredCapabilities.FIREFOX
        capability['loggingPrefs'] = {'browser': 'ALL'}
        driver = webdriver.Firefox(capabilities=capability)

    elif name == 'ie':
        capability = DesiredCapabilities.INTERNETEXPLORER
        driver = webdriver.Ie(capabilities=capability)

    else:
        raise RuntimeError("Browser name not found by: %s" % name)

    logging.info("driver.capabilities are: %s", str(driver.capabilities))
    return driver
