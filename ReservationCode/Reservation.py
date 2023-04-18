import time
import logging
from selenium.common.exceptions import TimeoutException,NoSuchElementException,ElementNotSelectableException
from Check import check_courts
from Regular_act import elementselector
# -*- coding: utf-8 -*-

# 设置logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class VenueReservation:
    def __init__(self, venue, agreement, sports, badminton, forward, refresh, 
                    reservation, companion_1, companion_2, submit,
                        driver,xpath_1, xpath_2):
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
        self.xpath_1 = xpath_1
        self.xpath_2 = xpath_2
        self.driver = driver
        self.select_court = check_courts(self.driver,xpath_1, xpath_2)
        self.inter = elementselector(self.driver)
        self.checker = check_courts(driver=self.driver, xpath_1=self.xpath_1, 
                                     xpath_2=self.xpath_2)
    
            
    def reserve_at_8am(self, dict_path):
        self.dict_path = dict_path
        self.selected_courts = []
        def select_court_if_available(locator):
            """
            如果场地可选，则选择场地并将其添加到已选列表中
            :param locator: 场地定位表达式
            """
            # 判断场地是否被选择
            def is_court_available(court):
                try:
                    return "reserved" not in court
                except TypeError as e:
                    print(f"TypeError")
                
            court = self.inter.interact_element(locator=locator, wait_type=None, get_attribute='class')
            if is_court_available(court):
                selected_court = self.inter.interact_element(locator=self.xpath_2, wait_type=None)
                logging.info(f"已选择场地：{selected_court}")
                self.selected_courts.append(selected_court)


        try:
            # 点击菜单进入场馆预约页面
            self.inter.interact_element(locator=self.venue,n=2,enabled=True)
            # 勾选协议
            self.inter.interact_element(locator=self.agreement,n=2)
            # 点击综合馆
            self.inter.interact_element(locator=self.sports,n=2,enabled=True)
            # 点击羽毛球馆
            self.inter.interact_element(locator=self.badminton,n=2,enabled=True)
            # 点击往后一天
            self.inter.interact_element(locator=self.forward,n=1)

        except TimeoutException:
            return None

        # 循环等待到8点开始预约
        while True:
            current_time = time.localtime(time.time())
            if current_time.tm_hour < 8:
                logging.info('还没到8点，等待中...')
                time.sleep(1)  # 等待三秒
            else:
                logging.info('已到8点，开始进行预约操作')

                # 预约操作
                try:
                    # 点击往后按钮
                    self.inter.interact_element(locator=self.forward,n=2)

                    # 刷新，确保场地可选
                    self.inter.interact_element(locator=self.refresh,n=2)

                except TimeoutException as e:
                    logging.error(f"出现错误")
                
                try:
                    if select_court_if_available( self.xpath_1):
                        print("已选择场地1")
                    if select_court_if_available(self.xpath_2):
                        print("已选择场地2")  
                    self.checker.select_courts(self.dict_path,self.selected_courts)
                
                except TimeoutException as e:
                    logging.error(f"出现错误")
                            
                        
                for _ in range(5):
                    try:
                        # 点击我要预约
                        self.inter.interact_element(
                            locator=self.reservation, n=2)  
                
                        # 隐式等待，勾选第一个同伴
                        self.inter.interact_element(
                            locator=self.companion_1,wait_type=None, n=2)

                        # 显示等待，勾选第二个同伴    
                        self.inter.interact_element(
                            locator=self.companion_2, n=2)           

                        # 提交订单
                        self.inter.interact_element(
                            locator=self.submit, n=2)

                    except Exception as e:
                        logging.error("出现错误，正在重新尝试点击...")
                        continue
                    break
                else:
                     return self.driver
            break
        return self.driver


        

