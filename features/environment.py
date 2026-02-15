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
    context.browser = context.config.userdata.get("browser", "chrome")

    #browserstack
    context.use_bs= context.config.userdata.get("browserstack","false")=="true"


    # Logger
    context.logger = setup_logger()
    context.logger.info("Starting test execution")
    context.logger.info(f"Environment: {env_value}, Browser: {context.browser}")

    # Write environment.properties for Allure
    with open(os.path.join(Allure_Results, "environment.properties"), "w") as f:
        f.write(f"Environment={env_value}\n")
        f.write(f"Browser={context.browser}\n")
        f.write(f"OS={platform.system()} {platform.release()}\n")
        f.write(f"Python={platform.python_version()}\n")
        f.write(f"ExecutionTime={TIMESTAMP}\n")

# ------------------ before_scenario ------------------
def before_scenario(context, scenario):
    context.driver = get_driver(context.browser,use_browserstack=context.use_bs)
    context.driver.get(context.url)

# ------------------ after_step ------------------
def after_step(context, step):
    try:
        # Attach screenshot for EVERY step
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
    if hasattr(context, "driver") and context.driver:
        context.driver.quit()

# ------------------ after_all ------------------
def after_all(context):
    context.logger.info("Test execution finished")
