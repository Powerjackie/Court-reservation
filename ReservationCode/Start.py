# Luo Y
# 2023-04-18
# -*- coding: utf-8 -*-
import configparser
import os


# 构造读取配置文件的函数
def get_config(section_name, config_path=None):
    if not config_path:
        config_path = os.path.join(os.path.dirname(__file__), 'config.ini')

    config = configparser.ConfigParser()
    with open(config_path, encoding='utf-8') as f:
        config.read_file(f)

    try:
        section = config[section_name]
    except KeyError:
        print("section error")

    return section

def main():
    import sys
    from Browser import initialize
    from PyQt5.QtWidgets import QApplication
    from GUI import CourtSelection
    from Reservation import VenueReservation
    from Login import loginhandler

    # 获取当前文件所在目录构造相对路径
    locators_path = os.path.join(os.path.dirname(__file__), 'data/common/hidden/inside/locators.ini')
    config_file_path = os.path.join(os.path.dirname(__file__), 'config/config.ini')
    # 读取配置文件
    login = get_config('login', config_file_path)
    website = get_config('website', locators_path)
    xpath = get_config('Xpath', locators_path)
    id = get_config('id', locators_path)
    
    username = login['username']
    password = login['password']
    website = website['website']
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
    submit_res = xpath['submit_res']
    companion_1 = xpath['companion_1']
    companion_2 = xpath['companion_2']
    submit = xpath['submit']

    driver = None   # 定义全局变量
    
    # 实例化QApplication类并调用
    app = QApplication(sys.argv)
    court_selection = CourtSelection()
    court_selection.show()
    app.exec_()
      
    xpath_1, xpath_2,headless,court_1,court_2,court_dict = court_selection.get_info()
    if xpath_1 != None and xpath_2 != None:
        try:          
            # 实例化浏览器实例
            driver = initialize.get_driver(headless)

            # 初始化LoginHandler和Reservation类，传入浏览器实例
            login_handler = loginhandler(driver=driver)       
            reservation = VenueReservation( driver)
    
            # 登录
            login_handler.login_action(username, password,website, user, pwd,log, login_button,img, cap)
            # 预约        
            reservation.reserve_at_8am(court_1,court_2,venue, agreement, sports, badminton,
                            forward, ref, res,submit_res, companion_1, companion_2, 
                            submit, xpath_1, xpath_2,court_dict)
            initialize.close_browser()
        
        except Exception as e:
            print(" ")

        finally:
            initialize.close_browser()

if __name__ == '__main__':
    main()

    


