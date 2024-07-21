import cv2
import numpy as np

def process_frame(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, binary = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)
    edges = cv2.Canny(binary, 50, 150)

    height, width = edges.shape
    mask = np.zeros_like(edges)
    mask[height // 2:] = edges[height // 2:]
    lines = cv2.HoughLinesP(mask, 1, np.pi / 180, 50, minLineLength=100, maxLineGap=50)

    steering_angle = 0
    if lines is not None:
        x1, y1, x2, y2 = lines[0][0]
        steering_angle = (x1 - width // 2) / (width // 2)

    return steering_angle, edges

def get_frame_from_camera(camera_index=0):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        raise Exception("Could not open video device")
    
    ret, frame = cap.read()
    cap.release()
    if not ret:
        raise Exception("Could not read frame")

    return frame

