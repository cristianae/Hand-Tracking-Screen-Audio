# Hand Gesture-Controlled Volume and Brightness Control (for macOS)

## Description
This is a Python-based project that uses your webcam and the MediaPipe library to detect hand gestures in real time.
- Use your **right hand** to adjust your volume 🔊 by adjusting the distance between your thumb and index finger.
- Use your **left hand** to adjust your screen brightness 💡 by adjusting the distance between your thumb and index finger.

## How to run the project
1. Clone the repo or dowload the handtracking.py file
2. In your terminal navigate to the project folder
3. Run the following line: python3 handtracking.py

# Author:
Cristiana Eagen


## Built with:
- OpenCV
- MediaPipe

## Features 
- It gives real-time feed for hand landmark tracking though the user's default webcam
- It distinguishes between **left** and **right** hand
- Adjusts volume using AppleScript (macOS only)
- Dims your video feed by simulating the brightness control
- Click the **"QUIT" button** on the screen to exit

## Requirements:
- Python 3.x
- macOS (for volume control with `osascript`)

