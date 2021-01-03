from Support import load_c2d_images


class Exp:
    def __init__(self, x=None):
        self.x = x or 5
        pass


if __name__ == "__main__":
    # ex1 = Exp(6)
    # print(ex1.x)
    # exp = Exp()
    # print(exp.x)
    #
    # list1 = [5]
    # list2 = list1
    # list2.append(6)
    # print(list1)
    #print(exp.__class__.__name__)
    exp = Exp(5)
    list = []
    list.append(exp)
    list.append(exp)
    print(list)
