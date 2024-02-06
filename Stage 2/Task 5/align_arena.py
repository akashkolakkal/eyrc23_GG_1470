import numpy as np
import cv2
import matplotlib.pyplot as plt
import pyperclip
from pathlib import Path


def onclick(event):
    coords = [event.xdata, event.ydata]
    print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          (event.button, event.x, event.y, event.xdata, event.ydata))
    pyperclip.copy(str(coords))


def helper_arena():
    cap = cv2.VideoCapture(2)
    cap.set(3, 1920)
    cap.set(4, 1080)
    # cap.set(cv2.CAP_PROP_FPS, 30)
    # cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

    # cap.set(cv2.CAP_PROP_AUTO_WB, 0)
    # cap.set(cv2.CAP_PROP_WB_TEMPERATURE, 100)

    for _ in range(30):
        ret, frame = cap.read()

    while cap.isOpened():

        ret, frame = cap.read()

        if not ret:
            print("Failed to capture frame.")

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        fig, ax = plt.subplots()
        ax.imshow(frame)
        cid = fig.canvas.mpl_connect('button_press_event', onclick)

        plt.axis("off")
        plt.show()

        actual = np.float32([[605, 17], [1617, 9], [1645, 1053], [573, 1031]])
        # input("Press Enter to continue...")


if __name__ == "__main__":
    helper_arena()
