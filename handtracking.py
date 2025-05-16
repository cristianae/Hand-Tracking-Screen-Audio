import cv2 #for webcam video capture
import mediapipe #real time hand tracking
import math
import numpy as np #used for volume control
from subprocess import call #used to change volume on mac os

handSolution = mediapipe.solutions.hands #hand detection
hand = handSolution.Hands() #creating an object of hands class
videoCap= cv2.VideoCapture(0) #0 is the default camera, opens the webcam
quitapplication = False
min = 30
max = 200
brightness = 1.0

if not videoCap.isOpened():
    print("Camera is not opening. ")
    exit()

print("Camera opened successfully")

def mouseClick(event, x, y, flags, param):
    global quitapplication
    if event == cv2.EVENT_LBUTTONDOWN: #if left mouse button is clicked
        if 10 <= x <= 110 and 10 <= y <= 50: 
            quitapplication = True #set quitapplication to true

cv2.namedWindow("My Camera") 
cv2.setMouseCallback("My Camera", mouseClick) #set mouse callback function

#note: ulti_hand_landmarks is for hand landmarks while multi_handedness is for multiple hands

while True:
    success, img= videoCap.read() #reading image, which returns an array of pixel values 
    if not success:
        break
    movement = hand.process(img) #process the image
    
    if movement.multi_hand_landmarks and movement.multi_handedness: 
        for i, handLandmarks in enumerate(movement.multi_hand_landmarks):
            label = movement.multi_handedness[i].classification[0].label  #"Left" or "Right"

            for id, lm in enumerate(handLandmarks.landmark):
                h, w, c = img.shape #height, width, channels of image
                cx, cy = int(lm.x * w), int(lm.y * h)
                if id == 4:
                    cv2.circle(img, (cx, cy), 8, (255, 0, 0), cv2.FILLED)  # Blue = Thumb tip
                elif id == 8:
                    cv2.circle(img, (cx, cy), 8, (0, 255, 0), cv2.FILLED)  # Green = Index tip
                else:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)  # Magenta = others

            thumb = handLandmarks.landmark[4] #thumb landmark
            index = handLandmarks.landmark[8] #index finger landmark
            thumb_x, thumb_y = int(thumb.x * w), int(thumb.y * h) #turning the float values into integers
            index_x, index_y = int(index.x * w), int(index.y * h)
            distance = math.sqrt((index_x- thumb_x)**2 + (index_y-thumb_y)** 2)#distance between thumb and index finger for volume control
            
            min = np.minimum(distance + 50, min)
            max = np.maximum(distance, max)

            if label == "Left": #if left hand is detected
                volume = np.clip((distance - min) / (max - min) * 100, 0, 100)
                #change volume on mac os
                call(["osascript", "-e", "set volume output volume {}".format(int(volume))]) 
                
            
            elif label == "Right": #if right hand is detected
                brightness = np.clip((distance - min) / (max - min), 0, 1.0)
                copydisplay = img.copy()
                alpha= 1.0 - brightness

                cv2.rectangle(copydisplay, (0, 0), (img.shape[1], img.shape[0]), (0, 0, 0), -1)
                cv2.addWeighted(copydisplay, alpha, img, 1 - alpha, 0, img)
            
            cv2.putText(img, f'Volume: {int(volume)}%', (15, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(img, f'Brightness: {int(brightness * 100)}%', (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
        
    cv2.rectangle(img, (10, 10), (110, 50), (0, 0, 255), -1)
    cv2.putText(img, 'QUIT', (25, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("My Camera", img) #showing the camera feed
    cv2.waitKey(1) #1 millisecond delay, for real time processing

    if quitapplication: 
        break
       

videoCap.release()
cv2.destroyAllWindows()