import cv2 #for webcam video capture
import mediapipe #real time hand tracking

handSolution = mediapipe.solutions.hands #hand detection
hand = handSolution.Hands() #creating an object of hands class
videoCap= cv2.VideoCapture(0) #0 is the default camera, opens the webcam
quitapplication = False

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

while True:
    success, img= videoCap.read() #reading image, which returns an array of pixel values 
    if not success:
        break
    movement = hand.process(img) #process the image
    if movement.multi_hand_landmarks: #if hand is detected
        for handLandmarks in movement.multi_hand_landmarks: #for each hand detected
            for id, lm in enumerate(handLandmarks.landmark): #enumerate gives index and value
                h, w, c = img.shape #height, width, channels of image
                cx, cy = int(lm.x * w), int(lm.y * h) #x and y coordinates of hand landmarks
                cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED) #draw circle on hand landmarks
        
    cv2.rectangle(img, (10, 10), (110, 50), (0, 0, 255), -1)
    cv2.putText(img, 'QUIT', (25, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("My Camera", img) #showing the camera feed
    cv2.waitKey(1) #1 millisecond delay, for real time processing
    if quitapplication: 
        break
       

videoCap.release()
cv2.destroyAllWindows()