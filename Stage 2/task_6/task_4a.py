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
# Theme:			Geo Guide (GG)
# Functions:		classify_event, process_test_images, classify_and_label_events
# Global Variables:	None


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


def classify_event(image, loaded_model) -> str:
    '''
    * Function Name:    classify_event
    * Input:            image -> The image to be classified
    *                   loaded_model -> The trained model
    * Output:           event -> String of thhe event detected
    * Logic:            This function is used to classify the event in the given image
    * Example Call:     classify_event(image, loaded_model)
    '''

    image = np.expand_dims(image, axis=0)
    pred = loaded_model.predict(image, verbose=0)

    event = np.argmax(pred)
    return event

def process_test_images(image):
    '''
    * Function Name:    process_test_images
    * Input:            image -> The image to be processed
    * Output:           image -> The processed image
    * Logic:            This function is used to process the given image
    * Example Call:     process_test_images(image)
    '''

    # thresholding the image
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.1, 0, 255)
    image = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # denoising the image
    image = cv2.fastNlMeansDenoisingColored(
        image, h=5, templateWindowSize=2, searchWindowSize=25)

    image = cv2.resize(image, (80, 80))

    return image

##############################################################


# def task_4a_return():
def classify_and_label_events():
    """
    * Function Name:    classify_and_label_events
    * Input:            None
    * Output:           identified_labels -> Dictionary containing the labels of the events detected
    * Logic:            This function is used to classify and label the events detected from the camera's feed
    * Example Call:     classify_and_label_events()
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

    # Opening the camera feed
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    cap.set(3, 1920)
    cap.set(4, 1080)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

    # Skipping the initial frames to let the camera adjust to the lighting conditions
    for _ in range(30):
        ret, frame = cap.read()

    # Getting the arena feed
    ret, frame = cap.read()

    if not ret:
        pass
    
    # extracting the arena from the frame, and transforming it to the required size
    img = get_arena(frame)

    # hardcoding the coordinates of the events
    y1, x1 = 242, 936
    y2, x2 = 715, 734
    y3, x3 = 723, 528
    y4, x4 = 229, 526
    y5, x5 = 249, 192

    # extracting the images of the events and processing them
    img_A = process_test_images(img[x1: x1 + 70, y1: y1 + 70])
    img_B = process_test_images(img[x2: x2 + 70, y2: y2 + 70])
    img_C = process_test_images(img[x3: x3 + 70, y3: y3 + 70])
    img_D = process_test_images(img[x4: x4 + 70, y4: y4 + 70])
    img_E = process_test_images(img[x5: x5 + 70, y5: y5 + 70])

    # loading the trained model
    loaded_model = Sequential()
    pretrained_model = tf.keras.applications.EfficientNetB7(
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

    loaded_model.load_weights("model_weights/effnet_task6(2).h5")

    image_labels = ['combat', 'destroyed_buildings', 'fire', 'humanitarian_aid', 'military_vehicles', 'None']
    console_labels = ['Combat', 'Destroyed buildings', 'Fire', 'Humanitarian Aid and rehabilitation', 'Military Vehicles', 'None']
    
    # classifying the events
    index_A = classify_event(img_A, loaded_model)
    index_B = classify_event(img_B, loaded_model)
    index_C = classify_event(img_C, loaded_model)
    index_D = classify_event(img_D, loaded_model)
    index_E = classify_event(img_E, loaded_model)

    # creating bounding boxes
    cv2.rectangle(img, (y1 - 5, x1 - 5), (y1 + 80, x1 + 80), (0, 255, 0), 5)
    cv2.rectangle(img, (y2 - 5, x2 - 5), (y2 + 80, x2 + 80), (0, 255, 0), 5)
    cv2.rectangle(img, (y3 - 5, x3 - 5), (y3 + 80, x3 + 80), (0, 255, 0), 5)
    cv2.rectangle(img, (y4 - 5, x4 - 5), (y4 + 80, x4 + 80), (0, 255, 0), 5)
    cv2.rectangle(img, (y5 - 5, x5 - 5), (y5 + 80, x5 + 80), (0, 255, 0), 5)

    # labeling the events on the image if they are not None
    if image_labels[index_A] != "None":
        cv2.putText(img, image_labels[index_A], (y1, x1 - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    if image_labels[index_B] != "None":
        cv2.putText(img, image_labels[index_B], (y2 - 50, x2-20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    if image_labels[index_C] != "None":
        cv2.putText(img, image_labels[index_C], (y3 - 50, x3 - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    if image_labels[index_D] != "None":
        cv2.putText(img, image_labels[index_D], (y4, x4 - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    if image_labels[index_E] != "None":
        cv2.putText(img, image_labels[index_E], (y5, x5 - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    img = cv2.resize(img, (950, 950))

    # printing the identified labels to the console
    identified_labels = {"A": console_labels[index_A], "B": console_labels[index_B],
                         "C": console_labels[index_C], "D": console_labels[index_D], "E": console_labels[index_E]}
    print(identified_labels)

    cv2.imshow("Arena Feed", img)
    cv2.waitKey(0)
    cap.release()
    cv2.destroyAllWindows()

    return identified_labels

############### Main Function	#################
if __name__ == "__main__":
    identified_labels = classify_and_label_events()
