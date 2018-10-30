from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from MyLog import my_log
from common import *
import time

fireFoxOptions = webdriver.FirefoxOptions()
fireFoxOptions.set_headless()

fp = webdriver.FirefoxProfile()
user_agent = get_header()
my_log.logger.info("user-agent:"+user_agent)
fp.set_preference("general.useragent.override", user_agent)
fp.update_preferences()
cap = webdriver.DesiredCapabilities.FIREFOX
cap['firefox_profile'] = fp.encoded

# driver = webdriver.Firefox(executable_path="./geckodriver",firefox_options=fireFoxOptions,firefox_profile =fp)
driver = webdriver.Firefox()

driver.get("https://httpbin.org/get?show_env=1")
html = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
my_log.logger.info(html)
print("sleep 10s")
time.sleep(10)
driver.close()


# while True:
#     time.sleep(5)
#     my_log.logger.info("sleep 5s...")
# print("exit...............")
# print(html)
# driver.get("https://www.tigonetwork.com/")
# contact = driver.find_element_by_class_name("contact_info").text
# print(contact)

# assert "Python" in driver.title
# elem = driver.find_element_by_name("q")
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source

