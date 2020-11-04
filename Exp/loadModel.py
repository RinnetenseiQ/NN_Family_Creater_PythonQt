import tensorflow as tf

if __name__ == '__main__':
    # model = load_model("D:\keras\Exports\animals_TensorFlow\saved_model.pb")
    #model = tf.saved_model.load("D:\\keras\\Exports\\animals_TensorFlow\\")
    model = tf.keras.models.load_model("D:\\keras\\Exports\\animals_TensorFlow\\")
    tf.keras.models.save_model(model, "D:\\keras\\Exports\\animals_TensorFlow\\model.h5")
    model = tf.keras.models.load_model("D:\\keras\\Exports\\animals_TensorFlow\\model.h5")
    model.summary()
    layers = model.layers
    print(model)
