import time

from selenium.webdriver.common.by import By

from pages.basepage import BasePage
from utils.action_logger import log_action


class LoginPage(BasePage):

    homepage_login_btn = (By.XPATH,"//a[@id='login2']")
    username=(By.XPATH,"//input[@id='loginusername']")
    password=(By.XPATH,"//input[@id='loginpassword']")
    login_btn=(By.XPATH,"//button[normalize-space()='Log in']")
    username_validation=(By.XPATH,"//a[@id='nameofuser']")

    @log_action
    def login(self,user,pwd):
        self.click(self.homepage_login_btn)
        time.sleep(2)
        self.type(self.username,user)
        self.type(self.password,pwd)
        self.click(self.login_btn)
        self.logger.info("Login button clicked")

    @log_action
    def validate_welcome_text(self):
        return self.get_text(self.username_validation)

