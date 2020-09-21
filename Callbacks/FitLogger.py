from tensorflow.keras.callbacks import Callback
#from project_main import MainWindow


class FitLogger(Callback):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window

    def on_train_begin(self, logs=None):
        #keys = list(logs.keys())
        #print("Starting training; got log keys: {}".format(keys))
        self.main_window.geneticOutput_TE.append("train beginning \n")

    def on_train_end(self, logs=None):
        pass

    def on_epoch_begin(self, epoch, logs=None):
        pass

    def on_epoch_end(self, epoch, logs=None):
        pass

    def on_test_begin(self, logs=None):
        pass

    def on_test_end(self, logs=None):
        pass

    def on_predict_begin(self, logs=None):
        pass

    def on_predict_end(self, logs=None):
        pass

    def on_train_batch_begin(self, batch, logs=None):
        pass

    def on_train_batch_end(self, batch, logs=None):
        if batch == 0:
            self.main_window.geneticOutput_TE.append("For batch {}, loss is {:7.2f}.".format(batch, logs["loss"]))
        else:
            text = self.main_window.geneticOutput_TE.toPlainText().split("\n")
            text.pop()
            text.append("For batch {}, loss is {:7.2f}.".format(batch, logs["loss"]))
            #self.main_window.geneticOutput_TE.clear()
            #for i in text:
                #self.main_window.geneticOutput_TE.append(i + "\n")


    def on_test_batch_begin(self, batch, logs=None):
        pass

    def on_test_batch_end(self, batch, logs=None):
        pass

    def on_predict_batch_begin(self, batch, logs=None):
        pass

    def on_predict_batch_end(self, batch, logs=None):
        pass
