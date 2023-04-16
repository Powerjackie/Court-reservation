import cv2
import os
import configparser
import time
import pytesseract
import threading
import numpy as np
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
# -*- coding: utf-8 -*-

# Set the tessdata directory and OCR engine mode
tessdata_dir_config = r'--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789'

# 构建配置文件的路径
config_file_path = f'C:\\Users\\G1942\\Documents\\GitHub\\Court-reservation\\ReservationData\\config.ini'    

# 读取配置文件
config = configparser.ConfigParser()
config.read(config_file_path, encoding='utf-8')
username = config['login']['username']
password = config['login']['password']


# this code is to define a class
class VenueReservation:
    _driver = None
    _lock = threading.Lock()

    def __init__(self):
        None

    @classmethod
    def get_driver(cls):
        with cls._lock:
            try:
                if cls._driver is None:
                    start_time = time.time()
                    service = Service(executable_path=r"C:\Program Files (x86)\Microsoft\Edge\Application\edgedriver_win64\msedgedriver.exe")
                    options = Options()
                    options.binary_location = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
                    options.use_chromium = True
                    options.add_argument("--disable-usb-keyboard-detect")
                    options.add_argument("--disable-extensions")
                    # options.add_argument("--headless")
                    cls._driver = webdriver.Edge(service=service, options=options)
                    end_time = time.time()
                    print("Browser started in {:.2f} seconds".format(end_time - start_time))
            
            except Exception as e:
                print(f"Error creating driver: {e}")

        return cls._driver
    
    def open_browser(self):
        driver = VenueReservation.get_driver()
        driver.get('https://ggtypt.njtech.edu.cn/venue/')

    @classmethod
    def close_browser(cls):
        if cls._driver is not None:
            try:
                cls._driver.quit()
                cls._driver = None
            except Exception as e:
                print(f"Error closing browser: {e}")


    def mouse_click(self, element):
        """鼠标点击"""
        ActionChains(VenueReservation.get_driver()).click(element).perform()

    def preprocess_image(self, image_path):
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        # 图像增强
        clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(9,9))
        img = clahe.apply(img)
        # 二值化
        _, img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        # 去噪和填充空洞
        kernel = np.ones((1,1), np.uint8)
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        # 滤波操作代码
        img = cv2.GaussianBlur(img, (3, 3), 0)
        img = cv2.blur(img, (1, 1))
        img = cv2.medianBlur(img, 5)  
        # 将数字放大到合适的尺寸
        img = cv2.resize(img, (0,0), fx=3.5, fy=3.5, interpolation=cv2.INTER_CUBIC)
        # 返回处理后的图片
        return img

    
    def login_action(self, ignore_login_button=False):
        if not ignore_login_button:
            try:
                login_button = WebDriverWait(VenueReservation.get_driver(), 1).until(
                    EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div/div/div[4]'))
                )
                login_button.click()
            except TimeoutException:
                pass

        try:
            username_field = WebDriverWait(VenueReservation.get_driver(), 0.5).until(
                EC.presence_of_element_located((By.ID, 'username'))
            )
            if username_field.get_attribute('value'):
                username_field.send_keys(Keys.CONTROL + 'a')
                username_field.send_keys(Keys.DELETE)
            username_field.send_keys(username)

            password_field = WebDriverWait(VenueReservation.get_driver(), 0.5).until(
                EC.presence_of_element_located((By.ID, 'password'))
            )
            password_field.send_keys(password)

            captcha_field = WebDriverWait(VenueReservation.get_driver(), 0.5).until(
                EC.element_to_be_clickable((By.ID, "pc-captcha"))
            )
            captcha_field.click()
            captcha_image = WebDriverWait(VenueReservation.get_driver(), 0.5).until(
                EC.element_to_be_clickable((By.ID, "pc-captcha"))
            )
            captcha_image.screenshot('captcha.png')
            processed_image = self.preprocess_image('captcha.png')  # 调用预处理方法
            captcha_text = pytesseract.image_to_string(processed_image, config=tessdata_dir_config)
            captcha_input = WebDriverWait(VenueReservation.get_driver(), 0.5).until(
                EC.presence_of_element_located((By.ID, "imgcaptcha"))
            )
            if captcha_input.get_attribute('value'):
                captcha_input.send_keys(Keys.CONTROL + 'a')
                captcha_input.send_keys(Keys.DELETE)
            captcha_input.send_keys(captcha_text)
            os.remove("captcha.png")  # 删除验证码图片

        except TimeoutException:
            pass

        try:
            login_button = WebDriverWait(VenueReservation.get_driver(), 0.5).until(
                EC.element_to_be_clickable((By.ID, 'login'))
            )
            login_button.click()
        except TimeoutException:
            pass

        try:
            WebDriverWait(VenueReservation.get_driver(), 0.5).until(
                EC.url_contains('ggtypt.njtech.edu.cn/venue/')
            )
            return True
        
        except TimeoutException:
            return False
    

    def reserve_at_8am(self):
        # 进入预约界面
        try:
            # 点击菜单进入场馆预约页面
            venue_reservation = WebDriverWait(VenueReservation.get_driver(), 0.5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//li[@class='ivu-menu-item' and @data-v-1f07b40e and descendant::span[text()='场馆预约']]"))
            )
            # venue_reservation.click()
            # self.mouse_click(venue_reservation)  
            self._driver.execute_script("arguments[0].click();", venue_reservation)

            # 勾选协议
            check_agreement = WebDriverWait(VenueReservation.get_driver(), 1).until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div/div[2]/div[3]/div/div[2]/div/div/div[2]/div[2]/label/span/input"))
            )
            # check_agreement.click()
            self.mouse_click(check_agreement)
            # self.driver.execute_script("arguments[0].click();", check_agreement)  
            
            # 点击综合馆
            on_sports = WebDriverWait(VenueReservation.get_driver(), 0.5).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "/html/body/div[1]/div/div[2]/div[3]/div/div[2]/div/div/div[2]/form/div[2]/div/div/label[7]"))
            )
            on_sports.click()
            # self.mouse_click(on_sports)  

            # 点击羽毛球馆
            on_badminton = WebDriverWait(VenueReservation.get_driver(), 0.5).until(
                EC.element_to_be_clickable((By.XPATH,
                                            "/html/body/div[1]/div/div[2]/div[3]/div/div[2]/div/div/div[2]/form/div[3]/div/div/label"))
            )
            on_badminton.click()
            # self.mouse_click(on_badminton)  

            # 点击往后一天
            move_back = WebDriverWait(VenueReservation.get_driver(), 0.5).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div[3]/div/div[2]/div/div/div[2]/form/div[1]/div/button[2]/i"))
            )
            move_back.click()
            # self.mouse_click(move_back)
            # self.driver.execute_script("arguments[0].click();", move_back)
        except TimeoutException:
            return None

        # 循环等待到8点开始预约
        while True:
            current_time = time.localtime(time.time())
            if current_time.tm_hour < 8:
                print('还没到8点，等待中...')
                time.sleep(3)  # 等待三秒
            else:
                print('已到8点，开始进行预约操作')

                # 预约操作
                try:
                    # 选择后天的预约场地
                    move_back = WebDriverWait(VenueReservation.get_driver(), 0.5).until(
                        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div[3]/div/div[2]/div/div/div[2]/form/div[1]/div/button[2]/i"))
                    )
                    move_back.click()    

                    # 刷新，确保场地可选
                    refresh = WebDriverWait(VenueReservation.get_driver(), 0.5).until(
                        EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div[3]/div/div[2]/div/div/div[2]/form/div[1]/div/button[3]/i"))
                    )
                    refresh.click()

                    # 选择第一个羽毛球场地
                    court1 = WebDriverWait(VenueReservation.get_driver(), 0.5).until(
                        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div[3]/div/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div/div/div/table/tbody/tr[5]/td[5]/div"))
                    )
                    court1.click()
                    # self.mouse_click(court1)              

                    # 选择第二个羽毛球场地
                    court2 = WebDriverWait(VenueReservation.get_driver(), 0.5).until(
                        EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[2]/div[3]/div/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div/div/div/table/tbody/tr[6]/td[5]/div"))
                    )
                    court2.click()
                    # self.mouse_click(court2)  

                except Exception as e:
                    print(f"出现错误：{str(e)}")            

                try:

                    # 点击我要预约
                    make_reservation = WebDriverWait(VenueReservation.get_driver(), 1).until(
                        EC.element_to_be_clickable((By.XPATH,"/html/body/div[1]/div/div[2]/div[3]/div/div[2]/div/div/div[2]/div[4]/div/button/span"))
                    )
                    make_reservation.click()
                    # self.mouse_click(make_reservation)
                
                except Exception as e:
                    print(f"出现错误：{str(e)}")


                while True:
                    try:  
                        # 勾选第一个同伴
                        companion_1 = WebDriverWait(VenueReservation.get_driver(), 2).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, "//span[contains(text(), '吴楠') and contains(@class, 'ivu-checkbox-group-item') and contains(@class, 'ivu-checkbox-wrapper-checked')]"))
                        )
                        companion_1.click()
                        # self.mouse_click(companion_1)     

                        # 勾选第二个同伴    
                        companion_2 = WebDriverWait(VenueReservation.get_driver(), 0.5).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, "//span[contains(text(), '曹桔垄') and contains(@class, 'ivu-checkbox-group-item') and not(contains(@class, 'ivu-checkbox-wrapper-checked'))]"))
                        )
                        companion_2.click()
                        # self.mouse_click(companion_2)

                        # 提交订单
                        submit = WebDriverWait(VenueReservation.get_driver(), 0.5).until(
                            EC.element_to_be_clickable((By.XPATH, "//div[@class='text-primary inlineBlock btnMaring pointer']//button[contains(text(),'提交订单')]"))
                        )
                        submit.click()
                        # self.mouse_click(submit)  
        
                        # 如果成功点击按钮，则退出 while 循环
                        break

                    except Exception as e:
                        print(f"出现错误：{str(e)}，正在重新尝试点击...")
        
            break

    def start_reservation(self):        
        while True:
            try:
                if self.login_action():
                    self.reserve_at_8am()
                    break
            except Exception as e:
                print(f'发生异常：{e}')
            print('重新登录')
            self.restry_login()

    def restry_login(self):
        self.ignore_login_button = True
        self.login_action() 


# 开始运行程序
if __name__ == '__main__':
        reservation = VenueReservation()
        reservation.open_browser()
        reservation.login_action()
        reservation.start_reservation()
        reservation.close_browser()

