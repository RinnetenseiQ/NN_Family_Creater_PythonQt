from Support import load_c2d_images


class Exp:
    def __init__(self):
        pass


if __name__ == "__main__":
    lb, trainX, testX, trainY, testY = load_c2d_images("D:\\keras\\datasets\\animals")
    exp = Exp()
    print(exp.__class__.__name__)
