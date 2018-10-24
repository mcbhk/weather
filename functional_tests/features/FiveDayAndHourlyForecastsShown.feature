@browser
Feature: Enter city name, get 5 day weather forecast and can show/hide hourly forecasts

  Background: set up for every scenario such that the scenarios start from same point
    Given the weather forecast application is running

  Scenario Outline: Cities return 5 day forecast
    When I search for the city <city>
    Then a five day forecast is shown for that city
    Examples:
    | city |
    | Edinburgh |
    | Aberdeen  |

  Scenario Outline: Select day, get 3 hourly forecast, select again and hide the 3 hourly forecast
    And I search for the city Dundee

    When I select the <which_day> day
    Then a three hourly forecast is shown for that <which_day> day

    When I select the <which_day> day again
    Then a three hourly forecast is not shown for that <which_day> day

    Examples:
    |which_day|
    |1st      |
    |3rd      |
    |5th      |

