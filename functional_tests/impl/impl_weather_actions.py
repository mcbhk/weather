import logging

from functional_tests.page_objects.pagefactory import get_page_object


def impl_start_app(context):

    # Create a page object and start the app
    weather_form = get_page_object("weather_start",
                                   context.browser, context.base_url)
    return weather_form


def impl_city_search(context, city):

    form_object = get_page_object('weather_home', context.browser)
    form_object.enter_search_criteria(city)


def check_five_days_listed(context):
    form_object = get_page_object('weather_home', context.browser)
    all_summaries = form_object.return_summary_elements()
    count_shown = len(all_summaries)
    assert count_shown == 5,\
        'We did not find summary data for 5 days - got %i' % count_shown


def get_ui_data_test_data(context):
    form_object = get_page_object('weather_home', context.browser)
    ui_data_dict = form_object.get_all_data_test_elements_to_dict()
    logging.info(ui_data_dict)
    return ui_data_dict
