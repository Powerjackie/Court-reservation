# Luo Y
# 2023-04-18
# -*- coding: utf-8 -*-
def main():
    import sys
    import os
    import configparser
    from Browser import initialize
    from PyQt5.QtWidgets import QApplication
    from GUI import CourtSelection
    from Reservation import VenueReservation
    from Login import loginhandler

    # 获取当前文件所在目录构造相对路径
    locators_path = os.path.join(os.path.dirname(__file__), 'data/common/hidden/inside/locators.ini')
    config_file_path = os.path.join(os.path.dirname(__file__), 'config/config.ini')
    # 读取配置文件
    config = configparser.ConfigParser()
    with open(config_file_path, encoding='utf-8') as f:
        config.read_file(f)
    with open(locators_path, encoding='utf-8') as f:
        config.read_file(f)

    login = config['login']
    xpath = config['Xpath']
    id = config['id']
    

    username = login['username']
    password = login['password']
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
    right = xpath['right']
    left = xpath['left']
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
            print(driver)

            # 初始化LoginHandler和Reservation类，传入浏览器实例
            login_handler = loginhandler(username, password,website, user, pwd, img, cap, log, login_button,driver=driver)       
            reservation = VenueReservation(venue, agreement, sports, badminton,
                            forward, ref, res,submit_res, companion_1, companion_2, 
                            submit, driver, xpath_1, xpath_2,court_dict)
    
            # 登录
            login_handler.login_action()
            # 预约        
            reservation.reserve_at_8am(court_1,court_2)
        except Exception as e:
            raise

        finally:
            initialize.close_browser()

if __name__ == '__main__':
    main()

    


