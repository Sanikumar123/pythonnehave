from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver, logger):
        self.driver = driver
        self.logger = logger
        self.wait = WebDriverWait(driver, 10)

    def click(self, locator):
        self.logger.info(f"Clicking on: {locator}")
        # Will raise exception naturally if element not found
        self.wait.until(EC.visibility_of_element_located(locator)).click()

    def type(self, locator, value):
        self.logger.info(f"Typing '{value}' into: {locator}")
        self.wait.until(EC.visibility_of_element_located(locator)).send_keys(value)

    def get_text(self, locator):
        self.logger.info(f"Getting text from: {locator}")
        return self.wait.until(EC.visibility_of_element_located(locator)).text
