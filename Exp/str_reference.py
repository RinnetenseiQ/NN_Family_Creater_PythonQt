class cls:
    def __init__(self, name: list):
        self.name = name
        #name = list("pnh")
        name.clear()
        name += ["beer"]

    def method(self):
        self.name = list("pnh")


if __name__ == "__main__":
    name = list("1")
    name[0] = "pnh"
    foo = cls(name)
    print(name[-1])
    #foo.method()
    #print(str(name))
