import requests

# Custom functions
from functions import initbrowser, findPageLinks, getTestimonials

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from datetime import datetime
import time

import pandas as pd


import re

if __name__ == "__main__":
        
    #url_home = "https://www.everyonesinvited.uk/"
    url_home = "https://www.everyonesinvited.uk/read"

    ## Date in yyyy-mm-dd format
    date = datetime.now().strftime("%Y-%m-%d")

    # Open browser on home page
    browser = initbrowser(url_home)

    # Sleep while browser loads
    timesleep = 5
    for i in range(timesleep):
        print(f"Sleep: {i} of {timesleep}")
        time.sleep(1)


    try:
        # Click away splash page
        btn_splash = browser.find_element(By.XPATH, "//a[@class='sqs-popup-overlay-close']")
        print("Closing splash screen")
        # Click it
        btn_splash.click()
    except:
        pass

    # Get page body
    body = browser.find_element(By.XPATH, "//body")

    # Init DF
    df = pd.DataFrame(data=None, columns='text,establishment,url'.split(','))

    # Stop after n iterations
    stopEarly = 3
    # Main loop
    while True:

        # Get testimonials from a single page
        pageTestimonials = getTestimonials(browser, colNames=df.columns, firstPage=True)

        # Add to existing dataframe
        df = pd.concat([df, pageTestimonials])

        # Get next page
        nextPage = findPageLinks(browser)

    # Output to csv
    # print("Let us save a text file with the data")
    # df.to_csv('testimonials-{}.txt'.format(date), sep='|', index=False)
