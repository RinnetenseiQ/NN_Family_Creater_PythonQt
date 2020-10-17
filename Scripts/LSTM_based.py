import os
import socket
import string
import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding, RepeatVector, Dropout
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from tensorflow.keras import optimizers
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

from Chromosomes.LSTM_chromosome import LSTM_chromosome

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
pd.set_option('display.max_colwidth', 200)


# 0 = all messages are logged, 3 - INFO, WARNING, and ERROR messages are not printed
# os.environ["CUDA_VISIBLE_DEVICES"] = "-1"  # Force CPU

class LSTM_based:
    def __init__(self, chromosome: LSTM_chromosome = None, chr_p=None, sock: socket = None):
        self.chr_p = chr_p
        self.chromosome = chromosome
        self.sock = sock

    def learn(self):
        self.getData()
        self.createModel()
        self.train()
        self.estimateModel()
        self.saveModel()
        self.makePrediction()
        pass

    def makePrediction(self):
        # Load model
        model = load_model('en-de-model.h5')

        phrs_enc = encode_sequences(self.eng_tokenizer, self.eng_length,
                                    ["the weather is nice today", "my name is tom", "how old are you",
                                     "where is the nearest shop"])
        print("phrs_enc:", phrs_enc.shape)

        preds = model.predict_classes(phrs_enc)
        print("Preds:", preds.shape)
        print(preds[0])
        print(get_word(preds[0][0], self.deu_tokenizer), get_word(preds[0][1], self.deu_tokenizer),
              get_word(preds[0][2], self.deu_tokenizer),
              get_word(preds[0][3], self.deu_tokenizer))
        print(preds[1])
        print(get_word(preds[1][0], self.deu_tokenizer), get_word(preds[1][1], self.deu_tokenizer),
              get_word(preds[1][2], self.deu_tokenizer),
              get_word(preds[1][3], self.deu_tokenizer))
        print(preds[2])
        print(get_word(preds[2][0], self.deu_tokenizer), get_word(preds[2][1], self.deu_tokenizer),
              get_word(preds[2][2], self.deu_tokenizer),
              get_word(preds[2][3], self.deu_tokenizer))
        print(preds[3])
        print(get_word(preds[3][0], self.deu_tokenizer), get_word(preds[3][1], self.deu_tokenizer),
              get_word(preds[3][2], self.deu_tokenizer),
              get_word(preds[3][3], self.deu_tokenizer))
        print()
        pass

    def getData(self):
        self.data = read_text("C:/keras/LSTM/deutch.txt")
        self.data = np.array(self.data)
        self.data = self.data[:30000, :]
        print("Dictionary size:", self.data.shape)

        # Remove punctuation
        self.data[:, 0] = [s.translate(str.maketrans('', '', string.punctuation)) for s in self.data[:, 0]]
        self.data[:, 1] = [s.translate(str.maketrans('', '', string.punctuation)) for s in self.data[:, 1]]

        # Convert text to lowercase
        for i in range(len(self.data)):
            self.data[i, 0] = self.data[i, 0].lower()
            self.data[i, 1] = self.data[i, 1].lower()

        # Prepare English tokenizer
        self.eng_tokenizer = Tokenizer()
        self.eng_tokenizer.fit_on_texts(self.data[:, 0])
        self.eng_vocab_size = len(self.eng_tokenizer.word_index) + 1
        self.eng_length = 8

        # Prepare Deutch tokenizer
        self.deu_tokenizer = Tokenizer()
        self.deu_tokenizer.fit_on_texts(self.data[:, 1])
        self.deu_vocab_size = len(self.deu_tokenizer.word_index) + 1
        self.deu_length = 8

        # Split data into train and test set
        train, test = train_test_split(self.data, test_size=0.2, random_state=12)

        # Prepare training data
        self.trainX = encode_sequences(self.eng_tokenizer, self.eng_length, train[:, 0])
        self.trainY = encode_sequences(self.deu_tokenizer, self.deu_length, train[:, 1])

        # Prepare validation data
        self.testX = encode_sequences(self.eng_tokenizer, self.eng_length, test[:, 0])
        self.testY = encode_sequences(self.deu_tokenizer, self.deu_length, test[:, 1])
        pass

    def createModel(self):
        print("deu_vocab_size:", self.deu_vocab_size, self.deu_length)
        print("eng_vocab_size:", self.eng_vocab_size, self.eng_length)
        # Model compilation (with 512 hidden units)
        self.model = make_model(self.eng_vocab_size, self.deu_vocab_size, self.eng_length, self.deu_length, 512)
        pass

    def train(self):
        # Train model
        num_epochs = 50
        self.history = self.model.fit(self.trainX, self.trainY.reshape(self.trainY.shape[0], self.trainY.shape[1], 1),
                                      epochs=num_epochs, batch_size=512,
                                      validation_split=0.2, callbacks=None, verbose=1)
        pass

    def estimateModel(self):
        plt.plot(self.history.history['loss'])
        plt.plot(self.history.history['val_loss'])
        plt.legend(['train', 'validation'])
        plt.show()
        pass

    def saveModel(self):
        self.model.save('en-de-model.h5')
        pass


# Read raw text file
def read_text(filename):
    with open(filename, mode='rt', encoding='utf-8') as file:
        text = file.read()
        sents = text.strip().split('\n')
        return [i.split('\t') for i in sents]


# Encode and pad sequences
def encode_sequences(tokenizer, length, lines):
    # integer encode sequences
    seq = tokenizer.texts_to_sequences(lines)
    # pad sequences with 0 values
    seq = pad_sequences(seq, maxlen=length, padding='post')
    return seq


# Build NMT model
def make_model(in_vocab, out_vocab, in_timesteps, out_timesteps, n):
    model = Sequential()
    model.add(Embedding(in_vocab, n, input_length=in_timesteps, mask_zero=True))
    model.add(LSTM(n))
    model.add(Dropout(0.3))
    model.add(RepeatVector(out_timesteps))
    model.add(LSTM(n, return_sequences=True))
    model.add(Dropout(0.3))
    model.add(Dense(out_vocab, activation='softmax'))
    model.compile(optimizer=optimizers.RMSprop(lr=0.001), loss='sparse_categorical_crossentropy')
    return model


def get_word(n, tokenizer):
    if n == 0:
        return ""
    for word, index in tokenizer.word_index.items():
        if index == n:
            return word
    return ""


if __name__ == '__main__':
    lstm_nn = LSTM_based()
    lstm_nn.learn()
