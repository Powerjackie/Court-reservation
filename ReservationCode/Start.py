# Luo Y
# 2023-04-18
# -*- coding: utf-8 -*-
import sys
import os
import configparser
from Browser import Browser
from PyQt5.QtWidgets import QApplication
from GUI import CourtSelection
from Reservation import VenueReservation
from Login import loginhandler

# 获取当前文件所在目录的绝对路径,构造相对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(current_dir, 'config.ini')
# 读取配置文件
config = configparser.ConfigParser()
with open(config_file_path, encoding='utf-8') as f:
    config.read_file(f)
data = config['data']
login = config['login']
file_path = config['File_Path']
xpath = config['Xpath']
id = config['id']
time = config['time']

dict_path = data['dict_path']
username = login['username']
password = login['password']
executable_path = file_path['executable_path']
binary_location = file_path['binary_location']
image_path = file_path['image']
website = login['website']
user = id['user']
pwd = id['pwd']
img = id['img']
cap = id['cap']
log = id['log']
login_button = xpath['login_button']
venue = xpath['venue']
agreement = xpath['agreement']
sports = xpath['sports']
badminton = xpath['badminton']
forward = xpath['forward']
ref = xpath['refresh']
res = xpath['reservation']
companion_1 = xpath['companion_1']
companion_2 = xpath['companion_2']
submit = xpath['submit']
IMPLICIT = int(time['IMPLICIT_WAIT'])
WAIT_TIME = int(time['WAIT_TIME'])

#...

driver = None   # 定义全局变量

# 实例化QApplication类并调用
app = QApplication(sys.argv)
court_selection = CourtSelection(dict_path, image_path)
app.exec_()
xpath_1, xpath_2 = court_selection.get_two_xpath()

if xpath_1 != None and xpath_2 != None:
    try:
        # 实例化浏览器实例
        driver = Browser.get_driver(os.path.join(executable_path), os.path.join(binary_location),IMPLICIT,headless=False)

        # 初始化LoginHandler和Reservation类，传入浏览器实例
        login_handler = loginhandler(username, password, website, user, pwd, img, cap, log, login_button,WAIT_TIME,driver)
        reservation = VenueReservation(venue, agreement, sports, badminton,
                        forward, ref, res, companion_1, companion_2, 
                        submit, driver, xpath_1, xpath_2)

        # 登录
        login_handler.login_action()
        # 预约
        reservation.reserve_at_8am(dict_path)
    except Exception as e:
        pass

    finally:
        Browser.close_browser()

    


