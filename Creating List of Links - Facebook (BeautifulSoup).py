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


if username == 'Home':
    os.chdir('C:/Users/Home/Dropbox/PRA/')
if username == 'zarnaab.ather':
    os.chdir('C:/Users/zarnaab.ather/Dropbox/PRA/')
if username == 'shaezal.cheema':
    os.chdir('C:/Users/shaezal.cheema/Dropbox/PRA/')
if username == 'TLS':
    os.chdir('C:/Users/TLS/Desktop/')

cookies = pickle.load(open("Web Scraping\\Code_4_Web Scraping\\Facebook\\cookies.pkl", "rb"))
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

Service = Service(executable_path="Web Scraping\\Code_4_Web Scraping\\Facebook\\chromedriver.exe")
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

for cookie in cookies:
    driver.add_cookie(cookie)

driver.refresh()

time.sleep(3)

 
#RUN TILL HERE - Wait for it to login and then run the rest of the script
base_url = "https://www.facebook.com/search/places/?q=restaurant%20cafe%20lahore%20pakistan"
driver.get(base_url) 

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
    
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        time.sleep(SCROLL_PAUSE_TIME)
        
LinksList = []     
#Links = []
#Name = []
#Cuisine = []
#Location = []
#Likes = []
#Rating = []

html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

#Pages = soup.find_all('div', class_ = 'j83agx80 l9j0dhe7 k4urcfbm')
Pages = soup.find_all('div', class_ = 'x78zum5 x1n2onr6 xh8yej3')

    
    
for page in Pages:
        s=page.get_text()
        #Link = page.find("a",href=True)["href"]
        Link = page.find('a',attrs={'href': re.compile("https://")})
        Links = Link.get('href')
      
        print(Links)
        
        Name = page.find("a", class_ = "x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f").text
        print(Name)

        LinksList.append((Links, Name)) 

     
Links_df = pd.DataFrame(LinksList,columns=['Link','Name'])
Links_df.to_csv('Web Scraping\\Output\\Facebook\\AllLinks.csv')   





