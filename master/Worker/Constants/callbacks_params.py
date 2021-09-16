early_stopping_params = {"monitor": "acc",
                         "min_delta": 0.01,
                         "patience": 5,
                         "mode": "auto",  # {min, max, auto}
                         "restore_best_weights": True,
                         "verbose": 1}