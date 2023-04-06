import os, time, sys

from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from subprocess import CREATE_NO_WINDOW

cwd = os.getcwd()

chrome_options = Options()  
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("--window-size=1920,1030")
chrome_options.add_argument("--disable-dev-shm-usage")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--disable-features=NetworkService")
chrome_options.binary_location = os.path.abspath(r"""chrome-win\chrome.exe""")
#chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])

#if platform.node() == 'DNR-5W53JL2':
#    
#    chromedriver_path = r"""E:\exceedance_report\google_traffic_map\chromedriver_win32\chromedriver.exe"""
#elif platform.node() == 'pcp263559pcs.dnr.state.ga.us':
#    chrome_options.binary_location = r"""/usr/bin/google-chrome-stable"""
#    chromedriver_path = r"""/mnt/local_data_disk/google_traffic_map/chromedriver"""
#else:
#    sys.exit("For now, this code only works on BK's desktop or the DMU's workstation!!!")

chrome_service = Service()
chrome_service.creationflags = CREATE_NO_WINDOW
browser = webdriver.Chrome(service=chrome_service,
                           options=chrome_options)

google_traffic_sites = [['https://www.google.com/maps/@38.921895,-77.013225,11z/data=!5m1!1e1', 'msa'],
                       ['https://www.google.com/maps/@38.9467487,-77.021343,13.46z/data=!5m1!1e1', 'dc_north'],
                       ['https://www.google.com/maps/@38.8479509,-77.021343,13.46z/data=!5m1!1e1', 'dc_south']]

for google_traffic_site in google_traffic_sites:
    browser.get(google_traffic_site[0])
    #interval = 60 # minutes
    screenshotDir = os.path.abspath(r"""\\ddoefile01\AQDDATA2\Air Quality Planning Branch\Emission Inventories & Modeling\Mobile Onroad Source EIs\GoogleTrafficPython\screenshots""")
    currentTime = time.localtime()
    filename = google_traffic_site[1] + '_%s.png' % time.strftime("%Y%m%d_%H%M%S", currentTime)
    screenshot_path = os.path.join(screenshotDir, filename)
    browser.save_screenshot(screenshot_path)

#
# Need to close the Chrome instance; otherwise, it will eat up all computing resources and eventually crashes. See error messages below
#
#Traceback (most recent call last):
  # File "/mnt/local_data_disk/google_traffic_map/get_google_traffic_map_once.py", line 20, in <module>
    # browser = webdriver.Chrome(executable_path=os.path.abspath(chromedriver_path), chrome_options=chrome_options)
  # File "/home/bkim/anaconda3/lib/python3.6/site-packages/selenium/webdriver/chrome/webdriver.py", line 75, in __init__
    # desired_capabilities=desired_capabilities)
  # File "/home/bkim/anaconda3/lib/python3.6/site-packages/selenium/webdriver/remote/webdriver.py", line 154, in __init__
    # self.start_session(desired_capabilities, browser_profile)
  # File "/home/bkim/anaconda3/lib/python3.6/site-packages/selenium/webdriver/remote/webdriver.py", line 243, in start_session
    # response = self.execute(Command.NEW_SESSION, parameters)
  # File "/home/bkim/anaconda3/lib/python3.6/site-packages/selenium/webdriver/remote/webdriver.py", line 312, in execute
    # self.error_handler.check_response(response)
  # File "/home/bkim/anaconda3/lib/python3.6/site-packages/selenium/webdriver/remote/errorhandler.py", line 242, in check_response
    # raise exception_class(message, screen, stacktrace)
# selenium.common.exceptions.WebDriverException: Message: unknown error: Chrome failed to start: crashed
  # (Driver info: chromedriver=2.35.528139 (47ead77cb35ad2a9a83248b292151462a66cd881),platform=Linux 3.10.0-693.5.2.el7.x86_64 x86_64)

browser.stop_client()
browser.close()
browser.quit()
