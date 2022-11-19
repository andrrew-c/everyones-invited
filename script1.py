import requests

# Custom functions
from functions import initbrowser, findPageLinks

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

    def scrollDown(driver):
        """Credit: https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python"""
        SCROLL_PAUSE_TIME = 1

        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")
        #print(last_height)

        while True:
            # Scroll down to bottom
            #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            browser.execute_script("window.scrollTo(0, window.scrollY + 1500)")
            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            #new_height = driver.execute_script("return document.body.scrollHeight")
            new_height = driver.execute_script("return window.scrollY")
            #print(new_height)
            if new_height == last_height:
                break
            last_height = new_height


    # Get pages
    #pages = browser.find_elements_by_xpath("//a[contains(@href, 'read-test')]")
    #pages = [p for p in pages if p.text != '']

    pages = findPageLinks(browser)
    print("Sleep 2")
    time.sleep(2)

    
    # Iterate through all pages
    for i in range(len(pages)):

        # If url already in df - pass
        if len(df.query("url=='{}'".format(pages[i]))) > 0:
            pass

        # Else, new URL - process it
        else:
                
            # If first page we don't need to click
            if i>0:
                print("Loading page {}".format(pages[i]))
                browser.get(pages[i])

            # Else, Page 0 (1) go to top
            else:
                print("First page = {}, need to get testimonials".format(i))
                print("\tGo to top of page")

                # Top of page and wait
                browser.execute_script("window.scrollTo(0, 0)")
                time.sleep(1.5)
                #ch = input("Continue?")


            # Scroll through page so testimonials load up
            scrollDown(browser)

            # Get testimonials - in blue frames
            blues = browser.find_elements(By.XPATH, "//div[@class='sqs-block-content']")

            print("\tGetting testimonials")
            # For each cell - get testimonial
            for b in blues:
                text = ''
                estab = ''
                
                # texts
                texts = b.find_elements(By.XPATH, ".//p[@class='preFade fadeIn']")
                if len(texts) > 0:
                    # Testimonial
                    text = texts[0].text

                    if len(texts)>1:
                        estab = texts[1].text
                
                    df = df.append(pd.DataFrame(data=[[text,estab,pages[i]]], columns=df.columns))
            time.sleep(1)        
            print(df.shape)
            
    # Reset index
    df = df.reset_index()

    # Output to csv
    print("Let us save a text file with the data")
    df.to_csv('testimonials-{}.txt'.format(date), sep='|', index=False)
