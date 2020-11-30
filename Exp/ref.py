class Controller:
    def __init__(self):
        self.callback = Callback()


class Current:
    def __init__(self, controller: Controller):
        self.callback = controller.callback


class Callback:
    def __init__(self):
        self.d = {"key": 1}

    def set_d(self, d):
        self.d = d


if __name__ == "__main__":
    controller = Controller()
    current = Current(controller)
    current.callback.set_d({"key": 0})
    bool = controller.callback.d.get("key") == current.callback.d.get("key")
    print(bool)

