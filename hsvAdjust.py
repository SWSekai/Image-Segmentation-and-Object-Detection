import cv2
import numpy as np

def hsv_adjust(image_path):
    """
        使用滑桿調整影像的HSV值，並顯示調整後的影像。
    """
    windowName = "HSV Adjustments"
    
    img = cv2.imread(image_path)
    if img is None:
        print(f"無法載入影像: {image_path}")
        return
    
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) # 轉換到HSV色彩空間
    cv2.namedWindow(windowName)
    
    # 創建滑桿
    cv2.createTrackbar("Lower Hue", windowName, 0, 179, nothing) # 色相範圍0-179，createTrackerbart傳入參數()
    cv2.createTrackbar("Upper Hue", windowName, 0, 179, nothing)
    cv2.createTrackbar("Lower Saturation", windowName, 0, 255, nothing) # 飽和度範圍0-255
    cv2.createTrackbar("Upper Saturation", windowName, 0, 255, nothing)
    cv2.createTrackbar("Lower Value", windowName, 0, 255, nothing) # 明度範圍0-255
    cv2.createTrackbar("Upper Value", windowName, 0, 255, nothing)
    
    cv2.setTrackbarPos("Lower Hue", windowName, 0)
    cv2.setTrackbarPos("Upper Hue", windowName, 179)
    cv2.setTrackbarPos("Lower Saturation", windowName, 0)
    cv2.setTrackbarPos("Upper Saturation", windowName, 255)
    cv2.setTrackbarPos("Lower Value", windowName, 0)
    cv2.setTrackbarPos("Upper Value", windowName, 255)
    
    while True:
        lower_hue = cv2.getTrackbarPos("Lower Hue", windowName)
        upper_hue = cv2.getTrackbarPos("Upper Hue", windowName)
        lower_saturation = cv2.getTrackbarPos("Lower Saturation", windowName)
        upper_saturation = cv2.getTrackbarPos("Upper Saturation", windowName)
        lower_value = cv2.getTrackbarPos("Lower Value", windowName)
        upper_value = cv2.getTrackbarPos("Upper Value", windowName)

        img_adjust_target = cv2.inRange(img_hsv,
                                 (lower_hue, lower_saturation, lower_value),
                                 (upper_hue, upper_saturation, upper_value))
        img_adjust = cv2.bitwise_and(img, img, mask=img_adjust_target)
        
        cv2.imshow(windowName, img_adjust)
        if cv2.waitKey(1) == 27:  # 按 'ESC' 鍵退出
            return img_adjust


def nothing(x):
    pass
    
                
    
if __name__ == "__main__":
    for i in range(1, 3):
        image = f"./image/image{i}.jpg"
        hsv_adjust(image)