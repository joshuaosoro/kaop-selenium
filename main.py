import pandas as pd

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By

# headless-mode
options = Options()
options.headless = True

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)
driver.get("http://kaop.co.ke")
driver.implicity_wait(30)

select_county = Select(driver.find_element(By.ID, 'County'))
select_county.select_by_value("43")

select_constituency = Select(driver.find_element(By.ID, 'Constituency'))
select_constituency.select_by_value("98")

select_ward = Select(driver.find_element(By.ID, 'Ward'))
select_ward.select_by_value(487)

driver.find_element(By.XPATH, '//div/input').click()

imgs = driver.find_element(By.XPATH, '//div/img')
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

weather_df['min_temp'] = weather_df['min_temp'].str.extract('(\d+)')
weather_df['max_temp'] = weather_df['max_temp'].str.extract('(\d+)')
weather_df['rainfall_chance'] = weather_df['rainfall_chance'].str.extract('(\d+)')
weather_df['rainfall_amount'] = weather_df['rainfall_amount'].str.extract('(\d+)')
weather_df['humidity'] = weather_df['humidity'].str.extract('(\d+)')
weather_df['wind_speed'] = weather_df['wind_speed'].str.extract('(\d+)')
weather_df


print(weather_df)

  