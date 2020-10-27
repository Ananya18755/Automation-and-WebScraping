import sqlalchemy
from sqlalchemy import create_engine

import pandas as pd 

engine = create_engine("sqlite:///output/propstream.db",echo=False)
connection = engine.connect()
table = 'scraped_data'


df = pd.read_sql_query('SELECT * FROM scraped_data',engine)

df.to_excel('Dallas_Texas.xlsx',index=False)