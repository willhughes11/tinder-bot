#!/usr/bin/env python3
import sys
import time
import traceback
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from input_args import get_input_args
from remote_server.remote_selenium_server import selenium_server
from utility_functions import find_and_click, find_and_type

class TinderBotV1():
    def __init__(self,driver):
        self.url = 'https://tinder.com/'
        self.driver = driver
    
    def login(self):
        driver = self.driver
        driver.get(self.url)
        find_and_click(driver,'//*[@id="q243527110"]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a/div[2]/div[2]')
        find_and_click(driver,'//*[@id="q-1484853966"]/main/div/div[1]/div/div/div[3]/span/div[3]/button')
        find_and_type(driver,'//*[@id="q-1484853966"]/main/div/div[1]/div/div[2]/div/input','4047190217')
        find_and_click(driver,'//*[@id="q-1484853966"]/main/div/div[1]/div/button')

        print('Enter your Tinder SMS verification code:')
        verification_code = input()

        find_and_type(driver,'//*[@id="q-1484853966"]/main/div/div[1]/div/div[3]/input[1]',verification_code)
        find_and_click(driver, '//*[@id="q-1484853966"]/main/div/div[1]/div/button')

if __name__ == '__main__':
    print('Starting...')
    platform = sys.platform
    args = get_input_args()
    remote = args.remote

    if platform == 'darwin':
        if remote:
            selenium_server()
            driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', desired_capabilities=webdriver.DesiredCapabilities.CHROME)
        else:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    elif platform == 'linux':
        if remote:
            selenium_server()
            driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub', desired_capabilities=webdriver.DesiredCapabilities.CHROME)
        else:
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    tinder_bot = TinderBotV1(driver)
    tinder_bot.login()

