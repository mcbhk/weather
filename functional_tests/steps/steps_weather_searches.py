import logging
from behave import *


from functional_tests.impl import impl_weather_actions as act
from functional_tests.page_objects.pagefactory import\
    get_page_object
from functional_tests.lib import util


@given("the weather forecast application is running")
def step_impl(context):
    act.impl_start_app(context)


@step("I search for the city {city}")
def step_impl(context, city):
    act.impl_city_search(context, city)


@step("a five day forecast is shown for that city")
def step_impl(context):
    act.check_five_days_listed(context)


@step("I select the {which_day} day")
@step("I select the {which_day} day again")
def step_impl(context, which_day):

    form_object = get_page_object('weather_home', context.browser)
    form_object.click_specified_day(which_day)


@step("a three hourly forecast is {expect_shown} for that {which_day} day")
def step_impl(context, expect_shown, which_day):

    form_object = get_page_object('weather_home', context.browser)

    if 'not' in expect_shown:
        expect_shown = False
    else:
        expect_shown = True

    form_object.check_details_visible(
        which_day, expected_vis=expect_shown)


@step('I check the maximum temperature in each of the hourly'
      ' data points for day {day}')
def step_impl(context, day):

    form_object = get_page_object('weather_home', context.browser)
    summary_max_temps = form_object.get_hourly_maximum_temps(day)
    logging.info('Hourly max temps shown for day %s are %s'
                 % (day, summary_max_temps))

    total_max = sum(summary_max_temps)

    average = total_max/len(summary_max_temps)
    # add the average to the context so we can use it again
    context.summary_max = average


@step('the maximum shown in the daily summary for day {day} is'
      ' the average of the maximum for all hours shown')
def step_impl(context, day):
    form_object = get_page_object('weather_home', context.browser)
    max_temp = form_object.get_daily_maximum_temp(day)

    # tidy up the text - remove the degrees symbol
    max_temp = util.clean_text_string_return_ascii(max_temp)
    logging.info(max_temp)

    assert max_temp == context.summary_max,\
        'Summary max temp for day %s is not as expected - the average' \
        ' hourly temp is %s , but summary shows: %s' \
        % (day, context.summary_max, max_temp)
