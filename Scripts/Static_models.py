import os

# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

import tensorflow as tf
from sklearn.metrics import classification_report
from tensorflow.keras.applications import ResNet50V2
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Flatten, Dense, Dropout
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np
import matplotlib.pyplot as plt
from multiprocessing import Process
import Support


class App_Models(Process):
    def __init__(self, datasetPath: str, mode: int):
        super().__init__()
        self.datasetPath = datasetPath
        self.mode = mode

    def run(self):
        if self.mode == 0:
            train_ResNet50V2(self.datasetPath)
        elif self.mode == 1:
            train_VGG19(self.datasetPath)
        self.join()


def train_ResNet50V2(path, include_top=True, weights="imagenet", input_tensor=None, input_shape=(224, 224, 3),
                     pooling="avg", classes=1000, classifier_activation=None):
    lb, trainX, testX, trainY, testY = Support.load_c2d_images(path)
    # resnet = ResNet50V2(include_top, weights, input_tensor, pooling=pooling, input_shape=(224, 224, 3), classes=5)
    # resnet = ResNet50V2(
    #     include_top=include_top,
    #     weights=weights,
    #     input_tensor=input_tensor,
    #     input_shape=input_shape,
    #     pooling=pooling,
    #     classes=classes,
    #     classifier_activation=classifier_activation
    # )
    resnet = ResNet50V2(
        include_top,
        weights,
        input_tensor,
        input_shape,
        pooling,
        classes,
    )
    resnet.summary()
    base_model = tf.keras.Model([resnet.input], resnet.get_layer("avg_pool").output)
    # output = resnet.layers[-1].output
    base_model.trainable = False
    output = Dense(len(lb.classes_), activation='softmax')

    # output = Flatten()(output)
    #base_model = Model(resnet.input, output)

    model = Sequential()
    model.add(base_model)
    model.add(output)
    # model.add(Dense(512, activation='relu', input_dim=(128, 128, 3)))
    # model.add(Dropout(0.3))
    # model.add(Dense(2048, activation='relu', input_shape=()))
    # model.add(Dropout(0.3))
    # model.add(Dense(5, activation='softmax'))
    # model.compile(loss='categorical_crossentropy',
    #               optimizer=RMSprop(lr=0.01),
    #               #optimizer=RMSprop(lr=2e-5),
    #               metrics=['acc'])
    model.compile(loss='categorical_crossentropy',
                       optimizer=RMSprop(lr=0.01),
                       # optimizer=RMSprop(lr=2e-5),
                       metrics=['acc'])
    model.summary()
    aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
                             height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
                             horizontal_flip=True, fill_mode="nearest")
    H = model.fit_generator(aug.flow(trainX, trainY, batch_size=16),
                                 validation_data=(testX, testY), steps_per_epoch=len(trainX) // 16,
                                 epochs=100, callbacks=None)

    # history = model.fit_generator(train_generator,
    #                               steps_per_epoch=100,
    #                               epochs=100,
    #                               validation_data=val_generator,
    #                               validation_steps=50,
    #                               verbose=1)
    predictions = model.predict(testX, batch_size=16)
    print(classification_report(testY.argmax(axis=1),
                                predictions.argmax(axis=1), target_names=lb.classes_, output_dict=False))

    N = np.arange(0, 100)
    plt.style.use("ggplot")
    plt.figure()
    plt.plot(N, H.history["loss"], label="train_loss")
    plt.plot(N, H.history["val_loss"], label="val_loss")
    plt.plot(N, H.history["acc"], label="train_acc")
    plt.plot(N, H.history["val_acc"], label="val_acc")
    plt.title("Training Loss and Accuracy (CNN)")
    plt.xlabel("Epoch #")
    plt.ylabel("Loss/Accuracy")
    plt.legend()
    plt.savefig("\\resnet.png")
    plt.close('all')


def train_VGG19(path, include_top=True, weights='imagenet', input_tensor=None, input_shape=None,
                pooling=None, classes=1000, classifier_activation='softmax'):
    lb, trainX, testX, trainY, testY = Support.load_c2d_images(path)
    vgg19 = tf.keras.applications.VGG19(
        include_top, weights=None, input_tensor=None, input_shape=None,
        pooling=None, classes=1000, classifier_activation='softmax'
    )


if __name__ == '__main__':
    train_ResNet50V2("D:\\keras\\datasets\\animals")
