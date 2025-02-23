from Lift import Lift
from Request import Request

class MyLift(Lift):
    def __init__(self, total_floors, max_capacity, travel_time=2, exit_time=4):

        # This calls the constructor of the parent class Lift, passing the parameters of Lift to MyLift
        super().__init__(total_floors, max_capacity, travel_time, exit_time)

        '''Initialises 2 dictionaries - for requests going up, and for requests going down. Inside each dictionary, 
        the current floor is the key, and destination floors are the value, stored in a list.'''
        self.up_requests = {floor: [] for floor in range(1, total_floors + 1)} 
        self.down_requests = {floor: [] for floor in range(1, total_floors + 1)}  

    def add_request(self, request):
        """Adds a Request object to the corresponding floor's queue, sorted by destination."""
        direction = request.request_direction()
        if direction == "UP":
            # Add to the up_requests and sort the list by destination floor
            self.up_requests[request.start_floor].append(request)
            self.up_requests[request.start_floor].sort(key=lambda r: r.destination_floor)
        elif direction == "DOWN":
            # Add to the down_requests and sort the list by destination floor (descending order)
            self.down_requests[request.start_floor].append(request)
            self.down_requests[request.start_floor].sort(key=lambda r: r.destination_floor, reverse=True)