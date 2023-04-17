from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import os
from preprocess import ImagePreprocessor
# -*- coding: utf-8 -*-


class LoginHandler:
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
        self.wait = WebDriverWait(self.driver, WAIT_TIME)

    def login_action(self):
        self.driver.get(self.website)
        try:
            loginbutton = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, self.login_button))
            )
            loginbutton.click()
        except TimeoutException:
            pass

        while True:
            try:
                username_field = self.wait.until(
                    EC.presence_of_element_located((By.ID, self.user))
                )
                if username_field.get_attribute('value'):
                    username_field.send_keys(Keys.CONTROL + 'a')
                    username_field.send_keys(Keys.DELETE)
                username_field.send_keys(self.username)

                password_field = self.wait.until(
                    EC.presence_of_element_located((By.ID, self.pwd))
                )
                password_field.send_keys(self.password)

                if self.need_captcha():
                    captcha_field = self.wait.until(
                        EC.element_to_be_clickable((By.ID, self.img))
                    )
                    captcha_field.click()
                    captcha_image = self.wait.until(
                        EC.element_to_be_clickable((By.ID, self.img))
                    )
                    captcha_image.screenshot('captcha.png')
                    captcha_text = self.preprocessor.preprocess_image('captcha.png')
                    captcha_input = self.wait.until(
                        EC.presence_of_element_located((By.ID, self.cap))
                    )
                    if captcha_input.get_attribute('value'):
                        captcha_input.send_keys(Keys.CONTROL + 'a')
                        captcha_input.send_keys(Keys.DELETE)
                    captcha_input.send_keys(captcha_text)
                    os.remove("captcha.png")

                loginbutton = self.wait.until(
                    EC.element_to_be_clickable((By.ID, self.log))
                )
                loginbutton.click()

                if self.driver.current_url == self.website:
                    break
                else:
                    continue
            

            except TimeoutException:
                continue
            
        
    def need_captcha(self):
        try:
            self.wait.until(
                EC.presence_of_element_located((By.ID, self.img)))
            return True
        except TimeoutException:
            return False