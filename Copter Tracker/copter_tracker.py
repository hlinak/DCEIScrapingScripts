import os, time, sys, traceback

import sqlite3

from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from subprocess import CREATE_NO_WINDOW

from bs4 import BeautifulSoup

dbconn = None
folder = r"""\\ddoefile01\AQDDATA2\Air Quality Planning Branch\Emission Inventories & Modeling\Mobile Nonroad and MAR Source EIs\Copter Tracker"""

browser = None
url = r"""https://globe.adsbexchange.com/?lat=38.9072&lon=-77.0369&zoom=12"""

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
        "Accept-Encoding": "*",
        "Connection": "keep-alive",
        "Referrer": "https://globe.adsbexchange.com/?lat=38.9072&lon=-77.0369&zoom=12"
    }

try:
    sql_database = folder +  r"""\copters.sqlite"""
    dbconn = sqlite3.connect(sql_database)
    if(not os.path.isfile(sql_database)):
        dbconn.execute("""CREATE TABLE copters
            (datetime DATETIME,
            hex_id TEXT NOT NULL COLLATE NOCASE,
            callsign TEXT NOT NULL COLLATE NOCASE,
            registration TEXT,
            type TEXT,
            alt REAL,
            speed REAL,
            lat REAL,
            lon REAL,
            PRIMARY KEY (datetime, hex_id, callsign),
            UNIQUE (datetime, hex_id, callsign));""")
        dbconn.commit()
            
    chrome_options = Options()  
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--window-size=1920,1030")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = os.path.abspath(r"""chrome-win\chrome.exe""")
    
    chrome_service = Service()
    #chrome_service.creationflags = CREATE_NO_WINDOW

    browserLoad = False
    i = 0
    while(not browserLoad and i < 10):
        try:
            browser = webdriver.Chrome(service=chrome_service,
                               options=chrome_options)
            browserLoad = True
        except:
            browserLoad = False
            i = i+1
    
    browser.get(url)
    
    #
    #browser.find_element(By.ID,"filters_description").submit()


    
##    for cookie in browser.get_cookies():
##        print(cookie)
##        
##    #browser.add_cookie({"name" : "adsbx_sid", "value" : "1671895873212_5xzwxpnuli5", "domain" : "globe.adsbexchange.com" })
##    browser.add_cookie({"name" : "adsbx_sid",
##                        "value" : "1671895873212_5xzwxpnuli5",
##                        "domain" : "globe.adsbexchange.com"})
##    #browser.add_cookie({"name" : "__cflb", "value" : "0H28vD1xVAZ2uKaiRDWQ17dG4WLv4fj6gCoV929Az9M", "domain" : "globe.adsbexchange.com"})
##    browser.add_cookie({"name" : "__cflb", "value" :
##                        "0H28vD1xVAZ2uKaiRDWQ17dG4WLv4fj6gCoV929Az9M",
##                        "domain" : "globe.adsbexchange.com"})
    

    browser.get(url)
    time.sleep(2)
    #browser.find_element(By.ID,"column_registration_cb").click()
    
    
    browser.execute_script("arguments[0].click()",
                       browser.find_element(By.ID,"column_registration_cb"))
    browser.execute_script("arguments[0].click()",
                       browser.find_element(By.ID,"column_flag_cb"))
    browser.execute_script("arguments[0].click()",
                       browser.find_element(By.ID,"column_lat_cb"))
    browser.execute_script("arguments[0].click()",
                       browser.find_element(By.ID,"column_lon_cb"))
    browser.execute_script("arguments[0].click()",
                       browser.find_element(By.ID,"column_wd_cb"))
    browser.execute_script("arguments[0].click()",
                       browser.find_element(By.ID,"column_ws_cb"))
    browser.execute_script("arguments[0].value = 'H..'",
                       browser.find_element(By.ID,"filters_description_input"))
    browser.execute_script("arguments[0].click()",
                        browser.find_element(By.ID,"filters_description").find_element(By.XPATH, './/button'))
    
    time.sleep(10)
    while(int(time.strftime("%M%S")) < 5955):
        #print(int(time.strftime("%M%S")))
        #print(browser.find_element(By.ID,"filters_description_input").get_attribute("value"))
        #print(browser.find_element(By.ID,"column_lat_cb").get_attribute('class'))
        #print(browser.find_element(By.ID,"planesTable").get_property('outerHTML'))
        soup = BeautifulSoup(browser.find_element(By.ID,"planesTable").get_property('outerHTML'), 'html.parser')
        for table in soup.find_all("table", id="planesTable"):
            for tr in table.find_all("tr"):
                tds = tr.find_all("td")
                if(tds[0].encode_contents().decode("utf-8") != 'Hex ID'):
                    #print((tds[0].encode_contents().decode("utf-8"), tds[1].encode_contents().decode("utf-8"),tds[2].encode_contents().decode("utf-8"), tds[3].encode_contents().decode("utf-8"), tds[4].encode_contents().decode("utf-8"), tds[5].encode_contents().decode("utf-8"), tds[6].encode_contents().decode("utf-8"), tds[7].encode_contents().decode("utf-8")))
                    dbconn.execute("""INSERT INTO copters (datetime, hex_id, callsign, registration, type, alt, speed, lat, lon)
                        SELECT datetime('now', 'localtime'), ?, ?, ?, ?, ?, ?, ?, ?""",
                        (tds[0].encode_contents().decode("utf-8"), tds[1].encode_contents().decode("utf-8"),tds[2].encode_contents().decode("utf-8"), tds[3].encode_contents().decode("utf-8"), tds[4].encode_contents().decode("utf-8"), tds[5].encode_contents().decode("utf-8"), tds[6].encode_contents().decode("utf-8"), tds[7].encode_contents().decode("utf-8")))
            dbconn.commit()
        time.sleep(2)
        
    dbconn.close()
            
    browser.stop_client()
    browser.close()
    browser.quit()

except Exception as e:
    logfile = open("error_log_"+str(time.time())+".txt", 'w')
    exc = sys.exc_info()[0]
    stack = traceback.extract_stack()[:-1]  # last one would be full_stack()
    trc = 'Traceback (most recent call last):\n'
    stackstr = trc + ''.join(traceback.format_list(stack))
    if exc is not None:
         stackstr += '  ' + traceback.format_exc().lstrip(trc)
    print(stackstr, file = logfile)
    logfile.close()

    if(browser):
        browser.stop_client()
        browser.close()
        browser.quit()
    if(dbconn):
        dbconn.close()

