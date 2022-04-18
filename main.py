import cv2
from handutil import HandDetector
import api
import os

# 開啟攝像頭
cap = cv2.VideoCapture(0)
# 建立一個手勢識別物件
detector = HandDetector()

# 6個command，分別代表0～5
finger_command_list = [
    'command 0',
    'command 1',
    'command 2',
    'command 3',
    'command 4',
    'command 5',
]
finger_command = 9
count = 0

# 指尖列表，分別代表大拇指、食指、中指、無名指和小指的指尖
tip_ids = [4, 8, 12, 16, 20]
command_temp = []
while True:
    success, img = cap.read()

    if success:
        # 檢測手勢
        img = detector.find_hands(img, draw=True)
        # 獲取手勢資料
        lmslist = detector.find_positions(img)
        if len(lmslist) > 0:
            fingers = []
            for tid in tip_ids:
                # 找到每個指尖的位置
                x, y = lmslist[tid][1], lmslist[tid][2]
                cv2.circle(img, (x, y), 10, (0, 255, 0), cv2.FILLED)
                # 如果是大拇指，如果大拇指指尖x位置大於大拇指第二關節的位置，則認為大拇指開啟，否則認為大拇指關閉
                if tid == 4:
                    if lmslist[tid][1] > lmslist[tid - 1][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                # 如果是其他手指，如果這些手指的指尖的y位置大於第二關節的位置，則認為這個手指開啟，否則認為這個手指關閉
                else:
                    if lmslist[tid][2] < lmslist[tid - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
            # fingers是這樣一個列表，5個數據，0代表一個手指關閉，1代表一個手指開啟
            # 判斷有幾個手指開啟
            cnt = fingers.count(1)
            # 找到對應的手勢並回傳command，順便檢查有沒有雜訊
            finger_command = finger_command_list[cnt]
            command_temp.append(finger_command)
            if len(command_temp) == 5:
                command_check = command_temp.count(command_temp[0]) == len(command_temp)
                if command_check:
                    if command_temp[2] == "command 4":
                        cv2.imwrite("D:\GestureRecognitionControl\Backend\images\\frame%d.jpg" % count, img)
                        filename = "frame%d.jpg" % count
                        api.readCommand.readMsg(command_temp[2],filename)
                        # print(f"Success! filename: {filename}")
                        count+=1
                    else:
                        pass
                    command_temp = []
                else:
                    command_temp = []

        cv2.imshow('Image', img)

    k = cv2.waitKey(1)
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()