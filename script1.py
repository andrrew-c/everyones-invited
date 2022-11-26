import requests

# Custom functions
from functions import initbrowser, findPageLinks, scrollDown

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

    def getTestimonials(browser, colNames, firstPage=False):

        """ On a single browser page, scroll down collecting each testimonial
            Returns a pandas dataframe 

            Scrolls down to the end of the page and then processes each blue frame (a blue)

        """

        # Initialise list of dataframe rows
        dfs = []

        # 
        if not firstPage:
            print("Not first page")
        
        # First page
        else:

            # Print message
            print("First page: Go to top of page")
            browser.execute_script("window.scrollTo(0, 0)")
            time.sleep(1.5)

        # Scroll down entire page, loading up testimonials
        print(f"Scrolling page: {browser.current_url}")
        scrollDown(browser)

        # Get testimonials - in blue frames
        blues = browser.find_elements(By.XPATH, "//div[@class='sqs-block-content']")
        

        # For each (blue) cell - get testimonial
        for blue in blues:

            # Process a single blue frame, looking for testimonials
            testimonial, estab = processSingleTestimonial(blue)

            # If a testimonial was returned, add it to the list
            if testimonial is not None: 
                dfs.append([testimonial, estab, browser.current_url])

            
        # Produce dataframe from list
        df = pd.DataFrame(data=dfs, columns=colNames)
        return df

    # Main loop
    do while True:

        # Get testimonials from a single page
        pageTestimonials = getTestimonials(browser, colNames=df.columns, firstPage=True)

        # Add to existing dataframe
        df = pd.concat([df, pageTestimonials])

        # Get next page
        nextPage = findPageLinks(browser)

    # Output to csv
    # print("Let us save a text file with the data")
    # df.to_csv('testimonials-{}.txt'.format(date), sep='|', index=False)
