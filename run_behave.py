import os
import sys
import shutil
import subprocess

# ---------------- Config ----------------
PROJECT_DIR = os.getcwd()
REPORT_DIR = os.path.join(PROJECT_DIR, "reports")
ALLURE_RESULTS = os.path.join(REPORT_DIR, "allure-results")
ALLURE_REPORT = os.path.join(REPORT_DIR, "allure-report")
ALLURE_CLI = os.path.join(PROJECT_DIR, r"allure-2.36.0\bin\allure.bat")  # Adjust if needed

# ---------------- Default args ----------------
tags = None
browser = "chrome"
feature_path = None
env = "qa"
browserstack="false"

# ---------------- Parse command line args ----------------
for arg in sys.argv[1:]:
    if arg.startswith("--tags="):
        tags = arg.split("=", 1)[1]
    elif arg.startswith("browser="):
        browser = arg.split("=", 1)[1]
        if browser.lower()=="browserstack":
            browserstack="true"

    elif arg.startswith("env="):
        env = arg.split("=", 1)[1]
    elif arg.startswith("--jobs="):
        parallel_jobs = int(arg.split("=", 1)[1])
    elif arg.endswith(".feature") or os.path.isdir(arg):
        feature_path = arg

print(f"Running tests with browser: {browser}, tags: {tags}, feature_path: {feature_path or 'all features'}")

# ---------------- Ensure results folder ----------------
if os.path.exists(ALLURE_RESULTS):
    shutil.rmtree(ALLURE_RESULTS, ignore_errors=True)
os.makedirs(ALLURE_RESULTS, exist_ok=True)

# ---------------- Build Behave Parallel command ----------------
behave_cmd = [
    "behave",
    "-f", "allure_behave.formatter:AllureFormatter",
    "-o", ALLURE_RESULTS,

]

if feature_path:
    behave_cmd.append(feature_path)

if tags:
    behave_cmd.append(f"--tags={tags}")

if browser:
    behave_cmd.append(f"-D browser={browser}")

if env:
    behave_cmd.append(f"-D env={env}")
if browserstack:
    behave_cmd.append(f"-D browserstack={browserstack}")

# ---------------- Run Behave ----------------
try:
    subprocess.run(behave_cmd, check=True)
except subprocess.CalledProcessError as e:
    print(f"Behave execution failed with exit code {e.returncode}")
    # Continue anyway to generate Allure report

# ---------------- Generate Allure report ----------------
try:
    subprocess.run([
        ALLURE_CLI,
        "generate", ALLURE_RESULTS,
        "-o", ALLURE_REPORT,
        "--clean"
    ], check=True)
    print(f"Allure report generated at: {ALLURE_REPORT}")
    print(f"To open the report: {ALLURE_CLI} open {ALLURE_REPORT}")
except subprocess.CalledProcessError as e:
    print(f"Failed to generate Allure report: {e}")
