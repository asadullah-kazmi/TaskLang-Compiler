from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
time.sleep(2)
driver.get("https://google.com/")
driver.find_element("name", "q").send_keys("compiler project")
driver.find_element("name", "q").send_keys(Keys.ENTER)
time.sleep(2)
driver.save_screenshot("test.png")