import numpy as np
import cv2
import matplotlib.pyplot as plt

def helper_arena():
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    cap.set(3, 1920)
    cap.set(4, 1080)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

    for _ in range(30):
        ret, frame = cap.read()
    
    ret, frame = cap.read()

    if not ret:
        print("Failed to capture frame.")
    
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    plt.imshow(frame)
    plt.axis("off")
    plt.show()

    actual = np.float32([[396, 6], [1385, 77], [1392, 1065], [313, 1063]])

helper_arena()