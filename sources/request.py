#This object represents the request of the passenger, the floor they start at and the floor they're going to
class Request:
    def __init__(self, start_floor, destination_floor):
        self.start_floor = start_floor
        self.destination_floor = destination_floor