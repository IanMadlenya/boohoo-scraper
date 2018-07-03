import requests as r
from bs4 import BeautifulSoup
import os

def name_scraper(url):
    i = 0
    fnames = []
    with open('file_names_dress.csv', 'w') as file:
        #no. of pages = 42, as of today there are 42 pages of 80 products each in the category of male: dresses
        while i < 42:
            url_temp = url + "?sz=80&start=" + str(80 * i)
            print(url_temp)

            req = r.get(url_temp)
            data = req.text
            soup = BeautifulSoup(data, "lxml")

            #a simple brute force approach to extract the final 'a' tag that contains the url of each product page
            for div in soup.find_all('div', class_ = 'primary-content'):
                for li in div.find_all('li', class_ = 'grid-tile'):
                    for product in li.find_all('div', class_ = 'product-name'):
                        for name in product.find_all('a', class_ = 'name-link'):
                            file.write(name["href"])
                            file.write('\n')
                            fnames.append(name["href"])
            i += 1

    return fnames



if __name__ == '__main__':
    #the base url for the for the catoegory of women > dresses
    url = "http://www.boohoo.com/womens/dresses"
    file_list = name_scraper(url)

    print("List of all the filenames:", file_list)
    print("Number of files", len(file_list))
