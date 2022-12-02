import requests

# Custom functions

# Browser related function
from functions import initbrowser
from functions import dealWithSplashPage
from functions import findPageLinks, checkNoNextPage, clickNextPage

# Getting the testimonials
from functions import getTestimonials

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
    stopEarly = 1

    ## Date in yyyy-mm-dd format
    date = datetime.now().strftime("%Y-%m-%d")

    # Open browser on home page
    browser = initbrowser(url_home)

    # Get rid of the splash page, if it is there
    dealWithSplashPage(browser, 2)

    # Get page body
    body = browser.find_element(By.XPATH, "//body")

    iIterations = 1
    # Main loop
    while True:

        # Get testimonials from a single page
        pageTestimonials = getTestimonials(browser, colNames=df.columns, firstPage=True)

        # Add to existing dataframe
        df = pd.concat([df, pageTestimonials])

        # Get next page
        pageLinks = findPageLinks(browser)
    
        # Get boolean to tell us whether this is the last page (whether we can find a 'next page')
        thisIsLastPage = checkNoNextPage(pageLinks)
        print(f"stopEarly = {stopEarly} and iIterations = {iIterations}")
        # If user wants to stop early
        if iIterations > stopEarly or thisIsLastPage:
            print("Stopping loop")
            break
        # Else, if not on last page
        elif not thisIsLastPage or iIterations > stopEarly:

            # Update count of iterations
            iIterations += 1

            # We can click the next page
            clickNextPage(browser, pageLinks)

    # Output to csv
    print("Let us save a text file with the data")
    df.to_csv('testimonials-{}.txt'.format(date), sep='|', index=False)
