
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time 
import datetime
from time import strftime
import pandas as pd
from dateutil import parser
import numpy as np 

import os 

# from dotenv import load_dotenv
# load_dotenv('./config.env')

DRIVER_PATH = '../Cdriver/chromedriver'

EMAIL = 'dasdad'
PSWD = 'dsds'
options = Options()
# options.headless = True
# options.add_argument('--window-size=1920, 1200')

options.add_argument('--disable-notifications')

driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)

search = str('oajrlxb2 rq0escxv f1sip0of hidtqoto lzcic4wl hzawbc8m ijkhr0an nlq1og4t sgqwj88q b3i9ofy5 oo9gr5id b1f16np4 hdh3q7d8 dwo3fsh8 qu0x051f esr5mh6w e9989ue4 r7d6kgcz br7hx15l h2jyy9rg n3ddgdk9 owxd89k7 ihxqhq3m jq4qci2q k4urcfbm iu8raji3 qypqp5cg l60d2q6s hv4rvrfc hwnh5xvq dati1w0a o1lsuvei o6r2urh6 rmlgq0sb aj8hi1zk r4fl40cc kd8v7px7 m07ooulj mzan44vs')

import pickle





def process_time(x):

    print("TIME : ",x)
    try:
        if 'at' in x:
            og_tm = parser.parse("".join(x.split('at')))
        elif 'm' in x:
            tm = int(x[:-1])
            delta = datetime.timedelta(minutes=tm)
            og_tm = datetime.datetime.now() - delta
        elif 'h' in x:
            tm = int(x[:-1])
            delta = datetime.timedelta(hours=tm)
            og_tm = datetime.datetime.now() - delta
        elif 'd' in x:
            tm = int(x[:-1])
            delta = datetime.timedelta(days=tm)
            og_tm = datetime.datetime.now() - delta
        

        return og_tm
    except Exception as e:
        print("ECEPTION:",e)
        return -1

def process_post(post):
    try:
        text = post.find_element_by_css_selector("div[class='kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql ii04i59q'").text
    except Exception as e:
        text = 'noText'
    try:
        likes = post.find_element_by_css_selector("span[class='pcp91wgn'").text
    except Exception as e:
        likes = np.nan        
    ago = post.find_element_by_css_selector("a[class='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8 b1v8xokw']")
    link = ago.get_attribute('href')
    link = link.split('?')[0]
    post_id = link.split('/')[-1]
    ago = process_time(ago.text)
    try :
        share = post.find_element_by_css_selector("span[class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql gk29lw5a a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d9wwppkn fe6kdd0r mau55g9w c8b282yb hrzyx87i jq4qci2q a3bd9o3v knj5qynh m9osqain']").text
    except Exception as e:
        share = np.nan

    
    try: 
        if ago <= datetime.datetime(2020,9,1,0,0):
            d = True
        else:
            d = False
    except Exception as e:
        d = False
        print("Exception :",e)
    
    print("Posted on: ",ago)
    print("Post text: ",text)
    print("Likes: ",likes)
    print("Shares: ",share)
    print("Link: ",link)
    print("Post id: ",post_id)

    return ago, post_id, text, likes, share,link,d



def scrap():
    driver.get('https://www.facebook.com/')
    try: 
        login = driver.find_element_by_id('email')
        pswd = driver.find_element_by_id('pass')
        
        login.send_keys(EMAIL)
        pswd.send_keys(PSWD)
        
        submit = driver.find_element_by_name('login')
        
        submit.click()
        
        print("login successfull")

        time.sleep(3)
    
        
        # driver.get('https://www.facebook.com/TataMotorsGroup')
        driver.get('https://www.facebook.com/RelianceIndustriesLimited')

        time.sleep(5)
        
        SCROLL_PAUSE_TIME = 3

# Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        LIKES= list()
        SHARES= list()
        POSTS = list()
        TIME = list()
        LINKS= list()
        POST_IDS = list()
        
        idx = 0 

        posts = driver.find_elements_by_css_selector("div[class='du4w35lb k4urcfbm l9j0dhe7 sjgh65i0'")
        idx = len(posts)

        print("Posts accquired")

        for post in posts:

            ago, post_id, text, likes, share,link,_ = process_post(post)
            TIME.append(ago)
            SHARES.append(share)
            LIKES.append(likes)
            POSTS.append(text)
            LINKS.append(link)
            POST_IDS.append(post_id)

        done = False
        while 1:

            
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            posts = driver.find_elements_by_css_selector("div[class='du4w35lb k4urcfbm l9j0dhe7 sjgh65i0'")
            print("len posts:",len(posts))
            if len(posts) > idx:
                posts = posts[idx:]
                idx = idx+len(posts)
            print(idx)
            
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            time.sleep(2)

        
            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

            for post in posts:

                ago, post_id, text, likes, share,link, done = process_post(post)
                TIME.append(ago)
                SHARES.append(share)
                LIKES.append(likes)
                POSTS.append(text)
                LINKS.append(link)
                POST_IDS.append(post_id)

            if done:
                break

        
    except Exception as e:
        print(e)
    
    return zip(TIME,POST_IDS,POSTS,LIKES,SHARES,LINKS)

data = scrap()
driver.quit()

df= pd.DataFrame(data,columns=['time','ids','post','likes','shares','link'])

print(df.head())

df.to_csv('../output/RIL_data.csv',index=False)