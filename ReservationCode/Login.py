# Luo Y
# 2023-04-18
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
from preprocess import ImagePreprocessor
from Regular_act import elementselector
from selenium.webdriver.support.ui import WebDriverWait
# -*- coding: utf-8 -*-


class loginhandler:
    def __init__(self, username, password, website, user, pwd, img, cap, log, login_button,WAIT_TIME,driver):
        self.website = website
        self.username = username
        self.password = password
        self.user = user
        self.pwd = pwd
        self.img = img
        self.cap = cap
        self.log = log
        self.login_button = login_button
        self.preprocessor = ImagePreprocessor()
        self.ignore_login_button = False
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 3)
        self.inter = elementselector(self.driver)

    def login_action(self):
        self.driver.get(self.website)
        def need_captcha( locator_type, locator):
            try:
                self.inter.interact_element(locator_type=locator_type,locator=locator )
                return True
            except TimeoutException:
                return False
            
        def get_captcha_image_element(locator_type, locator):
            try:
                captcha_element = self.wait.until(
                    EC.presence_of_element_located((locator_type, locator))
                )
                return captcha_element
            except TimeoutException:
                return None
        try:
            self.inter.interact_element(locator=self.login_button, n=1)
        except TimeoutException:
            pass

        while True:
            try:
                self.inter.interact_element(locator_type='id',locator=self.user,input_text=self.username,clear=True,execute_script="arguments[0].click();",n=2)
                self.inter.interact_element(locator_type='id',locator=self.pwd,input_text=self.password,execute_script="arguments[0].click();",n=2)
                if need_captcha(locator_type='id',locator=self.img):
                    captcha_image = get_captcha_image_element(locator_type='id',locator=self.img)
                    captcha_image.screenshot('captcha.png')
                    captcha_text = self.preprocessor.preprocess_image('captcha.png')
                    self.inter.interact_element(locator_type='id',locator=self.cap,clear=True,input_text=captcha_text)
                    os.remove("captcha.png")

                self.inter.interact_element(locator_type='id',locator=self.log,n=1,enabled=True)

                if self.driver.current_url == self.website:
                    break
                else:
                    continue
            
            except TimeoutException:
                continue
    

  
        
    