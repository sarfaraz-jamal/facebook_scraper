import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import xlsxwriter
import csv
import xlrd
import pandas as pd
from selenium.webdriver.common.keys import Keys
import getpass
import os
from selenium.webdriver.chrome.service import Service
import pickle


username = getpass.getuser()

if username == 'shaezal.cheema':
    os.chdir('C:/Users/shaezal.cheema/Dropbox/PRA/')
if username == 'Home':
    os.chdir('C:/Users/Home/Dropbox/PRA/')
if username == 'zarnaab.ather':
    os.chdir('C:/Users/zarnaab.ather/Dropbox/PRA/')
if username == 'TLS':
    os.chdir('C:/Users/TLS/Desktop/')
    
resturants_list = []
# with open("./FacebookLinks - New List(26May2023) (1).csv", encoding="utf8") as file:
#   csvreader = csv.reader(file)
#   for row in csvreader:
#       try:
#         resturants_list.append(row[1])
#       except:
#           continue

#book = pd.read_excel("Output\Web Scraping\Facebook\\7-3-2023\RestaurantsInformation.xlsx")
#sh = book.sheet_by_index(0)
#for rx in range(1,sh.nrows):
#    print(sh.row(rx)[0].value)
#    resturants_list.append(sh.row(rx)[0].value)

with open(r"Web Scraping\\Output\\Facebook\\AllLinks.csv", 'r') as file:
  csvreader = csv.reader(file)
  for row in csvreader:
      resturants_list.append(row[1])

resturant_details = xlsxwriter.Workbook('Web Scraping\\Output\\Facebook\\RestaurantsReviews.xlsx')
resturant_details_sheet = resturant_details.add_worksheet()
resturant_details_row = 1
resturant_details_sheet.write(0, 5, 'Link')
resturant_details_sheet.write(0, 0, 'Name')
resturant_details_sheet.write(0, 1, 'Reviewer Name')
resturant_details_sheet.write(0, 2, 'Reviewer Comment')
resturant_details_sheet.write(0, 3, 'Reviewer Recommend')
resturant_details_sheet.write(0, 4, 'Date')

# Service = Service(executable_path="Code_4_Web Scraping\\Facebook\\chromedriver.exe")
# options = webdriver.ChromeOptions()
# facebook = webdriver.Chrome(service=Service, options=options)
# #facebook = webdriver.Chrome(executable_path=r"Code\Web Scraping\\Facebook\\chromedriver.exe")
# #facebook.get("https://www.facebook.com/")
# email = facebook.find_element(By.CSS_SELECTOR, 'input[name="email"]')
# password = facebook.find_element(By.CSS_SELECTOR, 'input[name="pass"]')
# sub_btn = facebook.find_element(By.CSS_SELECTOR, 'button[name="login"]')
# # email.send_keys("resturant762@gmail.com")
# # password.send_keys("Kathmandu@123")
# # email.send_keys("jimdavid.dumb@gmail.com")
# # password.send_keys("youngdumb")
# email.send_keys("haribadhur275@gmail.com")
# password.send_keys("Apple@77")
# time.sleep(1)
# sub_btn.click()
# time.sleep(10)

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

time.sleep(3)

try:
    # Loop all rows
    # for index in range(0, len(resturants_list)):
    # Loop defined rows
    for index in resturants_list[1:]:
        try:
            if len(index.split("profile.php")) > 1:
                facebook.get(index.split("&")[0] + "/reviews")
            else:
                if index.split("?")[0][-1] == '/':
                    facebook.get(index.split("?")[0] + "reviews")
                else:
                    facebook.get(index.split("?")[0] + "/reviews")

            time.sleep(1)
            name_folowers_likes = facebook.find_element(By.CSS_SELECTOR, 'div.x1e56ztr.x1xmf6yo span[dir="auto"]')
            name = name_folowers_likes.text
            print(name)
            new_array_length = 0
            old_array_length = 0
            count = 0
            reviewer_name_array = []
            while True:
                new_array_length = len(facebook.find_elements(By.CSS_SELECTOR, 'div.x1yztbdb.x1n2onr6'))
                if old_array_length == new_array_length:
                    break
                old_array_length = new_array_length
                time.sleep(5)

                # print(len(facebook.find_elements(By.CSS_SELECTOR, 'div.x1yztbdb.x1n2onr6')))
                reviews = facebook.find_elements(By.CSS_SELECTOR, 'div.x1yztbdb.x1n2onr6')
                for review in reviews:
                    try:
                        divs_inside = review.find_elements(By.CSS_SELECTOR, 'div[role="button"]')
                        for div in divs_inside:
                            if div.text == 'See more':
                                div.click()
                    except:
                        continue
                reviews = facebook.find_elements(By.CSS_SELECTOR, 'div.x1yztbdb.x1n2onr6')
                for review in reviews:
                    reviewer_name = ""
                    is_exist = 0
                    reviews_lines = review.text.split("\n")
                    if "doesn't" in reviews_lines[0]:
                        reviewer_name = reviews_lines[0].split(" doesn't")[0]
                    else:
                        reviewer_name = reviews_lines[0].split(" recommend")[0]
                    # print(review.text)
                    try:
                        for reviewer in reviewer_name_array:
                            if reviewer == reviewer_name:
                                is_exist = 1
                        if is_exist == 0:
                            reviewer_name_array.append(reviewer_name)

                            if "doesn't" in reviews_lines[0]:
                                reviewer_recommend = "No"
                                review_date = reviews_lines[1]
                                print(reviewer_name + reviewer_recommend + review_date)
                                print(review.text.split("  ·")[1].split('Like')[0])
                                resturant_details_sheet.write(resturant_details_row, 0, name)
                                resturant_details_sheet.write(resturant_details_row, 1, reviewer_name)
                                resturant_details_sheet.write(resturant_details_row, 2,
                                                              review.text.split("  ·")[1].split('Like')[0])
                                resturant_details_sheet.write(resturant_details_row, 3, reviewer_recommend)
                                resturant_details_sheet.write(resturant_details_row, 4, review_date)
                                resturant_details_sheet.write(resturant_details_row, 5, index)
                                resturant_details_row = resturant_details_row + 1

                                reviewer_name_array.append(reviewer_name)
                            else:
                                reviewer_recommend = "Yes"
                                review_date = reviews_lines[1]
                                print(reviewer_name + reviewer_recommend + review_date)
                                print(review.text.split("  ·")[1].split('Like')[0])
                                resturant_details_sheet.write(resturant_details_row, 0, name)
                                resturant_details_sheet.write(resturant_details_row, 1, reviewer_name)
                                resturant_details_sheet.write(resturant_details_row, 2,
                                                              review.text.split("  ·")[1].split('Like')[0])
                                resturant_details_sheet.write(resturant_details_row, 3, reviewer_recommend)
                                resturant_details_sheet.write(resturant_details_row, 4, review_date)
                                resturant_details_sheet.write(resturant_details_row, 5, index)
                                resturant_details_row = resturant_details_row + 1
                                reviewer_name_array.append(reviewer_name)
                    except:
                        continue
                facebook.find_element(By.XPATH, "/html/body").send_keys(Keys.END)
       
        except:
            continue
      
    resturant_details.close()
except:
    resturant_details.close()

