from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint


class CallbacksHandler:
    def __init__(self,
                 early_stopping=None,
                 model_checkpoint=None):

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
        self.active = {"early_stopping": True, "model_checkpoint": True}

    def getCallbacks(self):
        callbacks = []
        if self.active.get("early_stopping"): callbacks.append(EarlyStopping(**self.early_stopping))
        if self.active.get("model_checkpoint"): callbacks.append(ModelCheckpoint(**self.model_checkpoint))

        return callbacks
