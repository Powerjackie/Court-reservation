import sys
import os
import configparser
from Reservation import VenueReservation
from PyQt5.QtWidgets import QApplication
from GUI import CourtSelection
from LonginHandler import LoginHandler
from Browser import Browser

# 获取当前文件所在目录的绝对路径,构造相对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(current_dir, 'config.ini')
# 读取配置文件
config = configparser.ConfigParser()
config.read(config_file_path, encoding='utf-8')
dict_path = config['data']['dict_path']
username = config['login']['username']
password = config['login']['password']
executable_path = config['File_Path']['executable_path']
binary_location = config['File_Path']['binary_location']
website = config['login']['website']
user = config['id']['user']
pwd = config['id']['pwd']
img = config['id']['img']
cap = config['id']['cap']
log = config['id']['log']
login_button = config['Xpath']['login_button']
venue = config['Xpath']['venue']
agreement = config['Xpath']['agreement']
sports = config['Xpath']['sports']
badminton = config['Xpath']['badminton']
forward = config['Xpath']['forward']
ref = config['Xpath']['refresh']
res = config['Xpath']['reservation']
companion_1 = config['Xpath']['companion_1']
companion_2 = config['Xpath']['companion_2']
submit = config['Xpath']['submit']
WAIT_TIME = int(config['time']['WAIT_TIME'])
IMPLICIT = int(config['time']['IMPLICIT_WAIT'])

# 实例化QApplication类并调用
app = QApplication(sys.argv)
court_selection = CourtSelection(dict_path)
app.exec_()
xpath_1, xpath_2 = court_selection.get_two_xpath()

# 实例化浏览器实例
driver = Browser.get_driver(os.path.join(executable_path), os.path.join(binary_location),IMPLICIT,WAIT_TIME,headless=True)

# 初始化LoginHandler和Reservation类，传入浏览器实例
login_handler = LoginHandler(username, password, website, user, pwd, img, cap, log, login_button,WAIT_TIME,driver)
reservation = VenueReservation(venue, agreement, sports, badminton, forward, ref, res, companion_1, companion_2, submit,WAIT_TIME, login_handler)

# 登录
login_handler.login_action()
# 预约
reservation.reserve_at_8am(xpath_1, xpath_2)
