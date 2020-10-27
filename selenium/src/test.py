import requests

from bs4 import BeautifulSoup


# html = requests.get('https://www.google.com').text

import pickle

html = pickle.load(open('base.pkl','rb'))


soup= BeautifulSoup(html, 'lxml')

print(str(soup))



# pickle.dump(str(soup), open('base.pkl','wb'))