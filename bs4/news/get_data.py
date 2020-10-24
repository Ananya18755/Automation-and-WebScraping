import requests
from bs4 import BeautifulSoup
import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd 
import time as t

engine = create_engine("sqlite:///lockdown_news_indian_express.db",echo=False)
connection = engine.connect()
table = 'lockdown'

# html = requests.get("https://www.ndtv.com/page/topic-load-more?type=news&page=0&query=lockdown").text
orig = 'https://indianexpress.com/page/'
search_key = "/?s=lockdown"



for i in range (490,601): 
    url = orig+str(i)+search_key
    # url = 'https://indianexpress.com/page/0/?s=lockdown'
    print(url)
    print("ON PAGE NUMBER : ",i)

    try :

        links = []
        headline=[]
        summary=[]
        date=[]
        contents=[]  

        html = requests.get(url).text
        # print(html)
        
        page = BeautifulSoup(html,'lxml')
        # print(page)

        lists = page.find(class_="search-result")
        # print(lists)
        articles = lists.find_all(class_='details')
        # print(articles[0].text)


        for a in articles:  
            hline = a.find('h3').text
            headline.append(hline)
            # print(hline)

            link = a.find('a')['href']
            links.append(link)
            # print(link)

            content = []
            cntnt = requests.get(link).text
            cntnt = BeautifulSoup(cntnt,'lxml')
            cntnt = cntnt.find(class_="full-details")
            cntnt = cntnt.find_all('p')

            for p in cntnt:  

                content.extend([p.text])
                
            
            content = " ".join(content)
            contents.append(content)
            # print(content)
            


            smry = a.find('p').text
            summary.append(smry)
            # print(smry)

            dt,time = a.find('time').text.split("Updated:")[-1].split('at')
            dt = " ".join([dt,time])
            date.append(dt)
            # print(dt)
        
        data = {'date':date,'headline':headline,'summary':summary,'content':contents,'link':links}

        df = pd.DataFrame(data)
        print(df)
        # df.to_excel("results.xlsx",engine='xlsxwriter')
        

        df.to_sql(table,connection,if_exists='append')
        del data 
        del df 

    except Exception as e:
        print(e)
    
        







    