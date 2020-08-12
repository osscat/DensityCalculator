class Person:
    def __init__(self, coordinate1, coordinate2):
        self.coordinates = (coordinate1, coordinate2)

    def pixel_delta(self):
        return abs(self.coordinates[0] - self.coordinates[1])
    
