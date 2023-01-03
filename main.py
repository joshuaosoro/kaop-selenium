from selenium import webdriver
import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# headless-mode
options = Options()
options.headless = True

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options = options)
driver.get("https://www.google.com")
print(driver.page_source)

    #print("hello world")

#chrome_options = webdriver.ChromeOptions()
#chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
#chrome_options.add_argument('--headless')
#chrome_options.add_argument('--disable-dev-shm-usage')
#chrome_options.add_argument('--no-sandbox')
#driver = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), chrome_options=chr)
#driver.get('https://www.google.come')

