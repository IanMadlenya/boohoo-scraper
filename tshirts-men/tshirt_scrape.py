'''
Image scraper for boohoo.com

Scrapes dynamically loaded images of frontal pose of the model, plus only the
isolated image of the article of clothing.

Boohoo follows the pattern of the first image being the model, and the third being
the image of the dress (but there are a handful of exceptions)

Author: Rahul M Patil
'''
import os
from bs4 import BeautifulSoup
import requests as r
import csv
import urllib
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver

def loadFilenames(fname):
    files = []
    with open(fname, 'r') as file:
        names = csv.reader(file, delimiter="\n")
        for i, name in enumerate(names):
            files.append(name)

    return files

# to scrape dynamic content
def get_images(url, i, driver, model_csv, shirt_csv):
    # flag to decide whether the current product has enough images or not, use of this will become more clear below
    flag = 1
    driver.get(url)
    timeout = 10

    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="js-alt-images"]/li[1]')))
    except TimeoutException:
        print("Timed out\n")
        driver.quit()

    #soup = BeautifulSoup(page_html)

    # first image is model standing straight
    model = driver.find_elements_by_xpath('//*[@id="js-alt-images"]/li[1]/a')
    # third image is the isolated image of the dress
    cloth = driver.find_elements_by_xpath('//*[@id="js-alt-images"]/li[3]/a')
    #thumbs_list = [i.text for i in thumbs]

    # get the url for the model
    model_pic = model[0].get_attribute('href')

    # a case where only 2 images so second image is the isolated image of the dress
    if cloth == []:
        cloth = driver.find_elements_by_xpath('//*[@id="js-alt-images"]/li[2]/a')

    # the last case where there is only image of the model, and can be completely ignored
    if cloth == []:
        flag = 0

    print(cloth)

    if flag == 1:
        cloth_pic = cloth[0].get_attribute('href')   #get the url for the isolated cloth

        # the URLs are of the type 'http://i1.adis.ws/i/boohooamplience/dzz79295_navy_xl_2?$product_page_main_magic_zoom$'
        # but the part after the '?' can be omitted, and hence only 'http://i1.adis.ws/i/boohooamplience/dzz79295_navy_xl_2' is what we store and use
        q_mark = model_pic.find('?')
        model_pic = model_pic[:q_mark]

        q_mark = cloth_pic.find('?')
        cloth_pic = cloth_pic[:q_mark]

        #add model img url entry to csv file
        model_csv.write(model_pic)
        #add shirt img url entry to other csv file
        shirt_csv.write(cloth_pic)

        #new entry in csv file
        model_csv.write('\n')
        shirt_csv.write('\n')

        filename = 'p' + str(i) + '.jpg'

        #save models photo in model directory
        urllib.request.urlretrieve(model_pic, 'models\\' + filename)
        time.sleep(1)
        #save the shirts photo is the shirts directory
        urllib.request.urlretrieve(cloth_pic, 'shirts\\' + filename)




if __name__ == '__main__':
    fnames = loadFilenames('file_names_shirt.csv')
    i = 0
    chrome_driver = "chromedriver" #path to your chrome driver that you can download from the link provided in the README
    os.environ["webdriver.chrome.driver"] = chrome_driver
    web_driver = webdriver.Chrome(chrome_driver)

    #store the respective image urls in these csv files
    with open('models_images.csv', 'w') as m:
        with open('shirts_images.csv', 'w') as s:
            while i < len(fnames):
                #print(fnames[i])
                print(fnames[i])
                time.sleep(1)
                get_images(str(fnames[i][0]), i, web_driver, m, s)
                i += 1

    web_driver.quit()
