import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

pytestmark = pytest.mark.local

@allure.title('UI-05 | Connexion locale : refus puis acceptation')
def test_ui05_login(driver, local_page):
    driver.get(local_page)
    driver.find_element(By.ID,'email').send_keys('sara@example.test')
    pwd = driver.find_element(By.ID,'password')
    pwd.send_keys('incorrect')
    driver.find_element(By.ID,'login').click()
    assert driver.find_element(By.ID,'status').text == 'Identifiants invalides'
    pwd.clear()
    pwd.send_keys('QaOps-demo-2026')
    driver.find_element(By.ID,'login').click()
    assert driver.find_element(By.ID,'status').text == 'Bienvenue Sara'

@allure.title('UI-06 | Entrer dans un iframe puis revenir au document')
def test_ui06_iframe(driver, local_page):
    driver.get(local_page)
    WebDriverWait(driver,10).until(EC.frame_to_be_available_and_switch_to_it((By.ID,'student-frame')))
    driver.find_element(By.ID,'student').send_keys('Sara Bennani')
    driver.find_element(By.ID,'save').click()
    assert driver.find_element(By.ID,'result').text == 'Étudiant : Sara Bennani'
    driver.switch_to.default_content()
    assert driver.find_element(By.ID,'page-title').text == 'Complément pédagogique QAOps'
