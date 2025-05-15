import cv2 
import mediapipe 

handSolution = mediapipe.solutions.hands #importing mediapipe library
hand = handSolution.Hands() #creating an object of hands class
videoCap= cv2.VideoCapture(0) #0 is the default camera

if not videoCap.isOpened():
    print("Camera is not opening. ")
    exit()

print("Camera opened successfully")

if cv2.waitKey(1) & 0xFF == ord('q'):
    print("Exiting the application.")
    exit()


while True:
    success, img= videoCap.read() #reading image, which returns an array of pixel values 
    if success:
        movement = hand.process(img) #process the image
        if movement.multi_hand_landmarks: #if hand is detected
            for handLandmarks in movement.multi_hand_landmarks: #for each hand detected
                for id, lm in enumerate(handLandmarks.landmark): #enumerate gives index and value
                    h, w, c = img.shape #height, width, channels of image
                    cx, cy = int(lm.x * w), int(lm.y * h) #x and y coordinates of hand landmarks
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED) #draw circle on hand landmarks
        cv2.imshow("CamOutput", img) #showing image on separate window
        cv2.waitKey(1) #wait for 1ms


 