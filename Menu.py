import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import xlsxwriter
import csv
from selenium.webdriver.common.keys import Keys
import xlrd
import os
import getpass
from selenium.webdriver.chrome.service import Service
import pickle
import requests

username = getpass.getuser()

if username == 'shaezal.cheema':
    os.chdir('C:/Users/shaezal.cheema/Dropbox/PRA/')
if username == 'Home':
    os.chdir('C:/Users/Home/Dropbox/PRA/')
if username == 'zarnaab.ather':
    os.chdir('C:/Users/zarnaab.ather/Dropbox/PRA/')
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



facebook = webdriver.Chrome(service=Service, options=option)

facebook.get('https://www.facebook.com/')

for cookie in cookies:
    facebook.add_cookie(cookie)

facebook.refresh()

#facebook = webdriver.Chrome(executable_path=r"Code\Web Scraping\\Facebook\\chromedriver.exe")
# facebook.get("https://www.facebook.com/")
# email = facebook.find_element(By.CSS_SELECTOR, 'input[name="email"]')
# password = facebook.find_element(By.CSS_SELECTOR, 'input[name="pass"]')
# sub_btn = facebook.find_element(By.CSS_SELECTOR, 'button[name="login"]')
# email.send_keys("resturant762@gmail.com")
# password.send_keys("Kathmandu@123")
# time.sleep(1)
# sub_btn.click()
time.sleep(2)

parent_dir = "menu/"
store_url = "Web Scraping\\Output\\Facebook\\23-01-2024\\menu"
try:
    os.makedirs('Web Scraping\\Output\\Facebook\\23-01-2024\\menu')
except OSError as error:
    print(error)
time.sleep(2)
resturants_list = []

# READ FILE FROM CSV FILE
# with open("./FacebookLinks - New List(26May2023) (1).csv", encoding="utf8") as file:
#   csvreader = csv.reader(file)
#   for row in csvreader:
#       try:
#         resturants_list.append(row[1])
#       except:
#           continue

# READ FILE FROM Excel FILE(.xls) format

# book = xlrd.open_workbook("RestaurantsInformation.xls")
# sh = book.sheet_by_index(0)
#for rx in range(1,sh.nrows):
 #   print(sh.row(rx)[0].value)
  #  resturants_list.append(sh.row(rx)[0].value)

with open(r"Web Scraping\\Output\\Facebook\\AllLinks.csv", 'r') as file:
  csvreader = csv.reader(file)
  for row in csvreader:
      resturants_list.append(row[1])

# Loop all rows
# for index in range(0, len(resturants_list)):
# Loop defined rows
for index in resturants_list[1:]:
  
    try:
        if len(index.split("profile.php")) > 1:
            facebook.get(index.split("&")[0] + "/menu")
        else:
            if index.split("?")[0][-1] == '/':
                facebook.get(index.split("?")[0] + "menu")
            else:
                facebook.get(index.split("?")[0] + "/menu")
        try:
            facebook.find_element(By.CSS_SELECTOR, 'div[aria-label="Close"]').click()
        except:
            print("")
        time.sleep(3)
        name_folowers_likes = facebook.find_element(By.CSS_SELECTOR, 'div.x1e56ztr.x1xmf6yo span[dir="auto"]')
        name = name_folowers_likes.text
        replacements = [('!', ''), ('?', ''), ('@', ''),('-', ''), ('&', ''), (' ', '')]
        for char, replacement in replacements:
            if char in name:
                name = name.replace(char, replacement)
        print(name.strip())
        folder = os.path.join(store_url, name.strip())
        print(folder)
        no_of_image_stored = 0
        try:
            os.mkdir(folder)
        except OSError as error:
            print(error)
            os.listdir(folder)
            # print(len(os.listdir(path)))
            no_of_image_stored = len(os.listdir(folder))
            print(error)

        # menu_photos = facebook.find_elements(By.CSS_SELECTOR, 'a[rel="theater"]')
        menu_photos = facebook.find_elements(By.CSS_SELECTOR, 'img.x1lq5wgf.xgqcy7u.x30kzoy.x9jhf4c.x6ffb70.xl1xv1r.x1rji325')
        
        print(no_of_image_stored)
        print(len(menu_photos))
        if no_of_image_stored != len(menu_photos):
            for photo in menu_photos:
                url = photo.get_attribute('src')
                response = requests.get(url)
                # facebook.execute_script("arguments[0].click()", menu_photos[index] )
                # # menu_photos[index].click()
                # time.sleep(3)
                # print(facebook.find_element(By.CSS_SELECTOR, 'img').get_attribute('src'))
                # url = facebook.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
    
                filename_array = url.split("?")[0].split("/")
                filename = filename_array[len(filename_array) - 1]
                print("menu/" + name.strip() + "/" + filename)
                with open(store_url + "/" + name.strip() + "/" + filename, "wb") as f:
                    f.write(response.content)
                # facebook.find_element(By.CSS_SELECTOR, 'div[aria-label="Close"]').click()
    
       
    except:
        continue