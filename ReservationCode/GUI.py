import csv
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QGridLayout,QLabel


class CourtSelection(QWidget):

    def __init__(self, dict_path):
        super().__init__()
        self.selected_court_1 = None
        self.selected_court_2 = None
        self.dict_path = dict_path

        # 设置背景颜色
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.white)
        self.setPalette(p)

        # 初始化40个按钮
        self.buttons = {}
        for i in range(15, 20):
            for j in range(1, 9):
                key = f"{i}_{j}"
                button = QPushButton(key, self)
                button.setFixedSize(100, 100)
                button.setStyleSheet("background-color: black")
                self.buttons[key] = button

        # 添加时间段和日期注释
        # 布局
        self.grid = QGridLayout()
        for i in range(15, 20):
            for j in range(1, 9):
                key = f"{i}_{j}"
                button = self.buttons[key]
                self.grid.addWidget(button, i-14, j)
                button.clicked.connect(self.handle_button_click)
        self.setLayout(self.grid)
        time_labels = ['时间段', '15:30-16:30', '16:30-17:30', '17:30-18:30', '18:30-19:30', '19:30-20:30']
        day_labels = ['时间段', '1号', '2号', '3号', '4号', '5号', '6号', '7号', '8号']
        for i, label in enumerate(time_labels):
            time_label = QLabel(label, self)
            time_label.setStyleSheet("background-color: white; color: black;")
            time_label.setAlignment(Qt.AlignCenter)
            self.grid.addWidget(time_label, i, 0)
        for i, label in enumerate(day_labels):
            day_label = QLabel(label, self)
            day_label.setStyleSheet("background-color: white; color: black;")
            day_label.setAlignment(Qt.AlignCenter)
            self.grid.addWidget(day_label, 0, i)

        

        # 读取场地字典信息
        self.court_dict = {}
        self.read_dict()

       
        # 设置窗口标题和字体颜色
        self.setWindowTitle('Court Selection')
        self.setStyleSheet("color: black; background-color: white")
        self.show()

    def read_dict(self):

        # 读取场地字典信息
        with open(self.dict_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            self.court_dict = {row[0]: row[1] for row in reader}

    def handle_button_click(self):
        button = self.sender()
        key = button.text()
        # 只能点击一次
        if button.isEnabled():
            button.setStyleSheet("background-color: red")
            button.setEnabled(False)

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
    
    


    
