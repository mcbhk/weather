import logging

from functional_tests.page_objects.po_application_main\
    import WeatherStart, WeatherHome


_configured_pages = {
    "weather_start":
        lambda driver, base_url: WeatherStart(driver, base_url=base_url),
    "weather_home":
        lambda driver, _: WeatherHome(driver)
}


def get_page_object(page_name, driver, base_url=False):

    page_name = page_name.lower()
    page_name = page_name.replace(' ', '_')

    logging.debug("About to look up page object: %s", page_name)

    test_obj = _configured_pages.get(page_name)

    if not test_obj:
        raise Exception("No page object configured for %s" % page_name)

    return test_obj(driver, base_url)
