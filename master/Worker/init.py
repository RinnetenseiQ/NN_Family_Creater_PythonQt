import json


def create_file():
    with open("./config.json", "w") as f:
        d = {"address": "localhost", "port": 9088}
        json.dump(d, f)


if __name__ == "__main__":
    create_file()
