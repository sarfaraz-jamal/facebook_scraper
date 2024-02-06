# -*- coding: utf-8 -*-
"""
Created on Tue Jan 11 18:02:07 2022

@author: Zarnaab Ather
"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import getpass
import os 
import pandas as pd
from bs4 import BeautifulSoup
import re 
import pickle


USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

username = getpass.getuser()


# if username == 'Home':
#     os.chdir('C:/Users/Home/Dropbox/PRA/')
# if username == 'zarnaab.ather':
#     os.chdir('C:/Users/zarnaab.ather/Dropbox/PRA/')

Service = Service(executable_path="Code_4_Web Scraping\\Facebook\\chromedriver.exe")
option = webdriver.ChromeOptions()

option.add_argument("--disable-infobars")
option.add_argument("start-maximized")
option.add_argument("--disable-extensions")
# Set the custom User-Agent
option.add_argument(f"--user-agent={USER_AGENT}")


# Pass the argument 1 to allow and 2 to block
option.add_experimental_option("prefs", { 
    "profile.default_content_setting_values.notifications": 2
})

SCROLL_PAUSE_TIME = 10



driver = webdriver.Chrome(service=Service, options=option)

driver.get('https://www.facebook.com/')

time.sleep(5)

usr = "sarfaraz.w.jamal@gmail.com"
pwd = "wahid52625"

 
username_box = driver.find_element(By.ID, 'email')
username_box.send_keys(usr)
print ("Email Id entered")
time.sleep(5)
 
password_box = driver.find_element(By.ID, 'pass')
password_box.send_keys(pwd)
password_box.send_keys(Keys.ENTER)
print ("Password entered")

time.sleep(5)

cookies = driver.get_cookies()

driver.close()



pickle.dump(cookies, open("cookies.pkl", "wb"))
