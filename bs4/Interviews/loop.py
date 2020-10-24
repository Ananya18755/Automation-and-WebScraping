from bs4 import BeautifulSoup
import requests
import sqlite3
import pandas as pd 
from sqlalchemy import create_engine
import time 

# URL_list = ['https://www.geeksforgeeks.org/tag/amazon/','https://www.geeksforgeeks.org/tag/microsoft/',
# 			'https://www.geeksforgeeks.org/tag/oracle/','https://www.geeksforgeeks.org/tag/makemytrip/',
# 			'https://www.geeksforgeeks.org/tag/flipkart/','https://www.geeksforgeeks.org/tag/paytm/',
# 			'https://www.geeksforgeeks.org/tag/adobe/','https://www.geeksforgeeks.org/tag/samsung/',
# 			'https://www.geeksforgeeks.org/tag/snapdeal/','https://www.geeksforgeeks.org/tag/vmware/']


engine = create_engine('sqlite:///scraped_data.db',echo=True)

connection = engine.connect()

table = 'Interviews'


html = requests.get('https://www.geeksforgeeks.org/company-interview-corner/').text

soup = BeautifulSoup(html, 'html.parser')

soup = soup.find(class_="sUlClass")

URL_list = []

for i in soup.findAll('a'):
    URL_list.append(i['href'])


#done till wipro page 3




# ID = []
# titles = []
# dates = []
# body = []
# upvotes=[]
# company=[]
# urls = []


for orig_url in URL_list[32:]:

	for j in range(1,100):

		ID = []
		titles = []
		dates = []
		body = []
		upvotes=[]
		company=[]
		urls = []

		i=orig_url
	
		if j == 1:
			pass
		else: 
			i=i+"page/"+str(j)
		try: 
			print(i)
			check = html = requests.get(i)
			if str(check) == "<Response [404]>":
				print("Page {} not found".format(j))
				break
			else:
				pass
			html = html.text


			soup = BeautifulSoup(html, "lxml")

			tag = soup.find(class_='archive-title').span.contents[0]
			print(tag)

			articles = soup.find_all('article')
			print(len(articles))

			links = []
			a = articles[0]
			for article in articles:
				link= article.find('a')['href']
				links.append(link)

			# print(urls)



			# variables



			count = 0

			for link in links:
				# url = 'https://www.geeksforgeeks.org/amazon-interview-experience-sde-2-3/'


				html = requests.get(link).text
				urls.append(link)

				soup = BeautifulSoup(html, "lxml")



				post = soup.find('div',class_='site-content')

				title = soup.html.head.title.string
				titles.append(title)

				ids = post('article')[0]['id'].split('-')[1]
				# print("id :",id )
				ID.append(ids)

				upvote = soup.find('div',class_='plugins upvoteArticle').span.contents
				if upvote[0] == 'Be the First to upvote.':
					upvote = 0
					upvotes.append(upvote)
				else:
					upvotes.append(upvote[0])

				script= soup.find_all('script')[3].contents
				date= script[0].split('\n')[-3].split('=')[1].split('"')[1].split(' ')[0]
				dates.append(date)

				# s = s[1].split('"')
				# s = s[1].split(' ')[0]





				contents = soup.find('div',class_='entry-content')

				#print(contents)


				text = []

				for c in contents.find_all('p'):

					if c.a:
						text.append(" ")
						pass
					else:

						#print(c.text)
						text.append(c.text)
						
						
				new_text = []
				for t in text:
					
					t = t.replace('\n',' ')
					new_text.append(t)

				#print(new_text)

				def convert(s): 
				
					# initialization of string to "" 
					new = "" 
				
					# traverse in the string  
					for x in s: 
						new += x+' '  
				
					# return string  
					return new 


				new_text = convert(new_text)
				body.append(new_text)
				company.append(tag)

				count = count+1
				print(count)
		except Exception as e: 
			print(e)
		try: 

			data = {'ID':ID,'Date':dates,'Titles':titles,'Company':company,'Experience':body,'Upvotes':upvotes,'URLS':urls}
			df = pd.DataFrame(data)
			
			

			df.to_sql(table,connection,if_exists='append')
			del data
			del df 
			print("Page {} appended to database".format(j))
		except Exception as e:
			print(e)
		# time.sleep(5)













