import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

pytestmark = pytest.mark.formy
def click(driver, by, value):
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((by, value))).click()

@allure.title('UI-01 | Inscription, radio et liste déroulante')
def test_ui01_form(driver, formy):
    driver.get(formy + '/form')
    for key, value in [('first-name','Sara'), ('last-name','Bennani'), ('job-title','QA Engineer')]:
        driver.find_element(By.ID, key).send_keys(value)
    click(driver, By.ID, 'radio-button-2')
    assert driver.find_element(By.ID, 'radio-button-2').is_selected()
    click(driver, By.ID, 'checkbox-2')
    assert driver.find_element(By.ID, 'checkbox-2').is_selected()
    select = Select(driver.find_element(By.ID, 'select-menu'))
    select.select_by_value('2')
    assert select.first_selected_option.get_attribute('value') == '2'
    driver.find_element(By.ID, 'datepicker').send_keys('10/05/2026', Keys.TAB)
    click(driver, By.LINK_TEXT, 'Submit')
    message = WebDriverWait(driver, 15).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'.alert-success')))
    assert 'successfully submitted' in message.text.lower()

@allure.title('UI-02 | Boutons et menu')
def test_ui02_buttons(driver, formy):
    driver.get(formy + '/buttons')
    click(driver, By.XPATH, "//button[normalize-space()='Primary']")
    click(driver, By.ID, 'btnGroupDrop1')
    item = WebDriverWait(driver,15).until(EC.visibility_of_element_located((By.CSS_SELECTOR,'.dropdown-menu.show .dropdown-item')))
    assert item.text.strip()
    item.click()
    WebDriverWait(driver,15).until(EC.invisibility_of_element_located((By.CSS_SELECTOR,'.dropdown-menu.show')))

@allure.title('UI-03 | Ouvrir et fermer une fenêtre modale')
def test_ui03_modal(driver, formy):
    driver.get(formy + '/modal')
    click(driver, By.ID, 'modal-button')
    modal = WebDriverWait(driver,15).until(EC.visibility_of_element_located((By.ID,'exampleModal')))
    assert 'Modal title' in modal.text
    click(driver, By.ID, 'close-button')
    WebDriverWait(driver,15).until(EC.invisibility_of_element_located((By.ID,'exampleModal')))

@allure.title('UI-04 | Alerte JavaScript et nouvelle fenêtre')
def test_ui04_alert_window(driver, formy):
    driver.get(formy + '/switch-window')
    original = driver.current_window_handle
    click(driver, By.ID, 'alert-button')
    alert = WebDriverWait(driver,15).until(EC.alert_is_present())
    assert alert.text == 'This is a test alert!'
    alert.accept()
    assert not EC.alert_is_present()(driver)
    before = set(driver.window_handles)
    click(driver, By.ID, 'new-tab-button')
    WebDriverWait(driver,15).until(EC.number_of_windows_to_be(2))
    driver.switch_to.window((set(driver.window_handles) - before).pop())
    WebDriverWait(driver,15).until(lambda d: d.current_url.startswith(formy))
    assert driver.find_element(By.TAG_NAME,'body').is_displayed()
    driver.close()
    driver.switch_to.window(original)
    assert driver.current_window_handle == original
