import matplotlib

#matplotlib.use("Agg")
matplotlib.use('TkAgg')
# подключаем необходимые пакеты
import matplotlib.pyplot as plt
# подключаем необходимые пакеты
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, InputLayer
from tensorflow.keras.layers import Conv2D, MaxPooling2D, ZeroPadding2D
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import backend
from imutils import paths
import numpy as np
import random
import cv2
import os


class Net:
    def __init__(self):
        # инициализируем данные и метки
        print("[INFO] loading images...")
        data = []
        labels = []
        # backend.set_floatx('float16')
        print(backend.floatx())
        # берём пути к изображениям и рандомно перемешиваем
        imagePaths = sorted(list(paths.list_images("D:/keras/datasets/animals")))
        random.seed(42)
        random.shuffle(imagePaths)

        # цикл по изображениям
        i = 0
        for imagePath in imagePaths:
            image = cv2.imread(imagePath)
            image = cv2.resize(image, (128, 128)).flatten()
            data.append(image)

            # извлекаем метку класса из пути к изображению и обновляем
            # список меток
            label = imagePath.split(os.path.sep)[-2]
            labels.append(label)
        # os.system('cls')

        # масштабируем интенсивности пикселей в диапазон [0, 1]
        data = np.array(data, dtype="float") / 255.0
        labels = np.array(labels)

        # разбиваем данные на обучающую и тестовую выборки, используя 80%
        # данных для обучения и оставшиеся 20% для тестирования
        (trainX, testX, trainY, testY) = train_test_split(data,
                                                          labels, test_size=0.2, random_state=42)

        # конвертируем метки из целых чисел в векторы (для 2х классов при
        # бинарной классификации вам следует использовать функцию Keras
        # “to_categorical” вместо “LabelBinarizer” из scikit-learn, которая
        # не возвращает вектор)
        lb = LabelBinarizer()
        trainY = lb.fit_transform(trainY)
        testY = lb.transform(testY)

        # reshape arrays
        trainX = trainX.reshape(trainX.shape[0], 128, 128, 3)
        testX = testX.reshape(testX.shape[0], 128, 128, 3)

        model = Sequential()

        #model.add(ZeroPadding2D((1, 1), input_shape=(128, 128, 3)))
        model.add(InputLayer(input_shape=(128, 128, 3)))
        model.add(Conv2D(64, kernel_size=(3, 3), strides=(1, 1), padding="same",  activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        # model.add(ZeroPadding2D((1, 1)))
        model.add(Conv2D(128, (3, 3), strides=(1, 1), padding="same", activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        # model.add(ZeroPadding2D((1, 1)))
        model.add(Conv2D(256, (3, 3), strides=(1, 1), padding="same", activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        # model.add(ZeroPadding2D((1, 1)))
        model.add(Conv2D(512, (3, 3), strides=(1, 1), padding="same", activation='relu'))
        model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))
        model.add(Flatten())
        model.add(Dense(1024, activation='relu'))
        model.add(Dropout(0.25))
        model.add(Dense(1024, activation='relu'))
        model.add(Dropout(0.25))
        model.add(Dense(len(lb.classes_), activation="softmax"))

        INIT_LR = 0.01
        EPOCHS = 5
        BS = 16

        # компилируем модель, используя SGD как оптимизатор и категориальную
        # кросс-энтропию в качестве функции потерь (для бинарной классификации
        # следует использовать binary_crossentropy)
        print("[INFO] training network...")
        opt = SGD(lr=INIT_LR)
        model.compile(loss="categorical_crossentropy", optimizer=opt,
                      metrics=["acc"])

        # обучаем нейросеть
        # H = model.fit(trainX, trainY, validation_data=(testX, testY),
        #	epochs=EPOCHS, batch_size=32)

        aug = ImageDataGenerator(rotation_range=30, width_shift_range=0.1,
                                 height_shift_range=0.1, shear_range=0.2, zoom_range=0.2,
                                 horizontal_flip=True, fill_mode="nearest")

        H = model.fit_generator(aug.flow(trainX, trainY, batch_size=BS),
                                validation_data=(testX, testY), steps_per_epoch=len(trainX) // BS,
                                epochs=EPOCHS)

        # оцениваем нейросеть
        print("[INFO] evaluating network...")
        predictions = model.predict(testX, batch_size=BS)
        print(classification_report(testY.argmax(axis=1),
                                    predictions.argmax(axis=1), target_names=lb.classes_))

        model.summary()

        # строим графики потерь и точности
        N = np.arange(0, EPOCHS)
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
        plt.show()
        # plt.savefig(args["plot"])

        # сохраняем модель и бинаризатор меток на диск
        print("[INFO] serializing network and label binarizer...")
        # model.save(args["model"])
        # f = open(args["label_bin"], "wb")
        # f.write(pickle.dumps(lb))
        # f.close()


if __name__ == "__main__":
    net = Net()
