# Luo Y
# 2023-04-18、
# -*- coding: utf-8 -*-
import csv
import os
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow ,QPushButton, QGridLayout,QLabel,QWidget, QLabel,QToolBar, QToolButton

# 获取当前文件所在目录构造相对路径
weekday_path = os.path.join(os.path.dirname(__file__), 'data/common/hidden/inside/XpathDict_Weekday.csv')
image_path = os.path.join(os.path.dirname(__file__), 'config/image.jpg')
weekend_path = os.path.join(os.path.dirname(__file__), 'data/common/hidden/inside/XpathDict_Weekend.csv')
class CourtSelection(QMainWindow):

    
    def __init__(self):
        super().__init__()
        self.selected_court_1 = None
        self.selected_court_2 = None
        self.court_dict = {}
        self.headless = True  # 默认无头模式
        self.change = True
        self.buttons = {}
        
       
    

        # 读取场地信息字典
        with open(weekday_path, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            self.court_dict = {row['key']: row['xpath'] for row in reader}

        # 创建工具栏
        toolbar = QToolBar(self)
        self.addToolBar(toolbar)

        # 添加无头模式开关按钮
        headless_button = QToolButton(self)
        headless_button.setStyleSheet("color: #FFFF00; ")
        headless_button.setText('打开浏览器窗口')
        headless_button.setCheckable(True)
        headless_button.clicked.connect(self.toggle_headless)
        toolbar.addWidget(headless_button)
        self.headless_button = headless_button # 将headless_button保存到self.headless_button属性中
        
        # 添加Weekend按钮
        weekend_button = QToolButton(self)
        weekend_button.setStyleSheet("color: #FFFF00; ")
        weekend_button.setText('周末')
        weekend_button.setCheckable(True)
        weekend_button.clicked.connect(lambda:self.show_courts(day=False))
        toolbar.addWidget(weekend_button)
        
        # 初始化40个按钮：
        for i in range(15, 20):
                for j in range(1, 9):
                    key = f"{i}_{j}"
                    button = QPushButton(key, self)
                    button.setFixedSize(62,65)
                    button.setStyleSheet("background-color: #808080; color: #000080;")
                    self.buttons[key] = button

        # 添加时间段和日期注释布局
        self.grid = QGridLayout()
        time_labels = ['时间段', '15:-16:30', '16:-17:30', '17:-18:30', '18:-19:30', '19:-20:30']
        day_labels = ['时间段', '1号', '2号', '3号', '4号', '5号', '6号', '7号', '8号']
        for i in range(9):
            label = QLabel(day_labels[i], self)
            label.setFixedSize(62,65)
            label.setStyleSheet("background-color:#808080; color: #FFFF00;")
            label.setAlignment(Qt.AlignCenter)
            self.grid.addWidget(label, 0, i)
        for i in range(1,6):
            label = QLabel(time_labels[i], self)
            label.setFixedSize(62,65)
            label.setStyleSheet("background-color:#808080; color: #FFFF00;")
            label.setAlignment(Qt.AlignCenter)
            self.grid.addWidget(label, i, 0)
            for j in range(1, 9):
                key = f"{i+14}_{j}"
                button = self.buttons[key]
                button.clicked.connect(self.handle_button_click)
                self.grid.addWidget(button, i, j)
        self.setCentralWidget(QWidget(self))
        self.centralWidget().setLayout(self.grid)

        # 添加背景图片
        bg_label = QLabel(self)
        bg_pixmap = QPixmap(image_path).scaled(self.size())
        bg_label.setPixmap(bg_pixmap)
        bg_label.resize(self.size())
        bg_label.lower()
            
        # 设置窗口标题和字体颜色
        self.setWindowTitle('                                                南工大"林丹"-LY')
        self.setStyleSheet("QMainWindow{background-color: transparent;}" 
                           "QPushButton{background-color: #808080; color: #000080;}" 
                           "QLabel{background-color:#808080; color: #FFFF00;}")

        self.show()

    def initialize_buttons(self):
        """
        初始化40个按钮
        """
        self.change = False  # 添加该行代码
        # 清空旧按钮
        for button in self.buttons.values():
            button.deleteLater()
        self.buttons.clear()
        # 初始化40个新按钮
        for i in range(12, 17):
            for j in range(1, 9):
                key = f"{i}_{j}"
                button = QPushButton(key, self)
                button.setFixedSize(62,65)
                button.setStyleSheet("background-color: #808080; color: #000080;")
                button.clicked.connect(self.handle_button_click)
                self.buttons[key] = button
                self.grid.addWidget(button, i-11, j)
         
        
    def show_courts(self, day=True):
        if day:
            with open(weekday_path, 'rb') as f:
                reader = csv.reader(f.read().decode('utf-8').splitlines())
                for row in reader:
                    self.court_dict[row[0].strip()] = row[1].strip()
        else:
            with open(weekend_path, 'rb') as f:
                reader = csv.reader(f.read().decode('utf-8').splitlines())
                for row in reader:
                    self.court_dict[row[0].strip()] = row[1].strip()
        if self.change:
            self.initialize_buttons()


    def handle_button_click(self):
        button = self.sender()
        key = button.text()
        # 只能点击一次
        if button.isEnabled():
            button.setStyleSheet("background-color: #FFFF00")
            button.setEnabled(False)

            # 更新场地选择
            if self.selected_court_1 is None:
                self.selected_court_1 = key
            elif self.selected_court_2 is None:
                self.selected_court_2 = key

            # 选择两个场地后关闭窗口
            if self.selected_court_1 is not None and self.selected_court_2 is not None:
                self.close()


    def get_info(self):
        xpath_1 = self.court_dict.get(self.selected_court_1)
        xpath_2 = self.court_dict.get(self.selected_court_2)
        if self.headless:
            return xpath_1, xpath_2, self.headless,self.selected_court_1,self.selected_court_2,self.court_dict
        else:
            return xpath_1, xpath_2, self.headless,self.selected_court_1,self.selected_court_2,self.court_dict
    

    def toggle_headless(self):
        # 切换无头模式状态
        self.headless = not self.headless
        if not self.headless:
            self.headless_button.setText('关闭浏览器窗口')
        return self.headless
    

    def get_courts(self, court_file_path):
        """
        从文件中读取场地信息，并返回一个字典
        :param court_file_path: 包含场地信息的文件路径
        :return: 包含场地信息的字典
        """
        court_dict = {}
        with open(court_file_path, 'r') as f:
            for line in f:
                if line.startswith('#'):
                    # 跳过注释行
                    continue
                fields = line.strip().split(',')
                if len(fields) < 3:
                    # 数据不完整
                    continue
                name = fields[0].strip()
                available = fields[1].strip().lower() == 'true'
                xpath = self.get_xpath(fields[2].strip())
                if xpath is None:
                    # 无法找到xpath路径
                    continue
                court_dict[name] = {'available': available, 'xpath': xpath}
        return court_dict


