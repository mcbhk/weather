@browser
Feature: Daily forecast should summarise the hourly data

  Background: set up for every scenario such that the scenarios start from same point
    Given the weather forecast application is running
    And I search for the city Glasgow

  Scenario Outline: Minimum and maximum temperatures correctly summarised
  Given I select the <day> day
  And a three hourly forecast is shown for that <day> day
  When I check the maximum temperature in each of the hourly data points for day <day>
  Then the maximum shown in the daily summary for day <day> is the average of the maximum for all hours shown
  Examples:
    |day|
    | 1 |
    | 2 |
    | 4 |

  @wip # TODO: what does 'most dominant or current' mean? Surely it must be one or the other?
  Scenario: Most dominant (or current) condition in hourly data is shown as the summary data for the day
    Given I select the 1st day
    And a three hourly forecast is shown for that 1st day
    When I check the most dominant condition in each of the hourly data points
    Then this dominant condition is correctly shown in the daily summary view

  @wip
  Scenario: Most dominant (or current) wind speed and direction correctly summarised for day

  @wip
  Scenario: Aggregate rainfall correctly summarised