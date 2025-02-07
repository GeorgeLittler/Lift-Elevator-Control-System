#This object represents the request of the passenger, the floor they start at and the floor they're going to
class Request:
    def __init__(self, start_floor, destination_floor):
        self.start_floor = start_floor
        self.destination_floor = destination_floor
    def request_direction(self):
        if self.start_floor>self.destination_floor:
            direction1="negative"
            return direction1
        if self.start_floor<self.destination_floor:
            direction1="positive"
            return direction1