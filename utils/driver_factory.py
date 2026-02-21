from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import platform

from config.env_config import ENV_CONFIG


def get_driver(browser="chrome",
               use_browserstack=False,
               scenario_name="Behave Test",
               browser_version=None,
               os_name=None,
               os_version=None,
               device_name=None,
               platform_name=None):
    """
    Returns a Selenium WebDriver instance.
    Supports:
        - Desktop: chrome, firefox, edge, safari (local + BrowserStack)
        - Mobile: BrowserStack real iOS/Android devices
    """

    browser_clean = browser.lower()

    # ----------------- BrowserStack Execution -----------------
    if use_browserstack:
        bs_config = ENV_CONFIG.get("browserstack")
        if not bs_config:
            raise ValueError("BrowserStack configuration missing in ENV_CONFIG")

        # Mobile device
        if device_name:
            options = webdriver.ChromeOptions()  # Options are mostly ignored on mobile
            bstack_options = {
                "userName": bs_config["username"],
                "accessKey": bs_config["access_key"],
                "deviceName": device_name,
                "realMobile": True,
                "sessionName": scenario_name
            }
            if platform_name:
                options.set_capability("platformName", platform_name)
            if os_version:
                bstack_options["osVersion"] = os_version
            options.set_capability("bstack:options", bstack_options)

        # Desktop browser
        else:
            if browser_clean == "chrome":
                options = webdriver.ChromeOptions()
            elif browser_clean == "firefox":
                options = webdriver.FirefoxOptions()
            elif browser_clean == "edge":
                options = webdriver.EdgeOptions()
            elif browser_clean == "safari":
                options = webdriver.SafariOptions()
            else:
                raise ValueError(f"Browser '{browser}' is not supported on BrowserStack.")

            options.set_capability(
                "browserName", "Safari" if browser_clean == "safari" else browser_clean
            )
            if browser_version:
                options.set_capability("browserVersion", browser_version)

            bstack_options = {
                "userName": bs_config["username"],
                "accessKey": bs_config["access_key"],
                "sessionName": scenario_name,
                "resolution": "1920x1080"
            }
            if os_name:
                bstack_options["os"] = os_name
            if os_version:
                bstack_options["osVersion"] = os_version
            options.set_capability("bstack:options", bstack_options)

        # Print capabilities for debugging
        print("=== BrowserStack Capabilities ===")
        print(options.capabilities)
        print("===============================")

        driver = webdriver.Remote(
            command_executor="https://hub.browserstack.com/wd/hub",
            options=options
        )

        # Adjust window size for Safari desktop
        if browser_clean == "safari" and not device_name:
            driver.set_window_size(1440, 900)
        elif not device_name:
            driver.maximize_window()

        return driver

    # ----------------- Local Execution -----------------
    if device_name:
        raise EnvironmentError("Local execution on mobile devices is not supported. Use BrowserStack.")

    if browser_clean == "safari" and platform.system() != "Darwin":
        raise EnvironmentError("Safari local execution requires macOS")

    if browser_clean == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=options
        )

    elif browser_clean == "firefox":
        options = webdriver.FirefoxOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Firefox(
            service=FirefoxService(GeckoDriverManager().install()),
            options=options
        )

    elif browser_clean == "edge":
        options = webdriver.EdgeOptions()
        options.use_chromium = True
        options.add_argument("--start-maximized")
        driver = webdriver.Edge(
            service=EdgeService(EdgeChromiumDriverManager().install()),
            options=options
        )

    elif browser_clean == "safari":
        options = webdriver.SafariOptions()
        driver = webdriver.Safari(options=options)
        driver.set_window_size(1440, 900)

    else:
        raise ValueError(
            f"Browser '{browser}' is not supported. Use 'chrome', 'firefox', 'edge', or 'safari'."
        )

    driver.implicitly_wait(10)
    return driver