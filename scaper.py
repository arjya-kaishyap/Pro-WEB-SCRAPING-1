from operator import imod
from re import A
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import requests

START_URL = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
browser = webdriver.Chrome("chromedriver")
browser.get(START_URL)
time.sleep(10)
headers = ["name","distance","mass","radius"]
star_data = []

def scrape():

    for i  in range(1,5):
         while True:
            time.sleep(2)
            soup = BeautifulSoup(browser.page_source,"html.parser")
            #check page no 
            current_page_num = int(soup.find_all("input",attrs = {"class","page_num"})[0].get("value"))
            if current_page_num<i :
                browser.find_element(By.XPATH, value = '//*[@id="mw-content-text"]/div[1]/table/thead/tr').click()
            elif current_page_num>i :
                browser.find_element(By.XPATH, value = '//*[@id="mw-content-text"]/div[2]/table/thead/tr').click()
            else:
                break    
            for ul_tag in soup.find_all("ul",attrs = {"class","stars"}):
                tr_tags = ul_tag.find_all("tr")
                temp_list = []
            for index,tr_tag in enumerate(tr_tags):
                if index == 0:
                    temp_list.append(tr_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(tr_tag.contents[0])
                    except:
                        temp_list.append("")
            star_data.append(temp_list)
            WebDriverWait(browser,20).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="mw-content-text"]/div[1]/table/thead/tr'))).click()
    #with open("scrapper2.csv","w") as f:
        #csvwriter = csv.writer(f)
        #csvwriter.writerow(headers)
        #csvwriter.writerows(star_data)

scrape()
new_stars_data =[]
def scrape_more_data(hyperlink) :
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content,"html.parser")
        temp_list = []
        for tr_tag in soup.find_all("tr",attrs = {"class": "fact_row"}) :
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags :
                try:
                    temp_list.append(td_tag.find_all("div",attrs = {"class": "value"})[0].contents[0])
                except:
                    temp_list.append("")
        new_stars_data.append(temp_list)
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)

for index,data in enumerate(star_data):
    scrape_more_data(data[5])
    print(f"scraping at {index + 1} is completed")
print(new_stars_data[0:10])

final_stars_data = []
for index,data in enumerate(star_data):
    new_stars_data_element = new_stars_data[index]
    new_stars_data_element = [elem.replace("\n","")for elem in new_stars_data_element]
    new_stars_data_element = new_stars_data_element[:7]
    final_stars_data.append(data + new_stars_data_element)

with open ("final.csv","w") as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(final_stars_data)