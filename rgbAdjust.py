import cv2
import numpy as np

def rgbAdjust(image_path):
    """
        使用滑桿決定RGB空間的上下限，以獲得一定顏色的區域。
        像素只要其中一個顏色通道不在設定數值範圍內，則此像素一律為黑。
    """
    windowName = "RGB Color Region Selection"

    img = cv2.imread(image_path)
    if img is None:
        print(f"無法載入影像: {image_path}")
        return

    cv2.namedWindow(windowName)

    # 創建滑桿來設定RGB的下限和上限
    cv2.createTrackbar("Lower Red", windowName, 0, 255, nothing)
    cv2.createTrackbar("Upper Red", windowName, 255, 255, nothing)
    cv2.createTrackbar("Lower Green", windowName, 0, 255, nothing)
    cv2.createTrackbar("Upper Green", windowName, 255, 255, nothing)
    cv2.createTrackbar("Lower Blue", windowName, 0, 255, nothing)
    cv2.createTrackbar("Upper Blue", windowName, 255, 255, nothing)

    while True:
        # 獲取滑桿的位置
        lower_red = cv2.getTrackbarPos("Lower Red", windowName)
        upper_red = cv2.getTrackbarPos("Upper Red", windowName)
        lower_green = cv2.getTrackbarPos("Lower Green", windowName)
        upper_green = cv2.getTrackbarPos("Upper Green", windowName)
        lower_blue = cv2.getTrackbarPos("Lower Blue", windowName)
        upper_blue = cv2.getTrackbarPos("Upper Blue", windowName)

        # 確保上限不小於下限
        lower_red = min(lower_red, upper_red)
        lower_green = min(lower_green, upper_green)
        lower_blue = min(lower_blue, upper_blue)

        cv2.setTrackbarPos("Lower Red", windowName, lower_red)
        cv2.setTrackbarPos("Lower Green", windowName, lower_green)
        cv2.setTrackbarPos("Lower Blue", windowName, lower_blue)

        # 建立顏色範圍的下限和上限
        lower_bound = np.array([lower_blue, lower_green, lower_red])
        upper_bound = np.array([upper_blue, upper_green, upper_red])

        # 根據顏色範圍創建遮罩
        # cv2.inRange 函式會檢查影像中每個像素的 BGR 值是否在 lower_bound 和 upper_bound 之間
        # 如果在範圍內，對應的遮罩像素值為255（白色），否則為0（黑色）
        mask = cv2.inRange(img, lower_bound, upper_bound)

        # 將原始影像與遮罩進行位元 AND 運算
        # 這樣只有在遮罩中為白色的像素（即在顏色範圍內的像素）才會保留原始影像的顏色
        # 遮罩中為黑色的像素（即不在顏色範圍內的像素）在結果影像中會變成黑色
        result_img = cv2.bitwise_and(img, img, mask=mask)

        cv2.imshow(windowName, result_img)

        if cv2.waitKey(1) == 27:  # 按 'ESC' 鍵退出
            return result_img

def nothing(x):
    pass

if __name__ == "__main__":
    # 確保您有這些圖片路徑，否則會報錯
    for i in range(1, 3):
        image = f"./image/image{i}.jpg"
        rgbAdjust(image)