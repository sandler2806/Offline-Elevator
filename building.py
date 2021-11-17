import json


class Building:
    def __init__(self, file_name):
        if file_name != "":
            with open(file_name, "r") as f:
                dict2 = json.load(f)
            self.minFloor = dict2.get('_minFloor')
            self.maxFloor = dict2.get('_maxFloor')
            self.Elevators = dict2.get('_elevators')
