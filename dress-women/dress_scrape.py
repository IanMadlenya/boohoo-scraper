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
import cv2
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

def get_images(url, i, driver, model_csv, shirt_csv):
    #to scrape dynamic content
    flag = 1
    driver.get(url)
    timeout = 50

    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="js-alt-images"]/li[1]')))
    except TimeoutException:
        print("Timed out\n")
        driver.quit()

    #soup = BeautifulSoup(page_html)
    time.sleep(1)
    model = driver.find_elements_by_xpath('//*[@id="js-alt-images"]/li[1]/a') #first image is model standing straight
    cloth = driver.find_elements_by_xpath('//*[@id="js-alt-images"]/li[3]/a') #third image is the isolated image of the dress
    #thumbs_list = [i.text for i in thumbs]
    model_pic = model[0].get_attribute('href')   #get the url for the model

    if cloth == []:
        cloth = driver.find_elements_by_xpath('//*[@id="js-alt-images"]/li[2]/a') #a case where only 2 images so second image is the isolated image of the dress

    if cloth == []:  # the last case where there is only image of the model, and can be completely ignored
        flag = 0

    if flag == 1:
        cloth_pic = cloth[0].get_attribute('href')   #get the url for the isolated cloth

        q_mark = model_pic.find('?')
        model_pic = model_pic[:q_mark]

        q_mark = cloth_pic.find('?')
        cloth_pic = cloth_pic[:q_mark]

        model_csv.write(model_pic)  #add model img url entry to csv file
        shirt_csv.write(cloth_pic)  #add shirt img url entry to other csv file

        model_csv.write('\n')  #new entry in csv file
        shirt_csv.write('\n')  #new entry in csv file

        filename = 'p' + str(i) + '.jpg'

        urllib.request.urlretrieve(model_pic, 'female_dress_boohoo_dress\\' + filename) #save models photo in model directory
        time.sleep(1)
        urllib.request.urlretrieve(cloth_pic, 'female_models_boohoo_dress\\' + filename) #save the shirts photo is the shirts directory




if __name__ == '__main__':
    fnames = loadFilenames('file_names_dress.csv')
    i = 2052
    chrome_driver = "chromedriver"
    os.environ["webdriver.chrome.driver"] = chrome_driver
    web_driver = webdriver.Chrome(chrome_driver)

    with open('models_images.csv', 'w') as m:
        with open('dress_images.csv', 'w') as s:
            while i < len(fnames):
                #print(fnames[i])
                print(fnames[i])
                time.sleep(1)
                get_images(str(fnames[i][0]), i, web_driver, m, s)
                i += 1

    web_driver.quit()
