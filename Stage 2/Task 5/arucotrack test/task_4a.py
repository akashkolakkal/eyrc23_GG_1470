'''
*****************************************************************************************
*
*        		===============================================
*           		Geo Guide (GG) Theme (eYRC 2023-24)
*        		===============================================
*
*  This script is to implement Task 4A of Geo Guide (GG) Theme (eYRC 2023-24).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			1470
# Author List:		Parth Jain, Anikesh Kulal, Akash Kolakkal, Keshav Jha
# Filename:			task_4a.py


####################### IMPORT MODULES #######################
import cv2
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.python.keras.layers import Dense, Flatten
from keras.models import Sequential
from utilities import get_arena

##############################################################


################# ADD UTILITY FUNCTIONS HERE #################

"""
You are allowed to add any number of functions to this code.
"""


def plot_point(img, x, y, color=(0, 255, 255)):
    return cv2.circle(img, (x, y), radius=20, color=color, thickness=-1)

def classify_event(image, loaded_model) -> str:

    class_names = ['combat', 'destroyed_buildings', 'fire', 'human_aid_rehabilitation', 'military_vehicles', 'None']
    
    image = np.expand_dims(image,axis=0)
    pred = loaded_model.predict(image, verbose=0)

    event = class_names[np.argmax(pred)]

    return event

# def get_arena(img):
#     actual = np.float32([[382, 47], [1362, 39], [1419, 1043], [345, 1075]])
#     should_be = np.float32([[0, 0], [1080, 0], [1080, 1080], [0, 1080]])

#     img = cv2.rotate(img, cv2.ROTATE_180)

#     pers_M = cv2.getPerspectiveTransform(actual, should_be)
#     rows,cols,ch = img.shape

#     img = cv2.warpPerspective(img, pers_M, (cols,rows))

#     return img[:, :1080]

def helper_arena():
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    cap.set(3, 1920)
    cap.set(4, 1080)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc(*'MJPG'))

    for _ in range(30):
        ret, frame = cap.read()

    ret, frame = cap.read()

    img = cv2.rotate(frame, cv2.ROTATE_180)
    cv2.imshow("ArUco Marker Detection", img)
    cv2.waitkey(0)

    actual = np.float32([[474, 14], [1489, 0], [1517, 1038], [454, 1034]])

def test_images():
    img = cv2.imread('sample3.jpg')
    img = get_arena(img)

    plt.imshow(img)
    plt.axis("off")
    plt.show()


    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    plt.subplot(1, 5, 1)
    y1, x1 = 235, 929
    plt.imshow(img[x1: x1 + 70, y1: y1 + 70])
    plt.axis("off")

    plt.subplot(1, 5, 2)
    y2, x2 = 708, 727
    plt.imshow(img[x2: x2 + 70, y2: y2 + 70])
    plt.axis("off")

    plt.subplot(1, 5, 3)
    y3, x3 = 716, 521
    plt.imshow(img[x3: x3 + 70, y3: y3 + 70])
    plt.axis("off")

    plt.subplot(1, 5, 4)
    y4, x4 = 222, 519
    plt.imshow(img[x4: x4 + 70, y4: y4 + 70])
    plt.axis("off")

    plt.subplot(1, 5, 5)
    y5, x5 = 242, 185
    plt.imshow(img[x5: x5 + 70, y5: y5 + 70])
    plt.axis("off")

    plt.show()

def process_test_images(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    laplacian = cv2.Laplacian(gray, cv2.CV_64F)

    laplacian = np.uint8(np.absolute(laplacian))

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.1, 0, 255)
    image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)


    image = cv2.fastNlMeansDenoisingColored(image, h=5, templateWindowSize=2, searchWindowSize=25)

    image = cv2.resize(image, (80, 80))

    return image

##############################################################


# def task_4a_return():
def return_labels_dict():
    """
    Purpose:
    ---
    Only for returning the final dictionary variable

    Arguments:
    ---
    You are not allowed to define any input arguments for this function. You can 
    return the dictionary from a user-defined function and just call the 
    function here

    Returns:
    ---
    `identified_labels` : { dictionary }
        dictionary containing the labels of the events detected
    """

############## ADD YOUR CODE HERE	##############
    
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

    img = get_arena(frame)

    y1, x1 = 235, 929
    y2, x2 = 708, 727
    y3, x3 = 716, 521
    y4, x4 = 222, 519
    y5, x5 = 242, 185


    img_A = process_test_images(img[x1: x1 + 70, y1: y1 + 70])
    img_B = process_test_images(img[x2: x2 + 70, y2: y2 + 70])
    img_C = process_test_images(img[x3: x3 + 70, y3: y3 + 70])
    img_D = process_test_images(img[x4: x4 + 70, y4: y4 + 70])
    img_E = process_test_images(img[x5: x5 + 70, y5: y5 + 70])


    loaded_model = Sequential()
    pretrained_model = tf.keras.applications.VGG19(
    include_top=False,
    input_shape=(80, 80, 3),
    pooling='avg',
    classes=6,
    weights='imagenet'
    )
    for layer in pretrained_model.layers:
        layer.trainable = False

    loaded_model.add(pretrained_model)
    loaded_model.add(Flatten())
    loaded_model.add(Dense(1024, activation='relu'))
    loaded_model.add(Dense(512, activation='relu'))
    loaded_model.add(Dense(512, activation='relu'))
    loaded_model.add(Dense(6, activation='softmax'))

    loaded_model.load_weights("model_weights/vgg19_task5.h5")

    label_A = classify_event(img_A, loaded_model)
    label_B = classify_event(img_B, loaded_model)
    label_C = classify_event(img_C, loaded_model)
    label_D = classify_event(img_D, loaded_model)
    label_E = classify_event(img_E, loaded_model)

    
    cv2.rectangle(img, (y1, x1), (y1 + 80, x1 + 80), (0, 255, 0), 5)
    cv2.rectangle(img, (y2, x2), (y2 + 80, x2 + 80), (0, 255, 0), 5)
    cv2.rectangle(img, (y3, x3), (y3 + 80, x3 + 80), (0, 255, 0), 5)
    cv2.rectangle(img, (y4, x4), (y4 + 80, x4 + 80), (0, 255, 0), 5)
    cv2.rectangle(img, (y5, x5), (y5 + 80, x5 + 80), (0, 255, 0), 5)

    cv2.putText(img, label_A, (y1, x1 - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(img, label_B, (y2 - 30, x2 - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(img, label_C, (y3, x3 - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(img, label_D, (y4, x4 - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(img, label_E, (y5, x5 - 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    img = cv2.resize(img, (450, 450))

    cv2.imshow("Arena Feed", img)
    cv2.waitKey(0)
    cap.release()
    cv2.destroyAllWindows()

    identified_labels = {"A": label_A, "B": label_B, "C": label_C, "D": label_D, "E": label_E}
    print(identified_labels)
##################################################
    return identified_labels

############### Main Function	#################
if __name__ == "__main__":
    identified_labels = return_labels_dict()
    print(identified_labels)