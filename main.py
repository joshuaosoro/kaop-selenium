from sqlalchemy import create_engine, MetaData, Date, String, Integer, Column, Table
import pandas as pd
import os
import pymysql
pymysql.install_as_MySQLdb()

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

# headless-mode
options = Options()
options.headless = True
#options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("http://kaop.co.ke")
driver.implicitly_wait(30)

select_county = Select(driver.find_element(By.ID, 'County'))
select_county.select_by_value("43")

select_constituency = Select(driver.find_element(By.ID, 'Constituency'))
select_constituency.select_by_value("98")

select_ward = Select(driver.find_element(By.ID, 'Ward'))
select_ward.select_by_value("487")

driver.find_element(By.XPATH, '//div/input').click()

imgs = driver.find_elements(By.XPATH, '//div/img')
containers = driver.find_elements(By.CLASS_NAME, 'weatherbox')

date = []
min_temp = []
max_temp = []
rainfall_chance = []
rainfall_amount = []
humidity = []
wind_speed = []

for c in containers:
    elem = c.text.split('\n')
    date.append(elem[0].split(':')[1])
    min_temp.append(elem[2].split(':')[1])
    max_temp.append(elem[3].split(':')[1])
    rainfall_chance.append(elem[4].split(':')[1])
    rainfall_amount.append(elem[5].split(':')[1])
    humidity.append(elem[6].split(':')[1])
    wind_speed.append(elem[7].split(':')[1])


hrefs = [i.get_attribute('src') for i in imgs]

weather_dict = {
    'date': date,
    'min_temp': min_temp,
    'max_temp':max_temp,
    'rainfall_chance': rainfall_chance,
    'rainfall_amount': rainfall_amount,
    'humidity': humidity,
    'wind_speed': wind_speed,
    'img': hrefs
}

weather_df = pd.DataFrame(weather_dict)
weather_df

# data cleaning
weather_df['min_temp'] = weather_df['min_temp'].str.extract('(\d+)')
weather_df['max_temp'] = weather_df['max_temp'].str.extract('(\d+)')
weather_df['rainfall_chance'] = weather_df['rainfall_chance'].str.extract('(\d+)')
weather_df['rainfall_amount'] = weather_df['rainfall_amount'].str.extract('(\d+)')
weather_df['humidity'] = weather_df['humidity'].str.extract('(\d+)')
weather_df['wind_speed'] = weather_df['wind_speed'].str.extract('(\d+)')

# take care of the data types
weather_df['date'] = pd.to_datetime(weather_df['date']) 
weather_df['min_temp'] = weather_df['min_temp'].astype(int)
weather_df['max_temp'] = weather_df['max_temp'].astype(int)
weather_df['rainfall_chance'] = weather_df['rainfall_chance'].astype(int)
weather_df['rainfall_amount'] = weather_df['rainfall_amount'].astype(int)
weather_df['humidity'] = weather_df['humidity'].astype(int)
weather_df['wind_speed'] = weather_df['wind_speed'].astype(int)

print(weather_df)

## send data to the database
credentials = {
    "Host": "sql7.freesqldatabase.com",
    "Database_name": "sql7588148",
    "Database_user": "sql7588148",
    "Database_password": "dkeHeFUvie",
    "Port_number": 3306
}

conn = f'mysql://{credentials["Database_user"]}:{credentials["Database_password"]}@{credentials["Host"]}:3306/{credentials["Database_name"]}'
engine = create_engine(conn)
metadata_obj = MetaData()


weather = Table(
    'weather', 
    metadata_obj,
    Column('id', Integer, primary_key=True), 
    Column("date", Date), 
    Column("min_temp", Integer),
    Column("max_temp", Integer),
    Column("rainfall_chance", Integer),
    Column("rainfall_amount", Integer),
    Column("humidity", Integer),
    Column("img", String(100)),
)

weather.drop(engine, checkfirst=True) # drop table before adding in fresh data
weather_df.to_sql("weather", engine)  # add the new data to the weather
