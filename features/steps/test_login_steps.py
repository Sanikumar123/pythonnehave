import time

from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.common.by import By

from pages.Loginpage import LoginPage


@given('user on OpenCard login page')
def login_page(context):
    #context.driver = webdriver.Chrome()
    #context.driver.maximize_window()
    #context.driver.get("https://www.demoblaze.com/index.html")
    #time.sleep(3)
    pass

@when('user enters username, password')
def username_password(context):

    context.login_page = LoginPage(context.driver,context.logger)
    context.login_page.login(context.username,context.password)
    time.sleep(3)




@when('clicks on Login button')
def login_btn(context):

    pass



@then('user should be able to login successfully')
def login_successful(context):
    actual = context.login_page.validate_welcome_text()
    assert actual=="Welcome seleniumtutorial4@gmail.com"


@when('user enters "{username}" and "{password}"')
def username_password_param(context,username,password):
    context.login_page = LoginPage(context.driver,context.logger)
    context.login_page.login("seleniumtutorial4@gmail.com", "Dexter@456")
    time.sleep(3)
