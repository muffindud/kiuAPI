import json
from os.path import isfile


class DataManager:
    instance = None
    file_path = 'data/queues.json'


    def __init__(self):
        if not isfile(self.file_path):
            with open(self.file_path, 'w') as file:
                file.write('{}')

        with open(self.file_path, 'r') as file:
            self.data = json.load(file)


    def get_data(self, keys=[]) -> dict:
        if keys:
            return {k: self.data[k] for k in keys if k in self.data}

        return self.data


    def add_data(self, data: dict, update: bool = False) -> None:
        if any(k in self.data for k in data.keys()) and not update:
            return -1
    
        if any(k not in self.data for k in data.keys()) and update:
            return -1

        for key, value in data.items():
            self.data[key] = value

        with open(self.file_path, 'w') as file:
            json.dump(self.data, file, indent=4)


    def remove_data(self, key: list) -> None:
        if any(k not in self.data for k in key):
            return -1

        for k in key:
            self.data.pop(k)

        with open(self.file_path, 'w') as file:
            json.dump(self.data, file, indent=4)
