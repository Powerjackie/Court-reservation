# Luo Y
# 2023-04-18
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
from preprocess import ImagePreprocessor
from Browser import elementselector
# -*- coding: utf-8 -*-

class loginhandler:
    def __init__(self,driver):
        self.preprocessor = ImagePreprocessor()
        self.ignore_login_button = False
        self.driver = driver
        self.inter = elementselector(self.driver)

    def login_action(self, username, password, website, user, pwd, log ,login_button, img=None, cap=None):
        """
        通用的登录操作元素
        :param username: 用户名
        :param password: 密码
        :param website: 登录网址
        :param user: 用户名输入框
        :param pwd: 密码输入框
        :param img: 验证码图片,默认不存在
        :param cap: 验证码输入框,默认不存在
        :param log: 登录按钮
        """
        self.driver.get(website)
        try:
            self.inter.interact_element(locator=login_button, n=1)
        except TimeoutException:
            pass

        while True:
            try:
                self.inter.interact_element(locator_type='id',locator=user,input_text=username,clear=True,n=2)
                self.inter.interact_element(locator_type='id',locator=pwd,input_text=password,n=2)
                if img is not None:
                    captcha_image = self.inter.interact_element(locator_type='id',locator=img)
                    captcha_image.screenshot('captcha.png')
                    captcha_text = self.preprocessor.preprocess_image('captcha.png')
                    self.inter.interact_element(locator_type='id',locator=cap,clear=True,input_text=captcha_text)
                    os.remove("captcha.png")

                self.inter.interact_element(locator_type='id',locator=log,n=1,enabled=True)

                if self.driver.current_url == website:
                    break
                else:
                    continue
            
            except TimeoutException:
                continue
    

  
        
    