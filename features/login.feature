Feature: OpenCart Login page

  Background:
    Given user on OpenCard login page

  @login
  Scenario: User login functionality

    When user enters username, password
    And clicks on Login button
    Then user should be able to login successfully

  @login_param
  Scenario: User login functionality with parameter

    When user enters "seleniumtutorial4@gmail.com" and "Dexter@456"
    And clicks on Login button
    Then user should be able to login successfully

  @login_outline
  Scenario Outline: User login functionality with outline

    When user enters "<username>" and "<password>"
    And clicks on Login button
    Then user should be able to login successfully
    Examples:
      |username|password|
      |seleniumtutorial4@gmail.com|Dexter@456|
