@timeout @BVT @browser @ssh @db
Feature: A way to setup Password analyzer timeout
    As a Mail admin
    I want to change the the waiting time of password analyzer
    So that I could control the mail latency caused by password extraction

@PA_timeout_default
Scenario: Default value on UI should be set in advance
    Given    i have login DDEI hidden page
    When    switch to "Timeout setting" tab
    Then    the timeout value of Password Analyzer should be 5 minutes

@PA_timeout_valid
Scenario Outline: Valid values are accepted in password extraction timeout
    Given i have login DDEI hidden page
    and Input a value "<x>" into password extraction timeout setting
    When I click save
    Then User can be infoed that the saving is success
    And DDEI take the new value as timeout
    And UI shows the new value after reenter this setting page

    Examples:
    |x|
    |1|
    |59|
    |0|
    |60|

@PA_timeout_invalid
Scenario Outline: Invalid values are not accepted in password extraction timeout
    Given i have login DDEI hidden page
    and Input a value "<x>" into password extraction timeout setting
    When I click save
    Then User can be infoed that the saving is failed
    And DDEI still use original value
    And UI shows the original value after reenter this setting page

    Examples:
    |x |
    |-1|
    |61|
    |2.5|
    |a|
    |null|
    |!|
    |$|
    |&|

@PA_timeout_fun001
Scenario Outline: Password-protect archive cannot be scanned when the password mail comes in after timeout
    Given   i have setup password extraction timeout as <time_value> minute
    and     send out a mail with virus in password-protected archive
    When    i send the mail containing the password 15 second after the timeout
    Then    The mail could not be detected

    Examples:
    |time_value|
    |1|
    |0|

@PA_timeout_fun002
Scenario Outline: Password-protect archive can be scanned when the password mail comes in before timeout
    Given   i have setup password extraction timeout as <time_value> minute
    and     send out a mail with virus in password-protected archive
    When    i send the mail containing the password 15 second before timeout
    Then    The mail could be detected

    Examples:
    |time_value|
    |1|
