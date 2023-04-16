import csv
import os
import configparser
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import  QWidget, QPushButton, QGridLayout

# 获取当前文件所在目录的绝对路径,构造相对路径
current_dir = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(current_dir, 'config.ini')

# 读取配置文件
config = configparser.ConfigParser()
config.read(config_file_path, encoding='utf-8')
dict_path = config['data']['dict_path']

class CourtSelection(QWidget):

    def __init__(self):
        super().__init__()
        self.selected_court_1 = None
        self.selected_court_2 = None

        # 设置背景颜色
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.blue)

        # 初始化40个按钮
        self.buttons = {}
        for i in range(15, 20):
            for j in range(1, 9):
                key = f"{i}_{j}"
                button = QPushButton(key, self)
                button.setFixedSize(90, 90)
                button.setStyleSheet("background-color: green")
                self.buttons[key] = button

        # 读取场地字典信息
        self.court_dict = {}
        self.read_dict()

        # 布局
        grid = QGridLayout()
        for i in range(15, 20):
            for j in range(1, 9):
                key = f"{i}_{j}"
                button = self.buttons[key]
                grid.addWidget(button, i-15, j-1)
                button.clicked.connect(self.handle_button_click)
        self.setLayout(grid)

        # 设置窗口标题和字体颜色
        self.setWindowTitle('Court Selection')
        self.setStyleSheet("color: yellow; background-color: blue")
        self.show()
        
    def read_dict(self):

        # 读取场地字典信息
        with open(dict_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            self.court_dict = {row[0]: row[1] for row in reader}

    def handle_button_click(self):
        button = self.sender()
        key = button.text()
        # 更新按钮颜色
        button.setStyleSheet("background-color: red")

        # 更新场地选择
        if self.selected_court_1 is None:
            self.selected_court_1 = key
        elif self.selected_court_2 is None:
            self.selected_court_2 = key

        # 选择两个场地后关闭窗口, 获取对应键的值并打印出来
        if self.selected_court_1 is not None and self.selected_court_2 is not None:
            self.close()

    def get_two_xpath(self):
        xpath_1 = self.court_dict.get(self.selected_court_1)
        xpath_2 = self.court_dict.get(self.selected_court_2)
        return xpath_1, xpath_2

    


    
