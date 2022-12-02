from constants import MAC_CHROME_DRIVER
import time
from selenium.webdriver.common.by import By
import re
import pandas as pd



def initbrowser(url=None, hidebrowser=False):

    """
        Initialises browser to scrape web data
        returns object browser (driver) - selenium object.

        Only needs to be run once per session.#

        url: url to load up
        hidebrowser: Minimise browser if True

        Dependencies: Will require selenium to control a browser.
            This has been developed bsaed on Chrome.  Not sure if other browsers will work (they should!)

        Suggested improvements:
            - Ability for python to pick up an existing session

        Author: Andrew Craik
        Date:   2017/2018?
    """

    ## Import os, system
    import os 
    import sys

     
    #############################################
    ## Import selenium
    #############################################import time
    
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys

    ## Chrome options
    ## Source: https://stackoverflow.com/questions/43149534/selenium-webdriver-how-to-download-a-pdf-file-with-python

    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {
        #"download.default_directory": r"C:/Users/name/Desktop", #Change default directory for downloads
        "download.prompt_for_download": False, #To auto download the file
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
        })

    # What platform are we using?
    print(f"Running on {sys.platform}")

    ###############################################
    ## Linux 
    ###############################################
    
    ## If running on linux open up pyvirtualdisplay to open browser
    if sys.platform == 'linux':

        from pyvirtualdisplay import Display

        driver_path = r'/home/public/python/chrome/chromedriver'
        print("NOTE: Driver path for chrome set as '{}'\nThis is hard-coded in '{}'".format(driver_path, os.path.abspath(__file__)))
    
        
        
        disp_size = (1024, 768)
        display = Display(visible=0, size=disp_size)
        display.start()
        
        browser = webdriver.Chrome(driver_path, chrome_options=options)
    
    ###############################################
    ## Mac 
    ###############################################
       
    elif sys.platform == 'darwin':

        # What platf
        
        # Path for Selenium driver 
        browser_path = MAC_CHROME_DRIVER
        print(f"Open browser with URL '{url}'")
        browser = webdriver.Chrome(MAC_CHROME_DRIVER, chrome_options=options)

    ## Else, on windows - specify path
    else:
        #browser_path = "C:\\Program Files\\Python36\\selenium\\webdriver\\chrome\\chromedriver.exe"
        browser_path = os.environ['CHROME_DRIVER']
        sys.path.append(os.environ['CHROME_DRIVER'])
        print(f"Open browser with URL '{url}'")

        browser = webdriver.Chrome(os.environ['CHROME_DRIVER'], chrome_options=options)
        
    


    ##  hide browser
    if hidebrowser: 
        print("Hiding browser - current position (before moving)\n", browser.get_window_position())
        browser.set_window_position(0,10000)
    
    ## Get browser to webpage
    if url != None:
        browser.get(url)
    return browser

def dealWithSplashPage(browser, timesleep=5):

    """ Specific to everyone's invited

        Tries to close the splash page by selecting a cross (sqs-popup-overlay-close)
        If it can't be found - pass
    """

    # Give time for the page to load up
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

def findPageLinks(browser):


        """
            Find out whether the end of the page has:
                "Previous page" only,
                "Next page" only, or
                both of the above

        """

        # Go to bottom of page
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        time.sleep(2)
        while True:

            # print("Scroll up")
            browser.execute_script("window.scrollTo(0, window.scrollY - 300)")
            time.sleep(1)
            # Scroll up until you find 'Previous' or 'Next' page
            pageLinks = browser.find_elements(By.XPATH, "//a[contains(text(), 'Next Page')]")

            # Remove items with no text
            pageLinks = [p for p in pageLinks if(p.text!='')]

            if len(pageLinks) > 0:
                
                print(f"Text in pageLinks = {[p.text for p in pageLinks]}")
                return pageLinks


def scrollDown(driver):
    """Credit: https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python"""
    SCROLL_PAUSE_TIME = 1

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    #print(last_height)

    while True:
        # Scroll down to bottom
        #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.execute_script("window.scrollTo(0, window.scrollY + 1500)")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        #new_height = driver.execute_script("return document.body.scrollHeight")
        new_height = driver.execute_script("return window.scrollY")

        # Use this line to debug if the script is stuck on scrolling
        # print(f"New height = {new_height}, last height = {last_height}")

        # Check whether the current (new) height is the same as the previous (last)
        # When True, this suggests that the browser has reached the end of the page.
        if new_height == last_height:
            break
        else: 
            # Update previous (last) height
            last_height = new_height


# Get pages
def processSingleTestimonial(blue):

    """ A blue is a single 'blue' frame (cell) that holds a testimonial
        Returns a tuple (testimonial, estab) holding the text of the testimonial and the
            name of the establishment (this second element has since been removed from the website)
        
    """


    # Regex - get text between quotes
    # Optional quotes
    rgx_quote = re.compile("""(?<=")?.+(?=")?""")
    
    # Initialise text and establishment
    text = ''
    estab = ''

    # texts
    texts = blue.find_elements(By.XPATH, ".//p[@class='preFade fadeIn']")

    # If there is text
    if len(texts) > 0:

        # Testimonial (extract)
        text = texts[0].text

        if len(texts)>1:
            estab = texts[1].text
    
        # Append next testimonial to a list
        return text, estab
    else:
        return None, None

def getTestimonials(browser, colNames, firstPage=False):

    """ On a single browser page, scroll down collecting each testimonial
        Returns a pandas dataframe 

        Scrolls down to the end of the page and then processes each blue frame (a blue)

        stopEarly - Integer - stops processing page after N testimonials have been selected
                    Default -1

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

def checkNoNextPage(pageLinks):

    """ List of Selenium objects
        Return True if no 'next page' link to select
    """

    # Next page items
    npItems = [p for p in pageLinks if('Next' in p.text)]
    if len(npItems)>0:
        return False
    else:
        return True


def clickNextPage(browser, pageLinks):
    """ Not as simple as just clicking
        We need to locate and move browser to link
    """
    # Click next page
    nextPage = [p for p in pageLinks if ('Next Page' in p.text)][0]

    # Get location
    nextPageLoc = nextPage.location
    
    # Move browser to that location
    browser.execute_script(f"window.scrollTo(0, {nextPageLoc['y']})")
    nextPage.click()
