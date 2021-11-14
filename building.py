
import copy
import json

class Building:
    def __init__(self,fname):
        with open(fname,"r") as f:
            dict = json.load(f)
        self.minFloor = dict.get('_minFloor')
        self.maxFloor = dict.get('_maxFloor')
        self.Elevators = dict.get('_elevators')






