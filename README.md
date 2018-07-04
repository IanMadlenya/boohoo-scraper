# boohoo-scraper
A scraper for products on the boohoo website, to extract the various static as well as dynamic elements using __BeautifulSoup__ and __Selenium__.
This is primarily for scraping the image of the models and the corresponding image of the article of clothing that the model is wearing.

## Brief
The initial script in both directories named `home_scrape.py` (can be found [here](dress-women/home_scrape.py)) is for scraping static elements. It extracts the URLs of each product from the home page
and enters them into a comma separated variables file. This is done by simply checking for html tags and respective classes of each of these html elements. Because of it's static nature, __BeautifulSoup__ has been utilized to perform this operation.

The [second file](dress-women/dress_scrape.py) in the respective directories is for extracting the URLs of the images in consideration, requesting for and finally downloading them. As these particular elements are loaded dynamically, the page is left to load fully for a certain amount of time. After which the XPath of these respective elements is used in order to extract the required URLs using __Selenium__, and finally download the images using __urllib__. Simultaneously, all these URLs are stored in respective CSV files for future use, if need be.
There are subtle changes between the code required for men > t-shirts and vests and women > dresses. This can be observed and modified accordingly for other categories by inspecting the html structure of the web page in consideration.

It will work for the structure of the website as of today (4th of July 2018).

## Getting the Web driver
One will require a web driver in order to run __Selenium__, as it aids in completely automating the browser's functions.
- I used the Google Chrome browser when I was working on this, and you can get the chrome driver at [chromedriver]( https://sites.google.com/a/chromium.org/chromedriver/)
- If you choose to use any other browser, check out [Selenium's downloads](https://www.seleniumhq.org/download/)

## Requirements
These are the modules and the versions that I have used in these scripts
```
selenium==3.13.0
requests==2.19.1
urllib3==1.22
XlsxWriter==1.0.4
lxml==4.2.1
html5lib==0.9999999
bs4==0.0.1
```

## Run the scripts
Make sure that you have a stable Internet connection, and then just run the following command after entering the respective directory:
```
python <file_name>.py
```
Make sure to make new folders with the same names as entered in the script (`urlretrieve` function call in the `get_image()` function), or give your own folder names and modify the script with the appropriate path. These folders will finally contain the images that will be scraped and downloaded from the web.

### Disclaimer
This has been written for purely educational purposes, and has no commercial usage whatsoever.
