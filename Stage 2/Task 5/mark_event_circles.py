from utilities import get_arena
import cv2
import matplotlib.pyplot as plt
import numpy as np
import pyperclip


cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cap.set(3, 1920)
cap.set(4, 1080)
cap.set(cv2.CAP_PROP_FPS, 30)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

cap.set(cv2.CAP_PROP_AUTO_WB, 0)

ret, image = cap.read()

image = get_arena(image)


cv2.circle(image, (300, 130), 100, (0, 0, 255), 5)
cv2.circle(image, (750, 670), 100, (0, 0, 255), 5)
cv2.circle(image, (300, 475), 100, (0, 0, 255), 5)
cv2.circle(image, (750, 470), 100, (0, 0, 255), 5)
cv2.circle(image, (300, 900), 100, (0, 0, 255), 5)


plt.imshow(image)
plt.axis("off")
plt.show()

        # "A": (300, 900),
        # "B": (750, 670),
        # "C": (750, 470),
        # "D": (300, 475),
        # "E": (300, 130)