from Lift1 import Lift1
from Request import Request

class MyLift(Lift1):
    def __init__(self, total_floors, max_capacity, travel_time=2, enter_exit_time=4):

        # This calls the constructor of the parent class Lift, passing the parameters of Lift to MyLift
        super().__init__(total_floors, max_capacity, travel_time, enter_exit_time)

        '''Initialises 2 dictionaries - for requests going up, and for requests going down. Inside each dictionary, 
        the current floor is the key, and destination floors are the value, stored in a list.'''
        self.up_requests = {floor: [] for floor in range(1, total_floors + 1)} 
        self.down_requests = {floor: [] for floor in range(1, total_floors + 1)} 

        self.active_requests = []

    def add_request(self, request):
        """Adds a Request object to the corresponding floor's queue, sorted by destination."""
        direction = request.request_direction()
        print(f"Adding request from floor {request.start_floor} to {request.destination_floor}, direction: {direction}")
        
        if direction == "positive":
            self.up_requests[request.start_floor].append(request)
        elif direction == "negative":
            self.down_requests[request.start_floor].append(request)
        

    def sort_requests(self):
        """Sorts the requests in both up_requests and down_requests."""
        # Sort up_requests in ascending order of destination
        for floor in self.up_requests:
            self.up_requests[floor].sort(key=lambda r: r.destination_floor)
        
        # Sort down_requests in descending order of destination
        for floor in self.down_requests:
            self.down_requests[floor].sort(key=lambda r: r.destination_floor, reverse=True)

    def display_requests(self):
        print("Up requests:", self.up_requests)
        print("Down requests:", self.down_requests)

    
    def check_if_up_requests(self):
        for floor in self.up_requests:
            if self.up_requests[floor]:  
                return True
        return False
    
    def check_if_down_requests(self):
        for floor in self.down_requests:
            if self.down_requests[floor]:
                return True
        return False
    
    def check_if_up_requests_at_current_floor(self):
        if self.up_requests[self.current_floor]:
            return True
        return False
    
    def check_if_down_requests_at_current_floor(self):
        if self.down_requests[self.current_floor]:
            return True
        return False
    
    def check_if_up_requests_above_floor(self):
        for floor in self.up_requests:  
            if self.up_requests[floor] and self.up_requests[floor][0].start_floor > self.current_floor:
                return True
        return False
    
    def check_if_down_requests_below_floor(self):
        for floor in self.down_requests:
            if self.down_requests[floor] and self.down_requests[floor][0].start_floor < self.current_floor:
                return True
        return False
    
    def check_if_active_requests(self):
        if len(self.active_requests) != 0:
            return True
        return False

    def is_current_floor_at_or_below_lowest_up_request(self):
        for floor in sorted(self.up_requests.keys()):  
            if self.up_requests[floor]:  
                return self.current_floor <= floor
        return None  

    def is_current_floor_at_or_below_highest_down_request(self):
        for floor in sorted(self.down_requests.keys(), reverse=True):  
            if self.down_requests[floor]:  
                return self.current_floor >= floor
        return None

    def pick_up_up_passengers(self):
        enter_time_incremented = False
        picked_up_passengers  = False

        while self.up_requests[self.current_floor] and self.current_capacity < self.max_capacity:
            passenger = self.up_requests[self.current_floor].pop(0)
            self.active_requests.append(passenger)
            self.current_capacity += 1
            self.available_capacity = self.max_capacity - self.current_capacity
            picked_up_passengers  = True
            
            if not enter_time_incremented:
                self.time_elapsed += self.enter_exit_time
                enter_time_incremented = True
            
            print(f"Picked up passenger at floor {self.current_floor} going to {passenger.destination_floor}")

        return picked_up_passengers 
    
    def pick_up_down_passengers(self):
        enter_time_incremented = False
        picked_up_passengers  = False

        while self.down_requests[self.current_floor] and self.current_capacity < self.max_capacity:
            passenger = self.down_requests[self.current_floor].pop(0)
            self.active_requests.append(passenger)
            self.current_capacity += 1  
            self.available_capacity = self.max_capacity - self.current_capacity
            picked_up_passengers  = True

            if not enter_time_incremented:
                self.time_elapsed += 4
                enter_time_incremented = True

            print(f"Picked up passenger at floor {self.current_floor} going to {passenger.destination_floor}")

        return picked_up_passengers 

    def pick_up_passengers(self):
        picked_up_passengers = False

        if self.up_requests[self.current_floor] and self.direction == "positive":
            picked_up_passengers = self.pick_up_up_passengers()
        elif self.down_requests[self.current_floor] and self.direction == "negative":
            picked_up_passengers = self.pick_up_down_passengers()

        print(f"Active requests: {self.active_requests}")
        return picked_up_passengers

    def move_lift_up(self):
        self.current_floor += 1
        self.time_elapsed += self.travel_time
        print(f"Lift moving up to floor {self.current_floor}")

    def move_lift_down(self):
        self.current_floor -= 1
        self.time_elapsed += self.travel_time
        print(f"Lift moving down to floor {self.current_floor}")

    def move_lift(self):
        if self.direction == "positive":
            self.move_lift_up()
        else:
            self.move_lift_down()

    def drop_off_passengers(self, picked_up_passengers):
        exit_time_incremented = False
        drop_off_passengers = False

        for passenger in self.active_requests[:]:  
            if passenger.destination_floor == self.current_floor:
                self.active_requests.remove(passenger)  
                self.current_capacity -= 1 
                self.available_capacity = self.max_capacity - self.current_capacity
                drop_off_passengers = True
                print(f"Dropped off passenger at floor {self.current_floor}")

                if not exit_time_incremented:
                    self.time_elapsed += self.enter_exit_time
                    exit_time_incremented = True

        if  picked_up_passengers and drop_off_passengers:
            self.time_elapsed -= self.enter_exit_time

    def change_lift_direction(self):
        if self.direction == "positive":
            self.direction = "negative"
        else:
            self.direction = "positive"

    
    def run(self):
        while self.check_if_up_requests() or self.check_if_down_requests() or self.check_if_active_requests():
            print(f"UP: {self.up_requests}")
            print(f"DOWN: {self.down_requests}")
            picked_up_passengers = self.pick_up_passengers()
            self.move_lift()
            self.drop_off_passengers(picked_up_passengers)

            if not self.check_if_active_requests():
                if self.direction == "positive":
                    if self.check_if_up_requests(): 
                        if not self.check_if_up_requests_at_current_floor() and not self.check_if_up_requests_above_floor():
                            self.change_lift_direction()
                    else:
                        if self.is_current_floor_at_or_below_highest_down_request():
                            self.change_lift_direction()

                elif self.direction == "negative":
                    if self.check_if_down_requests():
                        if not self.check_if_down_requests_at_current_floor() and not self.check_if_down_requests_below_floor():
                            self.change_lift_direction()
                    else:
                        if self.is_current_floor_at_or_below_lowest_up_request():
                            self.change_lift_direction()

        return self.time_elapsed




mylift = MyLift(total_floors=8, max_capacity=5)

# Adding requests to the MyLift object
requests_data = {
    1: [4, 6, 3, 2],      # Up to 3, 5
    2: [3, 5, 7],         # Down to 1
    3: [8],   # Down to 1, 2, Up to 4
    4: [2, 5],         # Down to 1
    5: [6, 4],         # Up to 6
    6: [8],         # Down to 3
    7: [4, 2],
    8: [3]
}

requests = []
for start_floor, destination_floors in requests_data.items():
    for destination_floor in destination_floors:
        requests.append(Request(start_floor, destination_floor))

# Adding requests to the MyLift object
for request in requests:
    mylift.add_request(request)

mylift.sort_requests()

mylift.display_requests()

# Run the simulation and get the total time elapsed
total_time = mylift.run()
print(f"Total time elapsed: {total_time} seconds")