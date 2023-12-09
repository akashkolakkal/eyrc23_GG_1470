'''
# Team ID:          1470
# Theme:            Geo Guide
# Author List:      Parth Jain, Akash Kolakkal, Anikesh Kulal, Keshav Jha
# Filename:         task_2b_model_training.py
# Functions:        < Comma separated list of functions in this file >
# Global variables: img_height, img_width, batch_size, train_ds, val_ds, class_names, pretrained_model, EffNet_model, history
'''

# We had actually used a colab notebook for training the model.
# The code is given below is a replica of the same.
# link: https://colab.research.google.com/drive/1C5Z0ujAqbse-6gZHj8pONB3jZO74AYCO?usp=sharing
#
# To run, place the training_dataset folder in the same directory as this file and run the file.


from tensorflow import keras
from keras.layers import Dense, Flatten
from keras.models import Sequential


img_height, img_width = 50, 50
batch_size = 32
train_ds = keras.preprocessing.image_dataset_from_directory(
    'training_dataset',
    seed=123,
    validation_split=0.1,
    subset="training",
    image_size=(img_height, img_width),
    batch_size=batch_size)

val_ds = keras.preprocessing.image_dataset_from_directory(
    'training_dataset',
    validation_split=0.1,
    subset="validation",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size)


class_names = train_ds.class_names
print(class_names)


pretrained_model = keras.applications.EfficientNetV2B3(
    include_top=False,
    weights="imagenet",
    input_shape=(50, 50, 3),
    pooling='avg',
    classes=5,
    classifier_activation="softmax"
)

EffNet_model = Sequential()


for layer in pretrained_model.layers:
    layer.trainable = False

EffNet_model.add(pretrained_model)
EffNet_model.add(Flatten())
EffNet_model.add(Dense(512, activation='relu'))
EffNet_model.add(Dense(5, activation='softmax'))

EffNet_model = Sequential()


for layer in pretrained_model.layers:
    layer.trainable = False

EffNet_model.add(pretrained_model)
EffNet_model.add(Flatten())
EffNet_model.add(Dense(512, activation='relu'))
EffNet_model.add(Dense(5, activation='softmax'))


EffNet_model.compile(
    optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])


epochs = 5
history = EffNet_model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=epochs
)

EffNet_model.save_weights("model.h5")
