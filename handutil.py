import cv2
import mediapipe as mp


class HandDetector():
    '''
    手勢識別類
    '''
    def __init__(self, mode=False, max_hands=2,modelC=1 ,detection_con=0.5, track_con=0.5):
        '''
        初始化
        :param mode: 是否靜態圖片，預設為False
        :param max_hands: 最多幾隻手，預設為2只
        :param detection_con: 最小檢測信度值，預設為0.5
        :param track_con: 最小跟蹤信度值，預設為0.5
        :param modelC: 好像是新的函數，不加不行
        '''
        self.mode = mode
        self.max_hands = max_hands
        self.detection_con = detection_con
        self.modelC = modelC
        self.track_con = track_con

        self.hands = mp.solutions.hands.Hands(self.mode, self.max_hands,self.modelC ,self.detection_con, self.track_con)

    def find_hands(self, img, draw=True):
        '''
        檢測手勢
        :param img: 影片幀圖片
        :param draw: 是否畫出手勢中的節點和連線圖
        :return: 處理過的影片幀圖片
        '''
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # 處理圖片，檢測是否有手勢，將資料存進self.results中
        self.results = self.hands.process(imgRGB)
        if draw:
            if self.results.multi_hand_landmarks:
                for handlms in self.results.multi_hand_landmarks:
                    mp.solutions.drawing_utils.draw_landmarks(img, handlms, mp.solutions.hands.HAND_CONNECTIONS)
        return img

    def find_positions(self, img, hand_no=0):
        '''
        獲取手勢資料
        :param img: 影片幀圖片
        :param hand_no: 手編號（預設第1隻手）
        :return: 手勢資料列表，每個資料成員由id, x, y組成，程式碼這個手勢位置編號以及在螢幕中的位置
        '''
        self.lmslist = []
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[hand_no]
            for id, lm in enumerate(hand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmslist.append([id, cx, cy])

        return self.lmslist