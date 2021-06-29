import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import math
from enum import IntEnum
pyautogui.FAILSAFE = False

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

class Gest(IntEnum):
    FIST = 0
    PINKY = 1
    RING = 2
    MID = 4
    INDEX = 8
    THUMB = 16
    PALM = 31
    FIRST2 = 12



class Hand_Recog:
    finger = 0
    
    #def render_vector(frame, hand_results):
    #    points = [[8,0],[12,0]]
    #    for point in points:
    #        s_cord = (int(hand_results.landmark[point[0]].x * Gest_Ctrl.CAM_WIDTH), int(hand_results.landmark[point[0]].y * Gest_Ctrl.CAM_HEIGHT))
    #        e_cord = (int(hand_results.landmark[point[1]].x * Gest_Ctrl.CAM_WIDTH), int(hand_results.landmark[point[1]].y * Gest_Ctrl.CAM_HEIGHT))
    #        frame = cv2.line(frame, s_cord, e_cord, (0,255,150), 9)
    #    return frame
    def get_dist(point):
        dist = (Gest_Ctrl.hand_result.landmark[point[0]].x - Gest_Ctrl.hand_result.landmark[point[1]].x)**2
        dist += (Gest_Ctrl.hand_result.landmark[point[0]].y - Gest_Ctrl.hand_result.landmark[point[1]].y)**2
        dist = math.sqrt(dist)
        return dist

    def render_finger_state(frame):
        points = [[8,5,0],[12,9,0],[16,13,0],[20,17,0]]
        label = ["dist_ratio :"]
        Hand_Recog.finger = 0
        Hand_Recog.finger = Hand_Recog.finger | 0 #thumb
        for idx,point in enumerate(points):
            
            dist = Hand_Recog.get_dist(point[:2])
            dist2 = Hand_Recog.get_dist(point[1:])
            
            try:
                ratio = round(dist/dist2,1)
                Hand_Recog.finger = Hand_Recog.finger << 1
                if ratio > 0.5 :
                    Hand_Recog.finger = Hand_Recog.finger | 1
                label[0] += str(ratio) + ','
            except:
                label[0] += "Division by 0"
        
        frame = cv2.putText(frame, label[0], (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)
        #frame = cv2.putText(frame, fingstr, (10,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA)
        
        return frame

    def get_gesture(frame):
        #if Gest.FIST == Hand_Recog.finger:
        #    return 0
        #if Gest.PALM == Hand_Recog.finger:
        #    return 0
        print("gest ", Hand_Recog.finger)
        if Gest.FIRST2 == Hand_Recog.finger :
            point = [[8,12],[5,9]]
            dist1 = Hand_Recog.get_dist(point[0])
            dist2 = Hand_Recog.get_dist(point[1])
            ratio = dist1/dist2
            frame = cv2.putText(frame, "ratio :" + str(ratio), (10,150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 1, cv2.LINE_AA)
        frame = cv2.putText(frame, "gest "+str(Hand_Recog.finger), (10,200), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 1, cv2.LINE_AA)
        return frame


#class Mouse:
#    def __init__(self):
#        self.tx_old = 0
#        self.ty_old = 0
#        self.trial = true
#        self.flag = 0
        
#    def move_mouse(self, gesture):
        
#        point = 9
#        position = [hand_results.landmark[point].x , hand_results.landmark[point].y]

#        (sx,sy)=pyautogui.size()
#        (camx,camy) = (frame.shape[:2][0],frame.shape[:2][1])
#        (mx_old,my_old) = pyautogui.position()
        
        
#        damping = 2 # hyperparameter we will have to adjust
#        tx = position[0]
#        ty = position[1]
#        if self.trial:
#            self.trial, self.tx_old, self.ty_old = false, tx, ty
        
#        delta_tx = tx - self.tx_old
#        delta_ty = ty - self.ty_old
#        self.tx_old,self.ty_old = tx,ty
        
#        if (gesture == 3):
#            self.flag = 0
#            mx = mx_old + (delta_tx*sx) // (camx*damping)
#            my = my_old + (delta_ty*sy) // (camy*damping)            
#            pyautogui.moveto(mx,my, duration = 0.1)

#        elif(gesture == gesture.T):
#            if self.flag == 0:
#                pyautogui.doubleclick()
#                self.flag = 1
#        elif(gesture == 1):
#            print('1 finger open')

        



class Gest_Ctrl:
    gc_mode = 0
    cap = None
    CAM_HEIGHT = None
    CAM_WIDTH = None
    hand_result = None

    def __init__(self):
        Gest_Ctrl.gc_mode = 1
        Gest_Ctrl.cap = cv2.VideoCapture(0)
        Gest_Ctrl.CAM_HEIGHT = Gest_Ctrl.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        Gest_Ctrl.CAM_WIDTH = Gest_Ctrl.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        
    def move_mouse(self):
        point = 9
        position = [Gest_Ctrl.hand_result.landmark[point].x ,Gest_Ctrl.hand_result.landmark[point].y]
        (sx,sy)=pyautogui.size()
        (mx_old,my_old) = pyautogui.position()
        tx = position[0]
        ty = position[1]
        pyautogui.moveTo(int(sx*tx), int(sy*ty), duration = 0.1)


    def calculate_position(self):
        final_x = (Gest_Ctrl.hand_result.landmark[8].x +  Gest_Ctrl.hand_result.landmark[12].x)/2
        final_y = (Gest_Ctrl.hand_result.landmark[8].y +  Gest_Ctrl.hand_result.landmark[12].y)/2
        return [final_x,final_y]
    
    def ShowLocation(self):
        try:
            print(Gest_Ctrl.hand_result.landmark[12].z)
        except:
            print('Hi')
    
    def start(self):
        with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
            while Gest_Ctrl.cap.isOpened() and Gest_Ctrl.gc_mode:
                success, image = Gest_Ctrl.cap.read()
                if not success:
                    print("Ignoring empty camera frame.")
                    continue

                image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
                image.flags.writeable = False
                results = hands.process(image)
                image.flags.writeable = True
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
                if results.multi_hand_landmarks:
                    Gest_Ctrl.hand_result = results.multi_hand_landmarks[0]
                    pos = self.calculate_position()
                    self.move_mouse()
                    ##hand
                    image = Hand_Recog.render_finger_state(image)
                    image = Hand_Recog.get_gesture(image)
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                cv2.imshow('MediaPipe Hands', image)
                if cv2.waitKey(5) & 0xFF == 13:
                    break
        Gest_Ctrl.cap.release()
        cv2.destroyAllWindows()

gc1 = Gest_Ctrl()
gc1.start()

