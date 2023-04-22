# Luo Y
# *-* coding: utf-8 *-*
# 2023.4.17
import random
from Browser import elementselector

class check_courts:
    def __init__(self, driver):
        self.driver = driver
        self.inter = elementselector(self.driver)
        

    def select_courts(self, selected_courts ,court_dict):    
        self.selected_courts = selected_courts
        self.court_dict = court_dict
       # 判断场地是否被选择
        def is_court_available(court):
            try:
                return "free"  in court.get_attribute("class")
            except TypeError:
                print(f"找不到场地")
                
        # 判断选择了几个场地
        num_selected_courts = len(self.selected_courts)
        if num_selected_courts == 0:
            print("没有选择场地")
        elif num_selected_courts == 1:
            print("选择了一个场地")
        else:
            print("选择了两个场地")

        # 判断是否需要在剩余的场地中选择
        if num_selected_courts < 2:
            # 计算还需要选择的场地数
            num_remaining_courts = 2 - num_selected_courts
            # 获取剩余的场地
            remaining_courts = [xpath for key, xpath in self.court_dict.items() 
                                if key not in self.selected_courts]
            # 随机选择场地
            random.shuffle(remaining_courts)
            for i in range(10):
                if num_remaining_courts == 0:
                    break
                # 随机选择一个场地
                court_xpath = remaining_courts[i]
                court_key = list(self.court_dict.keys())[list(self.court_dict.values()).index(court_xpath)]
                print(f"场地为: {court_key}")
                court_elem = self.inter.interact_element(locator=court_xpath,enabled=True)
                if is_court_available(court_elem):
                    try:
                        self.inter.interact_element(locator=court_xpath,n=2)
                        self.selected_courts = list(set(self.selected_courts))
                        self.selected_courts.append(court_key)
                        # 从剩余场地列表中移除已选场地
                        remaining_courts.remove(court_xpath)
                        print(f"选择了场地: {court_key}")
                        num_remaining_courts -= 1
                    except Exception as e:
                        print(f"无法选择场地{court_key}，原因为")
                else:
                    print(f"场地{court_key}已经被选")

   
        
    

