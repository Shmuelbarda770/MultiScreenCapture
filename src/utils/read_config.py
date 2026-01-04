import json


class Config:
    def __init__(self):
        self.data = {}

    def load(self, data):
        self.data = self.wrap(data)

    def wrap(self, json_data):
        if isinstance(json_data, dict):
            return type("ConfigObject", (), {k: self.wrap(v) for k, v in json_data.items()})()
        elif isinstance(json_data, list):
            return [self.wrap(i) for i in json_data]
        else:
            return json_data


with open("/Users/shmuelbarda/Desktop/MultiScreenCapture/config.json", encoding="utf-8") as json_file:
    data = json.load(json_file)

config = Config()
config.load(data)