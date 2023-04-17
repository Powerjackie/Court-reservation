import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException,NoSuchElementException,ElementNotSelectableException
from selenium.webdriver.common.action_chains import ActionChains
# -*- coding: utf-8 -*-

class VenueReservation:
    def __init__(self, venue, agreement, sports, badminton, forward, refresh, reservation, companion_1, companion_2, submit, WAIT_TIME, login_handler):
        self.venue = venue
        self.agreement = agreement
        self.sports = sports
        self.badminton = badminton
        self.forward = forward
        self.refresh = refresh
        self.reservation = reservation
        self.companion_1 = companion_1
        self.companion_2 = companion_2
        self.submit = submit
        self.driver = login_handler.driver
        self.wait = WebDriverWait(self.driver, WAIT_TIME)

    def mouse_click(self, element):
        """鼠标点击"""
        ActionChains(self.driver).click(element).perform()
            
    
    def reserve_at_8am(self, xpath_1, xpath_2):
        self.xpath_1 = xpath_1
        self.xpath_2 = xpath_2
        try:
            # 点击菜单进入场馆预约页面
            venue_reservation = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, self.venue))
            )
            self.driver.execute_script("arguments[0].click();", venue_reservation)

            # 勾选协议
            check_agreement = self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, self.agreement))
            )
            self.driver.execute_script("arguments[0].click();", check_agreement)  

            # 点击综合馆
            on_sports = self.wait.until(
                EC.element_to_be_clickable((By.XPATH,
                                            self.sports))
            )
            self.driver.execute_script("arguments[0].click();", on_sports)

            # 点击羽毛球馆
            on_badminton = self.wait.until(
                EC.element_to_be_clickable((By.XPATH,
                                            self.badminton))
            )
            self.driver.execute_script("arguments[0].click();", on_badminton)

            # 点击往后一天
            move_forward =  self.wait.until(
                EC.presence_of_element_located((By.XPATH,self.forward))
            )
            self.driver.execute_script("arguments[0].click();", move_forward)

        except TimeoutException:
            return None

        # 循环等待到8点开始预约
        while True:
            current_time = time.localtime(time.time())
            if current_time.tm_hour < 8:
                print('还没到8点，等待中...')
                time.sleep(1)  # 等待三秒
            else:
                print('已到8点，开始进行预约操作')

                # 预约操作
                try:
                    # 点击往后按钮
                    move_forward = self.wait.until(
                        EC.presence_of_element_located((By.XPATH, self.forward))
                    ) 
                    self.driver.execute_script("arguments[0].click();", move_forward)   

                    # 刷新，确保场地可选
                    refresh = self.wait.until(
                        EC.presence_of_element_located((By.XPATH, self.refresh))
                    )
                    self.driver.execute_script("arguments[0].click();", refresh)

                    # 隐式等待，等待页面刷新
                    court1 = self.driver.find_element(By.XPATH, self.xpath_1)
                    self.driver.execute_script("arguments[0].click();", court1)

                    # 显示等待，选择第二个羽毛球场地
                    court2 = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, self.xpath_2))
                    )
                    self.driver.execute_script("arguments[0].click();", court2)

                    # 点击我要预约
                    make_reservation = self.wait.until(
                        EC.element_to_be_clickable((By.XPATH, self.reservation))
                    )
                    print(type(make_reservation))
                    self.driver.execute_script("arguments[0].click();", make_reservation)
                
                except TimeoutException as e:
                    print(f"出现错误：{str(e)}")

                for _ in range(5):
                    try:

                        # 隐式等待，勾选第一个同伴
                        companion_1 = self.driver.find_element(By.XPATH, self.companion_1)
                        self.driver.execute_script("arguments[0].click();", companion_1)    

                        # 显示等待，勾选第二个同伴    
                        companion_2 = self.wait.until(
                            EC.element_to_be_clickable(
                                (By.XPATH, self.companion_2))
                        )
                        self.driver.execute_script("arguments[0].click();", companion_2)

                        # 提交订单
                        submit = self.wait.until(
                            EC.element_to_be_clickable((By.XPATH, self.submit))
                        )
                        self.driver.execute_script("arguments[0].click();", submit)
        
                        # 如果成功点击按钮，则退出 while 循环
                        break

                    except NoSuchElementException:
                        e=NoSuchElementException
                        print(f"出现错误：{str(e)}，正在重新尝试点击...")
        
            break


