@timeout @BVT @browser @ssh @db
Feature: A way to setup VA timeout
    As a Mail admin
    I want to change the the waiting time of VA analysis
    So that I could control the mail latency caused by VA analysis

@VA_timeout_default
Scenario: Default value on UI should be set in advance
    Given    i have login DDEI hidden page
    When    switch to "Timeout setting" tab
    Then    the timeout value of VA should be 20 minutes

@VA_timeout_valid
Scenario Outline: Valid values are accepted in VA timeout
    Given i have login DDEI hidden page
    and Input a value "<x>" into VA timeout setting
    When I click save
    Then User can be infoed that the saving is success
    And DDEI take the new value as timeout
    And UI shows the new value after reenter this setting page

    Examples:
    |x|
    |6|
    |2879|
    |5|
    |2880|


@VA_timeout_invalid
Scenario Outline: Invalid values are not accepted in VA timeout
    Given i have login DDEI hidden page
    and Input a value "<x>" into VA timeout setting
    When I click save
    Then User can be infoed that the saving is failed
    And DDEI still use original value
    And UI shows the original value after reenter this setting page

    Examples:
    |x |
    |-1|
    |4 |
    |2881|
    |a|
    |null|
    |!|
    |$|
    |&|

@VA_timeout_fun001
Scenario Outline: suspicious attachment should be bypassed after timeout
    Given   i have setup VA timeout as <time_value> minute
    When    i send out a suspicious mail, which will make VA timeout
    and     wait for timeout
    Then    The mail could not be detected

    Examples:
    |time_value|
    |5|


@VA_timeout_fun002
Scenario Outline: suspicious attachment should be detected before timeout
    Given   i have setup VA timeout as <time_value> minute
    When    i send out a suspicious mail, which could finish analysis before timeout
    and     wait for timeout
    Then    The mail could  be detected

    Examples:
    |time_value|
    |5|