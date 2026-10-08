import os
import html
import json
import platform
from datetime import datetime, timezone
from urllib.parse import quote
from pathlib import Path
import pytest
import allure
from selenium.common.exceptions import WebDriverException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

@pytest.fixture
def driver(request):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--window-size=1440,1000')
    options.add_argument('--disable-dev-shm-usage')
    if os.getenv('CHROME_BINARY'):
        options.binary_location = os.environ['CHROME_BINARY']
    remote = os.getenv('SELENIUM_REMOTE_URL')
    report_dir = Path('reports/ui')
    report_dir.mkdir(parents=True, exist_ok=True)
    if remote:
        browser = webdriver.Remote(command_executor=remote, options=options)
    else:
        service = Service(
            executable_path=os.getenv('CHROMEDRIVER'),
            log_output=str(report_dir / (request.node.name + '-chromedriver.log')),
        )
        browser = webdriver.Chrome(service=service, options=options)
    environment = {
        'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
        'python': platform.python_version(),
        'platform': platform.platform(),
        'browser': browser.capabilities.get('browserName'),
        'browser_version': browser.capabilities.get('browserVersion'),
        'chromedriver_version': browser.capabilities.get('chrome', {}).get('chromedriverVersion', '').split(' ')[0],
        'mode': 'remote' if remote else 'local',
        'headless': True,
        'chrome_sandbox_disabled_by_fixture': False,
    }
    (report_dir / 'environment.json').write_text(json.dumps(environment, indent=2), encoding='utf-8')
    allure.attach(json.dumps(environment, indent=2), name='Environnement reel', attachment_type=allure.attachment_type.JSON)
    try:
        browser.set_page_load_timeout(40)
        yield browser
    finally:
        try:
            report = getattr(request.node, 'rep_call', None)
            try:
                allure.attach(browser.get_screenshot_as_png(), name=request.node.name, attachment_type=allure.attachment_type.PNG)
                if report and report.failed:
                    allure.attach(browser.page_source, name='DOM', attachment_type=allure.attachment_type.HTML)
            except WebDriverException as exc:
                allure.attach(str(exc), name='Capture indisponible : navigateur arrêté', attachment_type=allure.attachment_type.TEXT)
        finally:
            browser.quit()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    setattr(item, 'rep_' + report.when, report)

@pytest.fixture
def formy():
    return os.getenv('FORMY_BASE_URL', 'https://formy-project.herokuapp.com').rstrip('/')

@pytest.fixture
def local_page():
    folder = Path(__file__).resolve().parents[2] / 'fixtures'
    content = (folder / 'index.html').read_text(encoding='utf-8')
    frame = html.escape((folder / 'student.html').read_text(encoding='utf-8'), quote=True)
    # Le navigateur distant reçoit les fixtures sans accès au disque du runner.
    content = content.replace('src="student.html"', 'srcdoc="' + frame + '"')
    return 'data:text/html;charset=utf-8,' + quote(content)
