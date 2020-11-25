from Support import load_c2d_images


class Exp:
    def __init__(self, x=None):
        self.x = x or 5
        pass


if __name__ == "__main__":
    ex1 = Exp(6)
    print(ex1.x)
    exp = Exp()
    print(exp.x)
    #print(exp.__class__.__name__)
