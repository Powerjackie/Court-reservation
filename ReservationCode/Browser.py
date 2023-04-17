import time
import threading
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options


# 初始化与关闭浏览器实例
class Browser:
    _driver = None
    _lock = threading.Lock()

    @classmethod
    def get_driver(cls, executable_path, binary_location, IMPLICIT_TIME,WAIT_TIME,headless):
        with cls._lock:
            try:
                if cls._driver is None:
                    start_time = time.time()
                    service = Service(executable_path=executable_path)
                    options = Options()
                    options.binary_location = binary_location
                    options.use_chromium = True
                    options.add_argument("--disable-usb-keyboard-detect")
                    options.add_argument("--disable-extensions")
                    if headless:
                        options.add_argument("--headless")
                    cls._driver = webdriver.Edge(service=service, options=options)
                    wait = WebDriverWait(cls._driver, WAIT_TIME)
                    cls._driver.implicitly_wait(IMPLICIT_TIME)  # 设置隐式等待时间
                    end_time = time.time()
                    print("Browser started in {:.2f} seconds".format(end_time - start_time))
            
            except Exception as e:
                print(f"Error creating driver: {e}")

        return cls._driver

    @classmethod
    def close_browser(cls):
        if cls._driver is not None:
            try:
                cls._driver.quit()
                cls._driver = None
            except Exception as e:
                print(f"Error closing browser: {e}")
