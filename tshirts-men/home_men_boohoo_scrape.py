import requests as r
from bs4 import BeautifulSoup
import os

def name_scraper(url):
    i = 0
    fnames = []
    with open('file_names_shirt.csv', 'w') as file:
        while i < 14:
            url_temp = url + "?sz=80&start=" + str(80 * i)
            print(url_temp)

            req = r.get(url_temp)
            data = req.text
            soup = BeautifulSoup(data, "lxml")


            for div in soup.find_all('div', class_ = 'primary-content'):
                for li in div.find_all('li', class_ = 'grid-tile'):
                    for product in li.find_all('div', class_ = 'product-name'):
                        for file_name in product.find_all('a', class_ = 'name-link'):
                            file.write(file_name["href"])
                            file.write('\n')
                            fnames.append(file_name["href"])
            i += 1

    return fnames



if __name__ == '__main__':
    url = "http://www.boohoo.com/mens/t-shirts-vests"
    file_list = name_scraper(url)

    print("List of all the filenames:", file_list)
    print("Number of files", len(file_list))
