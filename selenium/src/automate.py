from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

email = 'YOUR EMAIL'
pswd = 'YOUR PASSWORD'
options = Options()

# options.headless = True
# options.add_argument('--window-size=1920, 1200')

options.add_argument('--disable-notifications')



chromedriver = "../Cdriver/chromedriver.exe"
driver = webdriver.Chrome(options=options, executable_path=chromedriver)
driver.get("https://login.propstream.com/")


login = driver.find_element_by_name('username')
password = driver.find_element_by_name('password')


login.send_keys(email)
password.send_keys(pswd)

submit = driver.find_element_by_class_name('gradient-btn')
submit.click()

try:
    WebDriverWait(driver,3).until(EC.presence_of_element_located((By.CLASS_NAME,'_3FtuS__border-blue')))
    driver.find_element_by_class_name('_3FtuS__border-blue').click()
    search = driver.find_element_by_tag_name('input')
    search.send_keys('Dallas, TX')
    try:
        WebDriverWait(driver,3).until(EC.presence_of_element_located((By.CLASS_NAME,'react-autosuggest__suggestion-wrapper')))
        driver.find_elements_by_css_selector("span[class='react-autosuggest__suggestion-wrapper']")[0].click()
        driver.find_element_by_class_name('_2rE15__rightExpand').click()
    except Exception as e:
        print(e)

except Exception as e:
    print(e)
    print('not found')
