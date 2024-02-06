import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import xlsxwriter
import csv
import xlrd
import getpass
import os 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
import pickle
import re

username = getpass.getuser()

if username == 'Home':
    os.chdir('C:/Users/Home/Dropbox/PRA/')
if username == 'zarnaab.ather':
    os.chdir('C:/Users/zarnaab.ather/Dropbox/PRA/')
if username == 'shaezal.cheema':
    os.chdir('C:/Users/shaezal.cheema/Dropbox/PRA/')
if username == 'TLS':
    os.chdir('C:/Users/TLS/Desktop/')

resturants_list = []

with open(r"Web Scraping\\Output\\Facebook\\AllLinks.csv", 'r') as file:
  csvreader = csv.reader(file)
  for row in csvreader:
      resturants_list.append(row[1])




restaurant_details = xlsxwriter.Workbook('Web Scraping\\Output\\Facebook\\RestaurantsInformation.xlsx')
restaurant_details_sheet = restaurant_details.add_worksheet()
restaurant_details_row = 1


restaurant_details_sheet.write(0, 0, 'Name')
restaurant_details_sheet.write(0, 1, 'Timings')
restaurant_details_sheet.write(0, 2, 'Phone Number')
restaurant_details_sheet.write(0, 3, 'Email')
restaurant_details_sheet.write(0, 4, 'Services')
restaurant_details_sheet.write(0, 5, 'Creation Date')
restaurant_details_sheet.write(0, 6, 'Intro')
restaurant_details_sheet.write(0, 7, 'Page ID')
restaurant_details_sheet.write(0, 8, 'Date(When it was Scraped)')
restaurant_details_sheet.write(0, 9, 'Address')
restaurant_details_sheet.write(0, 10, 'Restaurant Type')
restaurant_details_sheet.write(0, 11, 'Restaurant Followers')
restaurant_details_sheet.write(0, 12, 'Restaurant Likes')
restaurant_details_sheet.write(0, 13, 'Restaurant Rating')
restaurant_details_sheet.write(0, 14, 'No of dollar sign')
restaurant_details_sheet.write(0, 15, 'Latitude')
restaurant_details_sheet.write(0, 16, 'Longitude')
restaurant_details_sheet.write(0, 17, 'Social Media Link')
restaurant_details_sheet.write(0, 18, 'Website')
restaurant_details_sheet.write(0, 19, 'Check ins')


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
 

for url in resturants_list[801:]:
  

    facebook.get(url)


    time.sleep(3)

    # Add Name
    try:
        facebook.find_element(By.CSS_SELECTOR, 'div[aria-label="Close"] i').click()
    except:
        print("")
    try:
        name_folowers_likes = facebook.find_element(By.CSS_SELECTOR, 'div.x1e56ztr.x1xmf6yo span[dir="auto"]')
    except Exception as e:
        print(e)
    try:
        other_information = facebook.find_elements(By.CSS_SELECTOR, 'ul > div.x9f619')
    except Exception as e:
        print(e)
    try:   
        name = name_folowers_likes.text
    except:
        name = ""

    #Add Intro
    try:
        intro = facebook.find_element(By.CSS_SELECTOR, 'div.xieb3on > div:nth-child(1) > div > div > span').text
    except:
        intro = ""

    if "pages" in url:

        contact = ""
        address = ""
        email = ""
        website = ""
        social_media = ""
        price_range = ""
        ratings = ''
        services = ""
        latitude = ""
        longitude = ""
        creation_date = ""
        page_id = ""
        likes = ""
        followers = ""
        restaurant_type = ""
        checkins = ""

          
        try:
            about_list = facebook.find_elements(By.CSS_SELECTOR, "div.x78zum5 .xdt5ytf .x5yr21d")
            for about in about_list: 
                pattern = re.search(r"([\d,]+)\speople like this\n([\d,]+)\speople follow this\n([\d,]+)\speople checked in here", about.text)
                if pattern:
                    likes = int(pattern.group(1).replace(",", ""))
                    followers = int(pattern.group(2).replace(",", ""))
                    checkins = int(pattern.group(3).replace(",", ""))
                elif re.search('.*\$', about.text):
                    price_range = re.sub(r'[^\$]', '', about.text)
                elif re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', about.text):
                    email = about.text
                elif re.search(r'^(?!.*(?:twitter|facebook|instagram|linkedin)).*(?:https?://)?(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:\/\S*)?$', about.text):
                    website = about.text     
                elif re.search(r'\b(?:https?://)?(?:www\.)?(?:facebook|twitter|instagram|linkedin)\.\S+', about.text):
                    social_media = about.text
                elif "Food & Beverage" in about.text:
                    restaurant_type = about.text
                elif "Restaurant" in about.text:
                    restaurant_type = about.text
                elif "Local Business" in about.text:
                    restaurant_type = about.text
                elif re.compile(r".*Lahore.*"):
                    address = about.text
                elif re.compile(r"\(042\)\s\d{7}"):
                    contact = about.text
                    
        except Exception as e:
            print(e)

        try:
            main_div = facebook.find_elements(By.CSS_SELECTOR, 'div[style*="background-image"]') 
            style = main_div[0].get_attribute('style')
            match = re.search(r'center=(-?\d+\.\d+)%2C(-?\d+\.\d+)', style)

            if match:
                latitude = match.group(1)
                longitude = match.group(2)
            else:
                latitude = ""
                longitude = ""
            
        except:
            latitude = ""
            longitude = ""
    else:
    #Add Contact
        contact = ""
        address = ""
        email = ""
        website = ""
        social_media = ""
        price_range = ""
        ratings = ''
        services = ""
        latitude = ""
        longitude = ""
        creation_date = ""
        page_id = ""
        likes = ""
        followers = ""
        restaurant_type = ""
        checkins = ""

  
        if len(url.split("profile.php")) > 1:
            facebook.get(url.split("&")[0] + "/about")
        else:
            if url.split("?")[0][-1] == '/':
                facebook.get(url.split("?")[0] + "about")
            else:
                facebook.get(url.split("?")[0] + "/about")

        try:
            restaurant_type = facebook.find_element(By.CSS_SELECTOR, 'div.x1gan7if div.xat24cr div.x9f619 div.xzsf02u span.x193iq5w').text
        except:
            restaurant_type = ""

        try:
            contact_info = facebook.find_element(By.CSS_SELECTOR, 'div.x1gan7if')
            info_list = contact_info.text.split('\n')
        
        except:
            info_list = ""

    

        for info in info_list:
            if "Mobile" in info:
                contact = info_list[info_list.index(info) - 1]
            elif "Address" in info:
                address = info_list[info_list.index(info) - 1]
            elif re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', info):
                email = info
            elif re.search(r'^(?!.*(?:twitter|facebook|instagram|linkedin)).*(?:https?://)?(?:www\.)?[a-zA-Z0-9-]+\.[a-zA-Z]{2,}(?:\/\S*)?$', info):
                website = info
            elif re.search(r'\b(?:https?://)?(?:www\.)?(?:facebook|twitter|instagram|linkedin)\.\S+', info):
                social_media = info
            elif "Price Range" in info:
                price_range = re.sub(r'[^\$]', '', info)
            elif re.search(r'^(Not yet rated|\d+(\.\d+)?)\s*\((\d+)\s*Reviews?\)$', info):
                ratings = info
            elif "Services" in info:
                services = info_list[info_list.index(info) - 1]
        
        try:
            main_div = facebook.find_elements(By.CSS_SELECTOR, 'div[style*="background-image"]') 
            style = main_div[0].get_attribute('style')
            match = re.search(r'center=(-?\d+\.\d+)%2C(-?\d+\.\d+)', style)

            if match:
                latitude = match.group(1)
                longitude = match.group(2)
            else:
                latitude = ""
                longitude = ""
                
        except:
            latitude = ""
            longitude = ""
    
        
        if len(url.split("profile.php")) > 1:
            facebook.get(url.split("&")[0] + "/about_profile_transparency")
        
        else:
            if url.split("?")[0][-1] == '/':
                facebook.get(url.split("?")[0] + "about_profile_transparency")
            else:
                facebook.get(url.split("?")[0] + "/about_profile_transparency")

        time.sleep(5)
        try:
            page_transparency = facebook.find_elements(By.CSS_SELECTOR, 'div.x1iyjqo2')
        
            page_transparency_list = []
            page_transparency_list_final = []

            for page in page_transparency:
                page_transparency_list.append(page.text.split('\n'))

            for each in page_transparency_list:
                for item in each:
                    if item != '':
                        page_transparency_list_final.append(item)

            page_transparency_list_final = list(set(page_transparency_list_final))


            for info in page_transparency_list_final:
                if re.search(r'(?:January|February|March|April|May|June|July|August|September|October|November|December)\s\d{1,2},\s\d{4}', info):
                    creation_date = info
                elif re.search(r'\d{15}', info):
                    page_id = info
                else:
                    match = re.search(r'(\d+K?) likes • (\d+K?) followers', info)
                    if match:
                        likes = match.group(1)
                        followers = match.group(2)
        except:
            creation_date = ""
            page_id = ""
            likes = ""
            followers = ""


    restaurant_details_sheet.write(restaurant_details_row, 0, name)
    restaurant_details_sheet.write(restaurant_details_row, 2, contact)
    restaurant_details_sheet.write(restaurant_details_row, 3, email)
    restaurant_details_sheet.write(restaurant_details_row, 4, services)
    restaurant_details_sheet.write(restaurant_details_row, 5, creation_date)
    restaurant_details_sheet.write(restaurant_details_row, 6, intro)
    restaurant_details_sheet.write(restaurant_details_row, 7, page_id)
    restaurant_details_sheet.write(restaurant_details_row, 8, time.strftime("%Y-%m-%d %H:%M:%S"))
    restaurant_details_sheet.write(restaurant_details_row, 9, address)
    restaurant_details_sheet.write(restaurant_details_row, 10, restaurant_type)
    restaurant_details_sheet.write(restaurant_details_row, 11, followers)
    restaurant_details_sheet.write(restaurant_details_row, 12, likes)
    restaurant_details_sheet.write(restaurant_details_row, 13, ratings)
    restaurant_details_sheet.write(restaurant_details_row, 14, price_range)
    restaurant_details_sheet.write(restaurant_details_row, 15, latitude)
    restaurant_details_sheet.write(restaurant_details_row, 16, longitude)  
    restaurant_details_sheet.write(restaurant_details_row, 17, social_media)
    restaurant_details_sheet.write(restaurant_details_row, 18, website)
    restaurant_details_sheet.write(restaurant_details_row, 19, checkins)


    restaurant_details_row += 1

   
restaurant_details.close()




        


