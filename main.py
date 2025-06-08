import cv2
import numpy as np

from hsvAdjust import hsv_adjust

def detect_and_draw_desktops(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print(f"無法載入影像: {image_path}")
        return

    output_img = img.copy()

    # 桌面HSV範圍
    img = hsv_adjust(image_path)
    if img is None:
        print("無法獲取HSV範圍，請先調整HSV值。")
        return
    
    # 形態學
    kernel = np.ones((5,5),np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

    # 尋找輪廓
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 矩形桌面
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 500:  # 過濾小物體
            continue

        # 近似多邊形
        epsilon = 0.02 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)

        # 尋找矩形(4個頂點)
        if len(approx) == 4:
            # 檢查外接矩形的長寬比
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = float(w)/h
            # 長寬比範圍
            if 0.5 < aspect_ratio < 5.0:
                # 繪製邊界框
                cv2.rectangle(output_img, (x, y), (x + w, y + h), (255, 0, 0), 2)

                # 標示桌角
                for point in approx:
                    cv2.circle(output_img, tuple(point[0]), 5, (0, 0, 255), -1)


    # 顯示結果
    cv2.imshow("Detected Desktops", output_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # 儲存結果 (您可以將儲存路徑修改為您需要的位置)
    # cv2.imwrite(f"./image/image2Result.jpg", output_img)
    
if __name__ == "__main__":
    for i in range(1, 3):
        image = f"./image/image{i}.jpg"
        print(f"處理圖像:image{i}...")
        detect_and_draw_desktops(image)
