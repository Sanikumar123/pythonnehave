import os
import platform
import shutil
from datetime import datetime
import allure
from allure_commons.types import AttachmentType

from config.env_config import ENV_CONFIG
from utils.driver_factory import get_driver
from utils.logger import setup_logger

TIMESTAMP = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

Root_dir = os.getcwd()
Report_dir = os.path.join(Root_dir, "reports")
Allure_Results = os.path.join(Report_dir, "allure-results")
Allure_Reports = os.path.join(Report_dir, "allure-report")


# ------------------ before_all ------------------
def before_all(context):
    # Clean old folders
    shutil.rmtree(Allure_Results, ignore_errors=True)
    shutil.rmtree(Allure_Reports, ignore_errors=True)
    os.makedirs(Allure_Results, exist_ok=True)
    os.makedirs(Allure_Reports, exist_ok=True)

    # Environment config
    env_value = context.config.userdata.get("env", "qa")
    env_data = ENV_CONFIG.get(env_value)
    if not env_data:
        valid_envs = ", ".join(ENV_CONFIG.keys())
        raise ValueError(f"Invalid environment '{env_value}'. Valid options: {valid_envs}")

    context.url = env_data.get("url")
    context.username = env_data.get("username")
    context.password = env_data.get("password")

    # Browser
    context.browser = context.config.userdata.get("browser", "chrome").lower()

    # BrowserStack
    context.use_bs = context.config.userdata.get("browserstack", "false").lower() == "true"

    # Browser version
    context.b_version = context.config.userdata.get("browser_version", "latest")

    # OS / device settings
    context.o_name = context.config.userdata.get("os_name")
    context.o_version = context.config.userdata.get("os_version")
    context.device_name = context.config.userdata.get("device_name")
    context.platform_name = context.config.userdata.get("platform_name")

    # Safari defaults for BrowserStack desktop
    if context.use_bs and context.browser == "safari" and not context.device_name:
        if not context.o_name:
            context.o_name = "OS X"
        if not context.o_version:
            context.o_version = "Monterey"
        if not context.b_version:
            context.b_version = "16.1"

    # Default desktop OS if not provided
    if not context.o_name and not context.device_name:
        context.o_name = "Windows"
    if not context.o_version and not context.device_name:
        context.o_version = "11"

    # Logger
    context.logger = setup_logger()
    context.logger.info("Starting test execution")
    context.logger.info(
        f"Environment: {env_value}, "
        f"Browser: {context.browser}, "
        f"BrowserStack: {context.use_bs}, "
        f"OS/Device: {context.o_name or context.device_name} {context.o_version or context.platform_name}, "
        f"Browser Version: {context.b_version}"
    )

    # Write environment.properties for Allure
    with open(os.path.join(Allure_Results, "environment.properties"), "w") as f:
        f.write(f"Environment={env_value}\n")
        f.write(f"Browser={context.browser}\n")
        f.write(f"OS/Device={platform.system()} {platform.release()}\n")
        f.write(f"Python={platform.python_version()}\n")
        f.write(f"ExecutionTime={TIMESTAMP}\n")


# ------------------ before_scenario ------------------
def before_scenario(context, scenario):
    context.driver = get_driver(
        browser=context.browser,
        use_browserstack=context.use_bs,
        scenario_name=scenario.name,
        browser_version=context.b_version,
        os_name=context.o_name,
        os_version=context.o_version,
        device_name=context.device_name,
        platform_name=context.platform_name
    )
    context.driver.get(context.url)


# ------------------ after_step ------------------
def after_step(context, step):
    try:
        # Attach screenshot for every step
        if hasattr(context, "driver") and context.driver:
            allure.attach(
                context.driver.get_screenshot_as_png(),
                name=f"{step.name} - {step.status}",
                attachment_type=AttachmentType.PNG
            )
    except Exception as e:
        context.logger.warning(f"Failed to attach screenshot: {e}")

    # Log step result
    if step.status == "passed":
        context.logger.info(f"STEP PASSED | {step.keyword} {step.name}")
    elif step.status == "failed":
        context.logger.error(f"STEP FAILED | {step.keyword} {step.name}")


# ------------------ after_scenario ------------------
def after_scenario(context, scenario):
    if hasattr(context, "driver"):
        try:
            if context.use_bs:
                status = "passed" if scenario.status == "passed" else "failed"
                reason = "Scenario Passed" if scenario.status == "passed" else "Scenario Failed"
                context.driver.execute_script(
                    f'browserstack_executor: {{"action": "setSessionStatus", "arguments": {{"status":"{status}","reason": "{reason}"}}}}'
                )
        finally:
            context.driver.quit()


# ------------------ after_all ------------------
def after_all(context):
    context.logger.info("Test execution finished")