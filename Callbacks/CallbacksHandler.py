from tensorflow.keras.callbacks import (EarlyStopping, ModelCheckpoint,
                                        TensorBoard, LearningRateScheduler,
                                        TerminateOnNaN, ReduceLROnPlateau,
                                        RemoteMonitor, LambdaCallback,
                                        CSVLogger, ProgbarLogger)


class CallbacksHandler:
    def __init__(self,
                 early_stopping=None,
                 model_checkpoint=None,
                 tensorboard=None,
                 LRScheduler=None,
                 terminateNaN=None,
                 reduceLR_onPlato=None,
                 remote_monitor=None,
                 lambda_callback=None,
                 CSVLogger=None,
                 progbar_logger=None
    ):

        # передать active

        self.early_stopping = early_stopping or {"monitor": "val_acc",
                                                 "min_delta": 0.01,
                                                 "patience": 5,
                                                 "mode": "auto",  # {min, max, auto}
                                                 "restore_best_weights": True,
                                                 "verbose": 1}
        self.model_checkpoint = model_checkpoint or {"filepath": "/Directory/checkpoints/temp_checkpoint.h5",
                                                     "monitor": "val_acc",  # {loss,acc,val_loss,val_acc}
                                                     "verbose": 1,
                                                     "save_best_only": True,
                                                     "mode": "auto",  # {min, max, auto}
                                                     "save_weights_only": False,
                                                     "save_freq": "epoch"  # "epoch" or integer
                                                     }
        self.tensorboard = tensorboard or {}
        self.LRScheduler = LRScheduler or {}
        self.terminateNaN = terminateNaN or {}
        self.reduceLR_onPlato = reduceLR_onPlato or {}
        self.remote_monitor = remote_monitor or {}
        self.lambda_callback = lambda_callback or {}
        self.CSVLogger = CSVLogger or {}
        self.progbar_logger = progbar_logger or {}

        self.active = {"early_stopping": True,
                       "model_checkpoint": True,
                       "tensorboard": False,
                       "LRScheduler": False,
                       "terminateNaN": False,
                       "reduceLR_onPlato": False,
                       "remote_monitor": False,
                       "lambda_callback": False,
                       "CSVLogger": False,
                       "progbar_logger": False}

    def getCallbacks(self):
        callbacks = []
        if self.active.get("early_stopping"): callbacks.append(EarlyStopping(**self.early_stopping))
        if self.active.get("model_checkpoint"): callbacks.append(ModelCheckpoint(**self.model_checkpoint))
        if self.active.get("tensorboard"): callbacks.append(TensorBoard(**self.tensorboard))
        if self.active.get("LRScheduler"): callbacks.append(LearningRateScheduler(**self.LRScheduler))
        if self.active.get("terminateNaN"): callbacks.append(TerminateOnNaN(**self.terminateNaN))
        if self.active.get("reduceLR_onPlato"): callbacks.append(ReduceLROnPlateau(**self.reduceLR_onPlato))
        if self.active.get("remote_monitor"): callbacks.append(RemoteMonitor(**self.remote_monitor))
        if self.active.get("lambda_callback"): callbacks.append(LambdaCallback(**self.lambda_callback))
        if self.active.get("CSVLogger"): callbacks.append(CSVLogger(**self.CSVLogger))
        if self.active.get("progbar_logger"): callbacks.append(ProgbarLogger(**self.progbar_logger))

        return callbacks


if __name__ == "__main__":
    handler1 = CallbacksHandler()
    handler2 = CallbacksHandler(early_stopping={})
    print("exp")
