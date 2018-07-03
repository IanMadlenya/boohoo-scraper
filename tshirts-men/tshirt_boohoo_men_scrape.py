'''
Image scraper for boohoo.com

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
    #pure html approach that didnt work for boohoo.com as the images are dynamically rendered
    # url_temp = url.replace("\n", "")
    # req = r.get(url_temp)
    # data = req.text
    # soup = BeautifulSoup(data, "lxml")
    #
    # print(soup.prettify())
    #
    # for div in soup.find_all('div', class_ = "primary-content"):
    #     for div_main in div.find_all('div', class_ = "pdp-main"):
    #         for div_cont in div_main.find_all('div', class_ = "product-image-container"):
    #             for div_product in div_cont.find_all('div', class_ = "product-thumbnails-container"):
    #                 print(div_product.prettify())


    #attempt to scrape dynamic content
    flag = 1
    driver.get(url)
    timeout = 10

    try:
        WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="js-alt-images"]/li[1]')))
    except TimeoutException:
        print("Timed out\n")
        driver.quit()

    #soup = BeautifulSoup(page_html)

    model = driver.find_elements_by_xpath('//*[@id="js-alt-images"]/li[1]/a') #first image is model standing straight
    cloth = driver.find_elements_by_xpath('//*[@id="js-alt-images"]/li[3]/a') #third image is the isolated image of the dress
    #thumbs_list = [i.text for i in thumbs]
    model_pic = model[0].get_attribute('href')   #get the url for the model

    if cloth == []:
        cloth = driver.find_elements_by_xpath('//*[@id="js-alt-images"]/li[2]/a') #a case where only 2 images so second image is the isolated image of the dress

    if cloth == []:  # the last case where there is only image of the model, and can be completely ignored
        flag = 0

    print(cloth)

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

        urllib.request.urlretrieve(model_pic, 'models\\' + filename) #save models photo in model directory
        urllib.request.urlretrieve(cloth_pic, 'shirts\\' + filename) #save the shirts photo is the shirts directory




if __name__ == '__main__':
    fnames = loadFilenames('file_names_shirt.csv')
    i = 937
    chrome_driver = "chromedriver"
    os.environ["webdriver.chrome.driver"] = chrome_driver
    web_driver = webdriver.Chrome(chrome_driver)

    with open('models_images.csv', 'w') as m:
        with open('shirts_images.csv', 'w') as s:
            while i < len(fnames):
                #print(fnames[i])
                print(fnames[i])
                get_images(str(fnames[i][0]), i, web_driver, m, s)
                i += 1

    web_driver.quit()
