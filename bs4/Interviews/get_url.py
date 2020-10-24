from bs4 import BeautifulSoup

import requests


html = requests.get('https://www.geeksforgeeks.org/company-interview-corner/').text

soup = BeautifulSoup(html, 'html.parser')

soup = soup.find(class_="sUlClass")

URL_list = []

for c,i in enumerate(soup.findAll('a')):
    URL_list.append(i['href'])
    if 'wipro' in i['href']: #31
        idx =c


print(URL_list[idx:])

