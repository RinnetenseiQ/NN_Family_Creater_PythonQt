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

        # early_stopping
        # model_checkpoint
        # tensorboard
        # LRScheduler
        # terminateNaN
        # reduceLR_onPlato
        # remote_monitor
        # lambda_callback
        # CSVLogger
        # progbar_logger

        self.early_stopping = early_stopping or {"monitor": "acc",
                                                 "min_delta": 0.01,
                                                 "patience": 5,
                                                 "mode": "auto",  # {min, max, auto}
                                                 "restore_best_weights": True,
                                                 "verbose": 1}
        self.model_checkpoint = model_checkpoint or {"filepath": "/Directory/checkpoints/temp_checkpoint.h5",
                                                     "monitor": "acc",  # {loss,acc,val_loss,val_acc}
                                                     "verbose": 1,
                                                     "save_best_only": True,
                                                     "mode": "auto",  # {min, max, auto}
                                                     "save_weights_only": False,
                                                     "save_freq": "epoch"  # "epoch" or integer
                                                     }
        self.tensorboard = tensorboard or {"log_dir": "logs",  # the path of the directory where to save the log files
                                                               # to be parsed by TensorBoard.
                                           "histogram_freq": 0,  # frequency (in epochs), if 0 - without hist
                                           "write_graph": True,  # whether to visualize the graph in TensorBoard.
                                                                 # The log file can become quite
                                                                 # large when write_graph is set to True.
                                           "write_images": False,  # whether to write model weights
                                                                   # to visualize as image in TensorBoard.
                                           "update_freq": "epoch",  # 'batch' or 'epoch' or integer.
                                                                    # If using an integer, let's say 1000,
                                                                    # the callback will write the metrics and
                                                                    # losses to TensorBoard every 1000 batches
                                           "profile_batch": 2,  # must be a non-negative integer or a tuple of integers.
                                                                # Set profile_batch=0 to disable profiling.
                                           "embeddings_freq": 0,  # frequency (in epochs) at which embedding layers will
                                                                  # be visualized.
                                                                  # If set to 0, embeddings won't be visualized.
                                           "embeddings_metadata": None  # a dictionary which maps layer name
                                                                        # to a file name in which metadata
                                                                        # for this embedding layer is saved.
                                           }

        self.LRScheduler = LRScheduler or {"schedule": None, "verbose": 0} # не уверен, что выйдет реализовать

        self.terminateNaN = terminateNaN or TerminateOnNaN()  # не имеет аргументов

        self.reduceLR_onPlato = reduceLR_onPlato or {"monitor": 'val_loss',
                                                     "factor": 0.1,  # new_lr = lr * factor
                                                     "patience": 10,  # number of epochs with no improvement
                                                                      # after which learning rate will be reduced.
                                                     "verbose": 0,  # int. 0: quiet, 1: update messages.
                                                     "mode": 'auto',  # one of {'auto', 'min', 'max'}
                                                     "min_delta": 0.0001,  # threshold for measuring the new optimum,
                                                                           # to only focus on significant changes.
                                                     "cooldown": 0,  # number of epochs to wait before resuming
                                                                     # normal operation after lr has been reduced.
                                                     "min_lr": 0}  # lower bound on the learning rate.
        self.remote_monitor = remote_monitor or {"root": 'http://localhost:9000',  # String; root url of the target server.
                                                 "path": '/publish/epoch/end/',  # String; path relative to root to which the events will be sent.
                                                 "field": 'data',
                                                 "headers": None,
                                                 "send_as_json": False}

        self.lambda_callback = lambda_callback or {"on_epoch_begin": None,
                                                   "on_epoch_end": None,
                                                   "on_batch_begin": None,
                                                   "on_batch_end": None,
                                                   "on_train_begin": None,
                                                   "on_train_end": None}
        self.CSVLogger = CSVLogger or {"filename": "csv_logs",
                                       "separator": ',',
                                       "append": False}

        self.progbar_logger = progbar_logger or {"count_mode": 'samples',
                                                 "stateful_metrics": None}  # не уверен, что он нужен

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
