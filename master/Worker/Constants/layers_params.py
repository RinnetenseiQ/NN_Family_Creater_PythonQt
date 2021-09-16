


input_params = {
    "shape": (1,),
    "batch_size": None,
    "name": None,
    "dtype": None,
    "sparse": False,
    "tensor": None,
    "ragged": False
}

conv2d_params = {
    "filters": 2,
    "kernel_size": (3, 3),
    "strides": (1, 1),
    "padding": 'valid',
    "data_format": None,
    "dilation_rate": (1, 1),
    "activation": None,
    "use_bias": True,
    "kernel_initializer": 'glorot_uniform',
    "bias_initializer": 'zeros',
    "kernel_regularizer": None,
    "bias_regularizer": None,
    "activity_regularizer": None,
    "kernel_constraint": None,
    "bias_constraint": None
}



dense_params = {
    "units": 1,
    "activation": None,
    "use_bias": True,
    "kernel_initializer": 'glorot_uniform',
    "bias_initializer": 'zeros',
    "kernel_regularizer": None,
    "bias_regularizer": None,
    "activity_regularizer": None,
    "kernel_constraint": None,
    "bias_constraint": None
}

dropout_params = {
    "rate": 0,
    "noise_shape": None,
    "seed": None
}

flatten_params = {
    "data_format": None
}

maxpool2d_params = {
    "pool_size": (2, 2),
    "strides": None,
    "padding": 'valid',
    "data_format": None
}
