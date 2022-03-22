import os
from time import sleep
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager as CM

def check_difference_in_count(driver):
    global count

    new_count = len(driver.find_elements_by_xpath("//div[@role='dialog']//li"))

    if count != new_count:
        count = new_count
        return True
    else:
        return False

username = 'osakakuma'
password = 'Okuma2020'

driver = webdriver.Chrome("C:/Users/SSY/Downloads/chromedriver_win32/chromedriver.exe")
driver.get("https://instagram.com")
sleep(2)
driver.find_element_by_xpath("//input[@name=\"username\"]").send_keys(username)
driver.find_element_by_xpath("//input[@name=\"password\"]").send_keys(password)
driver.find_element_by_xpath('//button[@type="submit"]').click()
sleep(4)
not_now1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click() 
not_now2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()
driver.get("https://www.instagram.com/osakakuma/")
driver.find_element_by_partial_link_text("follower").click()
xpath = "//div[@style='position: relative; z-index: 1;']/div/div[2]/div/div[1]"
WebDriverWait(driver, 10).until(
EC.presence_of_element_located((By.XPATH, xpath)))

sleep(4)
count = 0

while 1:
    # scroll down
    driver.execute_script("document.querySelector('div[role=dialog] ul').parentNode.scrollTop=1e100")

    try:
        WebDriverWait(driver, 5).until(check_difference_in_count)
        xpath = "//div[@style='position: relative; z-index: 1;']//ul/li/div/div/div/div/a"
        followers_elems = driver.find_elements_by_xpath(xpath)

    except:
        break

print(e.text for e in followers_elems)















