import numpy as np
import cv2
import matplotlib.pyplot as plt
import pyperclip
from utilities import get_arena

def onclick(event):
    coords = [event.xdata, event.ydata]
    print('button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
          (event.button, event.x, event.y, event.xdata, event.ydata))
    pyperclip.copy(str(coords))


def helper_arena():
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    cap.set(3, 1920)
    cap.set(4, 1080)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

    for _ in range(30):
        ret, frame = cap.read()
    
    ret, frame = cap.read()
    frame = get_arena(frame)

    if not ret:
        print("Failed to capture frame.")
    
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    fig, ax = plt.subplots()
    ax.imshow(frame)
    cid = fig.canvas.mpl_connect('button_press_event', onclick)

    plt.axis("off")
    plt.show()

    actual = np.float32([[382, 47], [1362, 39], [1419, 1043], [345, 1075]])

if __name__ == "__main__":
    helper_arena()


# "A": (300, 900),
# "B": (750, 670),
# "C": (750, 470),
# "D": (300, 475),
# "E": (300, 130)