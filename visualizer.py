import json
class Visualizer:
    def __init__(self):
        self.file_loc = 'data/tracked_data.json'

    def visualize(self):
        with open(self.file_loc, 'r') as f:
            for line in f:
                print(line)