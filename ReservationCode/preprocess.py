import cv2
import numpy as np

class ImagePreprocessor:
    
    def __init__(self):
        pass
    
    def preprocess_image(self, image_path):
        img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        # 图像增强
        clahe = cv2.createCLAHE(clipLimit=2, tileGridSize=(9,9))
        img = clahe.apply(img)
        # 二值化
        _, img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        # 去噪和填充空洞
        kernel = np.ones((1,1), np.uint8)
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        # 滤波操作代码
        img = cv2.GaussianBlur(img, (3, 3), 0)
        img = cv2.blur(img, (1, 1))
        img = cv2.medianBlur(img, 5)  
        # 将数字放大到合适的尺寸
        img = cv2.resize(img, (0,0), fx=3.5, fy=3.5, interpolation=cv2.INTER_CUBIC)
        # 返回处理后的图片
        return img
