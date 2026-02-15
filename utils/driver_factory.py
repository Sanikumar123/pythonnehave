from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from config.env_config import ENV_CONFIG


def get_driver(browser="chrome", use_browserstack=False, scenario_name="Behave Test"):
    # 🔵 BrowserStack execution
    if use_browserstack:
        bs_config = ENV_CONFIG["browserstack"]

        # Use options instead of desired_capabilities
        if bs_config["browser"].lower() == "chrome":
            options = webdriver.ChromeOptions()
        elif bs_config["browser"].lower() == "firefox":
            options = webdriver.FirefoxOptions()
        elif bs_config["browser"].lower() == "edge":
            options = webdriver.EdgeOptions()
        else:
            raise ValueError(f"Browser '{bs_config['browser']}' is not supported on BrowserStack.")

        # Set capabilities for BrowserStack
        options.set_capability("browserName", bs_config["browser"])
        options.set_capability("browserVersion", bs_config["browser_version"])
        options.set_capability("bstack:options", {
            "os": bs_config["os"],
            "osVersion": bs_config["os_version"],
            "resolution": "1920x1080",
            "userName": bs_config["username"],
            "accessKey": bs_config["access_key"],
            "sessionName": scenario_name
        })

        driver = webdriver.Remote(
            command_executor="https://hub.browserstack.com/wd/hub",
            options=options
        )

        return driver

    # 🟢 Local execution
    if browser.lower() == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )

    elif browser.lower() == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )

    elif browser.lower() == "edge":
        options = webdriver.EdgeOptions()
        options.use_chromium = True  # Ensure Edge runs in Chromium mode
        options.add_argument("--start-maximized")
        # Use cached driver if exists, otherwise WebDriver Manager downloads
        driver_path = EdgeChromiumDriverManager().install()
        driver = webdriver.Edge(
            service=EdgeService(driver_path),
            options=options
        )


    else:
        raise ValueError(f"Browser '{browser}' is not supported. Use 'chrome', 'firefox', or 'edge'.")

    driver.implicitly_wait(10)
    return driver
