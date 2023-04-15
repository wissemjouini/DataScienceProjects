# Hand Finger Detection and Counting
This script uses computer vision to detect and count the number of fingers held up by the user's hand. It utilizes the MediaPipe library for hand detection and landmark tracking.

## Requirements
To run this script, you will need to install the following libraries:

OpenCV
MediaPipe
You can install them using pip by running:
pip install opencv-python mediapipe

## Usage
To run the script, simply execute the hand_finger_detection.py file. The script will access your webcam to detect your hand and count your fingers. Hold your hand up in front of the camera and try moving your fingers to see the count change in real-time.

You can exit the script by pressing the 'q' key.

## Notes
The script can detect up to two hands at a time.
The finger counting algorithm is based on the position of certain landmarks on the hand, and may not always be accurate.
If the script fails to run, make sure that your webcam is properly connected and configured.
