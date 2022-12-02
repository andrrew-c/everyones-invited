import requests

# Custom functions
from functions import initbrowser, findPageLinks, getTestimonials
from functions import dealWithSplashPage

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from datetime import datetime
import time

import pandas as pd


import re

if __name__ == "__main__":
        
    #url_home = "https://www.everyonesinvited.uk/"
    url_home = "https://www.everyonesinvited.uk/read"

    # Init DF
    df = pd.DataFrame(data=None, columns='text,establishment,url'.split(','))

    # Stop after n iterations
    stopEarly = 3

    ## Date in yyyy-mm-dd format
    date = datetime.now().strftime("%Y-%m-%d")

    # Open browser on home page
    browser = initbrowser(url_home)

    # Get rid of the splash page, if it is there
    dealWithSplashPage(browser, 2)

    # Get page body
    body = browser.find_element(By.XPATH, "//body")

    iIterations = 0
    # Main loop
    # while True:

    # Get next page
    pageLinks = findPageLinks(browser)

    # Get testimonials from a single page
    # pageTestimonials = getTestimonials(browser, colNames=df.columns, firstPage=True)

    # Add to existing dataframe
    # df = pd.concat([df, pageTestimonials])
   
    # This is the last page?
    thisIsLastPage = checkNoNextPage(pageLinks)

    if not thisIsLastPage:
        # We can click the next page
        clickNextPage()
    # Else, we have reached the last page
    else:
        # We leave the loop
        break



    # Click next page
    # if len(nextPage)==1:
    #     nextPage[0].click()

    # break

    # Output to csv
    # print("Let us save a text file with the data")
    # df.to_csv('testimonials-{}.txt'.format(date), sep='|', index=False)
