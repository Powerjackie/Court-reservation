# Luo Y
# 2023-04-20
# -*- coding: utf-8 -*-
import time
import logging
from selenium.common.exceptions import TimeoutException
from Check import check_courts
from Browser import elementselector


# 设置logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class VenueReservation:
 
     
    def __init__(self, driver):
        self.driver = driver
        self.inter = elementselector(self.driver)
        self.checker = check_courts(driver=self.driver)
    
            
    def reserve_at_8am(self,court_1, court_2,venue, agreement, sports, badminton, forward, refresh, 
                    reservation,submit_res, companion_1, companion_2, submit,xpath_1, xpath_2,court_dict):
        """
        预约场馆。
        
        参数：
        court_1: 第一个场地
        court_2: 第二个场地
        
        返回值：
        None
        """
        self.selected_courts = []
        def select_court_if_available(locator):
            """
            如果场地可选，则选择场地并将其添加到已选列表中
            :param locator: 场地定位表达式
            """
            # 判断场地是否被选择
            def is_court_available(court):
                try:
                    return "free"  in court
                except TypeError:
                    print(f"找不到场地")
                
            court = self.inter.interact_element(locator=locator,  get_attribute='class')
            if is_court_available(court):
                selected_court = self.inter.interact_element(locator=locator,n=2)
                logging.info(f"已选择场地：{selected_court}")
                self.selected_courts.append(selected_court)
        
        
        try:
            # 点击菜单进入场馆预约页面
            self.inter.interact_element(locator=venue,n=2,enabled=True)
            # 勾选协议
            self.inter.interact_element(locator=agreement,n=2)
            # 点击综合馆
            self.inter.interact_element(locator=sports,n=2,enabled=True)
            # 点击羽毛球馆
            self.inter.interact_element(locator=badminton,n=2,enabled=True)
            # 点击往后一天
            self.inter.interact_element(locator=forward,n=1)

        except TimeoutException:
            return None

        # 循环等待到8点开始预约
        while True:
            current_time = time.localtime(time.time())
            if current_time.tm_hour < 8:
                logging.info('还没到8点，等待中...')
                time.sleep(1)  # 等待三秒
                continue
            else:
                logging.info('已到8点，开始进行预约操作')

                # 预约操作
                try:
                    # 点击往后按钮
                    self.inter.interact_element(locator=forward,n=2)

                    # 刷新，确保场地可选
                    self.inter.interact_element(locator=refresh,n=2)

                except TimeoutException as e:
                    logging.info(f"出现错误reser108")

                try:
                    select_court_if_available(locator=xpath_1)
                    select_court_if_available(locator=xpath_2)                    
                    # 调用检查方法判断是否还要选择场地        
                    self.checker.select_courts(self.selected_courts,court_dict)

                    # 点击我要预约
                    self.inter.interact_element(locator=reservation, n=2)  
        
                except TimeoutException as e:
                    logging.info(f"出现错误,reser121")                                              
                
                for _ in range(3):
                    try:               
                        # 隐式等待，勾选第一个同伴
                        self.inter.interact_element(locator=companion_1,wait_type='implicit', n=2)

                        # 显示等待，勾选第二个同伴    
                        self.inter.interact_element(locator=companion_2, n=2)           

                        # 提交订单
                        self.inter.interact_element(locator=submit, n=2)               

                    except Exception as e:
                        logging.error("出现错误，正在重新尝试...")
                        time.sleep(1)
                        continue

            break

        
    




        

