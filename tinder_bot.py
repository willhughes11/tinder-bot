#!/usr/bin/env python3
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from getpass import getpass
from PIL import Image
from io import BytesIO
import base64
import traceback
from input_args import get_input_args
from remote_server.remote_selenium_server import selenium_server
from utility_functions import *
from tinder_functions import get_tinder_api_request, post_tinder_api_request

class TinderBotV1():
    def __init__(self,driver,host,port,human_login,use_api,min_rating,pref_race):
        self.url = 'https://tinder.com/'
        self.driver = driver
        self.host = host
        self.port = port
        self.human_login = human_login
        self.use_api = use_api
        self.min_rating = min_rating
        self.pref_race = pref_race
    
    def login(self):
        driver = self.driver
        human_login = self.human_login

        driver.get(self.url)
        driver.maximize_window()

        if human_login:
            time.sleep(70)
        else:
            # print('Enter Facebook Username:')
            # fb_username = input()
            # print('Enter Facebook Password:')
            # fb_password = getpass()
            
            find_and_click(driver, '//*[@id="c-1560500889"]/div/div[2]/div/div/div[1]/div[1]/button/div[2]')
            find_and_click(driver,'//*[@id="c-1560500889"]/div/div[1]/div/main/div[1]/div/div/div/div/header/div/div[2]/div[2]/a/div[2]')
            find_and_click(driver,'//*[@id="c1006085331"]/main/div/div[1]/div/div/div[3]/span/div[2]/button')

            base_window = driver.window_handles[0]
            facebook_window = driver.window_handles[1]

            driver.switch_to.window(facebook_window)
            find_and_type(driver, '//*[@id="email"]', 'willhughes2110@gmail.com')
            find_and_type(driver, '//*[@id="pass"]', 'Messyroom12wkh!')
            find_and_click(driver, '/html/body/div/div[2]/div[1]/form/div/div[3]/label[2]/input')
            time.sleep(3)

            driver.switch_to.window(base_window)

            find_and_click(driver,'//*[@id="c1006085331"]/main/div/div/div/div[3]/button[1]')
            find_and_click(driver, '//*[@id="c1006085331"]/main/div/div/div/div[3]/button[1]')

            time.sleep(10)
        
    def get_match_images_and_swipe(self,likes,like_limit=10):
        driver = self.driver
        use_api = self.use_api

        if use_api:
            local_storage = driver.execute_script('return window.localStorage;')
            api_token = local_storage['TinderWeb/APIToken']
            url = 'https://api.gotinder.com/v2/recs/core'
            data = get_tinder_api_request(url,api_token)
            for i in data['data']['results']:
                if likes < like_limit:
                    user_id = i['user']['_id']
                    images = []
                    for y in i['user']['photos']:
                        img_url = y['processedFiles'][0]['url']
                        images.append(img_url)

                    print(i['user']['name'])
                    likes += self.match_decision(images,user_id,api_token)
                else:
                    break
                
            return likes
        else:
            buffered = BytesIO()
            window = driver.get_window_size()
            
            loc,size = find_elem_pos_and_size(driver,'//*[@id="c-1560500889"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div/div[3]/div[1]')
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            div = soup.select('#c-1560500889 > div > div.App__body.H\(100\%\).Pos\(r\).Z\(0\) > div > main > div.H\(100\%\) > div > div > div.Mt\(a\).Px\(4px\)--s.Pos\(r\).Expand.H\(--recs-card-height\)--ml.Maw\(--recs-card-width\)--ml > div.recsCardboard__cardsContainer.H\(100\%\).Pos\(r\).Z\(1\) > div > div.Toa\(n\).Bdbw\(--recs-gamepad-height\).Bdbc\(t\).Bdbs\(s\).Bgc\(\#000\).Wc\(\$transform\).Prs\(1000px\).Bfv\(h\).Ov\(h\).W\(100\%\).StretchedBox.Bdrs\(8px\) > div.Expand.D\(f\).Pos\(r\).tappable-view.Cur\(p\) > div.CenterAlign.D\(f\).Fxd\(r\).W\(100\%\).Px\(8px\).Pos\(a\).TranslateZ\(0\)')
            try:
                buttons = div[0].find_all('button')
            except:
                buttons = [1]
            
            if window['width'] <= 1440 and window['height'] <= 875:
                left = loc['x']+700
                top = loc['y']
                right = loc['x']+1100 + size['width']
                bottom = loc['y'] + size['height']+400
            else:
                left = loc['x']
                top = loc['y']
                right = loc['x'] + size['width']
                bottom = loc['y'] + size['height']

            if check_exists_by_xpath(driver, '//*[@id="c1006085331"]/main/div/div[2]/button[2]/div[2]'):
                find_and_click(driver, '//*[@id="c1006085331"]/main/div/div[2]/button[2]/div[2]')

            images = []
            for i in range(1,len(buttons)+1):
                if len(buttons) > 1:
                    find_and_click(driver,f'//*[@id="c-1560500889"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[3]/div[1]/div[2]/button[{i}]', False)
                png = driver.get_screenshot_as_png()
                im = Image.open(BytesIO(png))
                im = im.crop((left, top, right, bottom))
                rgb_im = im.convert('RGB')
                rgb_im.save(buffered, format="JPEG")
                rgb_im.save("img1.png","PNG")
                img_str = base64.b64encode(buffered.getvalue())
                images.append(img_str.decode('utf-8'))

            self.match_decision(images)

            return likes
    
    def match_decision(self,images,user_id=None,api_token=None):
        driver = self.driver
        host = self.host
        port = self.port
        use_api = self.use_api
        min_rating = self.min_rating
        pref_race = self.pref_race

        rating = get_rating(host=host,port=port,images=images,race=pref_race,rating=min_rating)
        print(rating)

        if use_api:
            if rating['match']:
                post_tinder_api_request(f'https://api.gotinder.com/like/{user_id}?locale=en', api_token)
                return 1
            else:
                get_tinder_api_request(f'https://api.gotinder.com/pass/{user_id}?locale=en',api_token)
                return 0
        else:
            if rating['match']:
                find_by_selector_and_click(driver,'#c-1560500889 > div > div.App__body.H\(100\%\).Pos\(r\).Z\(0\) > div > main > div.H\(100\%\) > div > div > div.Mt\(a\).Px\(4px\)--s.Pos\(r\).Expand.H\(--recs-card-height\)--ml.Maw\(--recs-card-width\)--ml > div.recsCardboard__cardsContainer.H\(100\%\).Pos\(r\).Z\(1\) > div > div.Pos\(a\).B\(0\).Iso\(i\).W\(100\%\).Start\(0\).End\(0\) > div > div.Mx\(a\).Fxs\(0\).Sq\(70px\).Sq\(60px\)--s.Bd.Bdrs\(50\%\).Bdc\(\$c-ds-border-gamepad-like-default\) > button')
                return 1
            else:
                find_by_selector_and_click(driver,'#c-1560500889 > div > div.App__body.H\(100\%\).Pos\(r\).Z\(0\) > div > main > div.H\(100\%\) > div > div > div.Mt\(a\).Px\(4px\)--s.Pos\(r\).Expand.H\(--recs-card-height\)--ml.Maw\(--recs-card-width\)--ml > div.recsCardboard__cardsContainer.H\(100\%\).Pos\(r\).Z\(1\) > div > div.Pos\(a\).B\(0\).Iso\(i\).W\(100\%\).Start\(0\).End\(0\) > div > div.Mx\(a\).Fxs\(0\).Sq\(70px\).Sq\(60px\)--s.Bd.Bdrs\(50\%\).Bdc\(\$c-ds-border-gamepad-nope-default\) > button')
                return 0

if __name__ == '__main__':
    try:
        platform = sys.platform
        args = get_input_args()
        remote = args.remote
        host = args.host
        port = args.port
        human_login = args.human_login
        use_api = args.use_api
        pref_race = args.pref_race
        min_rating = args.min_rating

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

        tinder_bot = TinderBotV1(driver,host,port,human_login=human_login,use_api=use_api,pref_race=pref_race,min_rating=min_rating)
        tinder_bot.login()
        likes = 0
        while likes < 10:
            likes += tinder_bot.get_match_images_and_swipe(likes)
    except:
        print(traceback.print_exc())
    # finally:
    #     driver.quit()
