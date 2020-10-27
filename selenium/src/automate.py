from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options as selenium_options


import time
from bs4 import BeautifulSoup
import pickle 
import pandas as pd 

import sqlalchemy
from sqlalchemy import create_engine

import random



engine = create_engine("sqlite:///output/propstream.db",echo=False)
connection = engine.connect()
table = 'scraped_data'


email = 'Your Email' 
pswd = 'Your pass'
options = Options()


SEARCH_KEY = 'Dallas, Texas'




# options.headless = True
# # options.add_argument('--window-size=1920, 1200')

# options.add_argument('--disable-notifications')

browser_options = selenium_options()
browser_options.add_argument("--headless")
browser_options.add_argument('--disable-notificatons')




def scrape(soup=None,page_number=None,connection=None):
    # soup = BeautifulSoup(pickle.load(open('base.pkl','rb')),'lxml')

    try:
        table_present = engine.dialect.has_table(engine, 'scraped_data')
        if page_number==1 and table_present:
            test_df = pd.read_sql_query('SELECT * FROM scraped_data',engine)
            max_page = test_df['page_number'].max()
            print("Data exists till page number: ",max_page)
            print("Starting Scrapper from page number :",max_page+1)
            
        elif page_number==1 and table_present==False:
            max_page =0
            print('No table found starting fresh')
        else:
            max_page=page_number-1
    except Exception as e:
        max_page = 0
        print("Exception occured at table checking, Exception: ",e)

    if page_number>max_page:
        
        try:

            table = soup.find('table')

            columns = []

            rows = []

            for i in table.findAll('th'):
                columns.append(i.text)

            for i in table.findAll('tr')[1:]:
                row = []
                for j in i.findAll('td'):
                    row.append(j.text)
                rows.append(row)


            df = pd.DataFrame(rows, columns=columns)
            df['page_number'] = page_number
            df.rename(columns={' ':'blank','':'_blank'},inplace=True)

            max_page = df['page_number'].max()

            df.to_sql('scraped_data',connection,if_exists='append')

            del df
        except Exception as e:
            print("Exception occured at finding soup attributes, Exception: ",e)
            print("error at page number : ",page_number )


        # print(df)    
    else :
        print('data exists skipping page number: ',page_number)
    
    return max_page





# chromedriver = "../Cdriver/chromedriver.exe"
driver = webdriver.Firefox(options=browser_options)
driver.get("https://login.propstream.com/")


login = driver.find_element_by_name('username')
password = driver.find_element_by_name('password')


login.send_keys(email)
password.send_keys(pswd)

submit = driver.find_element_by_class_name('gradient-btn')
submit.click()
    
try:
    WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME,'_3FtuS__border-blue')))
    driver.find_element_by_class_name('_3FtuS__border-blue').click()
    search = driver.find_element_by_tag_name('input')
    search.send_keys(SEARCH_KEY)


    try:
        WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CLASS_NAME,'react-autosuggest__suggestion-wrapper')))
        driver.find_elements_by_css_selector("span[class='react-autosuggest__suggestion-wrapper']")[0].click()
        driver.find_element_by_class_name('_2rE15__rightExpand').click()


        time.sleep(2)
        

        soup = BeautifulSoup(driver.page_source,'lxml')

        pages = soup.find('div',{'class':'_2cHFz__currentPage'}).findAll('span')
        pages = pages[2].text.split(' ')[-1]
        max_page = scrape(soup,page_number=1,connection=connection)

        for i in range(max_page+1,int(pages)):
            try:
                if i==int(pages)-1:
                    print(f"Scrapped data from {pages} pages")
                    print("Stopping scrapper")
                    break
                
                page_field= driver.find_elements_by_css_selector("input[class='_3CzCP__input']")[0]
                page_field.send_keys(i)
                page_field.send_keys(Keys.ENTER)
                WebDriverWait(driver,10).until(EC.presence_of_element_located((By.TAG_NAME,'table')))
                print("Loaded page number: ",i)
                time.sleep(random.randint(3,8))
                soup = BeautifulSoup(driver.page_source,'lxml')
                _=scrape(soup, page_number=i,connection=connection)
                print("Scrapped page number: ",i)
            except Exception as e:
                print("Exception occured in loop, Exception: ",e)




    except Exception as e:
        print("Exception at inner level 2:",e)

except Exception as e:
    print("Excepotion at outer level: ",e)

driver.quit()