from Lift1 import Lift1

class MyLift(Lift1):
    def __init__(self, total_floors, max_capacity, travel_time=2, enter_exit_time=4):

        # This calls the constructor of the parent class Lift, passing the parameters of Lift to MyLift
        super().__init__(total_floors, max_capacity, travel_time, enter_exit_time)

        '''Initialises 2 dictionaries - for requests going up, and for requests going down. Inside each dictionary, 
        the current floor is the key, and destination floors are the value, stored in a list.'''
        self.up_requests = {floor: [] for floor in range(1, total_floors + 1)} 
        self.down_requests = {floor: [] for floor in range(1, total_floors + 1)} 

        # This will store the requests of the passengers inside of the lift
        self.active_requests = []

    # This function adds the requests to up_requests or down_requests based on direction
    def add_request(self, request):
        direction = request.request_direction()
        print(f"Adding request from floor {request.start_floor} to {request.destination_floor}, direction: {direction}")
        
        if direction == "positive":
            self.up_requests[request.start_floor].append(request)
        elif direction == "negative":
            self.down_requests[request.start_floor].append(request)
        

    def sort_requests(self):
        # Sorts up_requests in ascending order of destination
        for floor in self.up_requests:
            self.up_requests[floor].sort(key=lambda r: r.destination_floor)
        
        # Sorts down_requests in descending order of destination
        for floor in self.down_requests:
            self.down_requests[floor].sort(key=lambda r: r.destination_floor, reverse=True)

    # This function isn't used but can be used to show the requests
    def display_requests(self):
        print("Up requests:", self.up_requests)
        print("Down requests:", self.down_requests)

    # This function returns a boolean value depending on if there is anything in the up_requests dictionary
    def check_if_up_requests(self):
        for floor in self.up_requests:
            if self.up_requests[floor]:  
                return True
        return False
    
    # This function returns a boolean value depending on if there is anything in the down_requests dictionary
    def check_if_down_requests(self):
        for floor in self.down_requests:
            if self.down_requests[floor]:
                return True
        return False
    
    # This function returns a boolean value depending on if there are any up requests at the lift's current floor
    def check_if_up_requests_at_current_floor(self):
        if self.up_requests[self.current_floor]:
            return True
        return False
    
    # This function returns a boolean value depending on if there are any down requests at the lift's current floor
    def check_if_down_requests_at_current_floor(self):
        if self.down_requests[self.current_floor]:
            return True
        return False
    
    # This function returns a boolean value depending on if there are any up requests above the lift's current floor
    def check_if_up_requests_above_floor(self):
        for floor in self.up_requests:  
            if self.up_requests[floor] and self.up_requests[floor][0].start_floor > self.current_floor:
                return True
        return False
    
    # This function returns a boolean value depending on if there are any down requests below the lift's current floor
    def check_if_down_requests_below_floor(self):
        for floor in self.down_requests:
            if self.down_requests[floor] and self.down_requests[floor][0].start_floor < self.current_floor:
                return True
        return False
    
    # This function returns a boolean value depending on if there are any passengers currently in the lift
    def check_if_active_requests(self):
        if len(self.active_requests) != 0:
            return True
        return False

    # This function returns True if the lift's current floor is at or below the lowest start floor in up_requests
    def is_current_floor_at_or_below_lowest_up_request(self):
        for floor in sorted(self.up_requests.keys()):  
            if self.up_requests[floor]:  
                return self.current_floor <= floor
        return None  

    # This function returns True if the lift's current floor is at or above the highest start floor in down_requests
    def is_current_floor_at_or_below_highest_down_request(self):
        for floor in sorted(self.down_requests.keys(), reverse=True):  
            if self.down_requests[floor]:  
                return self.current_floor >= floor
        return None

    # This function picks up passengers from up_requests
    def pick_up_up_passengers(self):

        # This flag is used so time only increases by 4 when picking up passengers, no matter if there is 1 passenger or 4 passengers for example
        enter_time_incremented = False

        # This flag is being used so if passengers are picked up and dropped off at the same floor, time still only increases by 4
        picked_up_passengers  = False

        # Picks up as many passengers as it can at the current floor
        while self.up_requests[self.current_floor] and self.current_capacity < self.max_capacity:

            # Removes the first request at the lift's current floor and appends this to the active_requests list
            passenger = self.up_requests[self.current_floor].pop(0)
            self.active_requests.append(passenger)

            # Increment's the lift's current capacity and updates the lift's available capacity
            self.current_capacity += 1
            self.available_capacity = self.max_capacity - self.current_capacity
            picked_up_passengers  = True # Sets flag to true
            
            if not enter_time_incremented:
                self.time_elapsed += self.enter_exit_time
                enter_time_incremented = True
            
            print(f"Picked up passenger at floor {self.current_floor} going to {passenger.destination_floor}")

        # Returns flag as it is needed as a condition in the function for dropping off passengers
        return picked_up_passengers 
    
    # This function picks up passengers from down_requests
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

    # This function uses the 2 previously defined functions to pick up all passengers based on their request direction
    def pick_up_passengers(self):
        picked_up_passengers = False

        if self.up_requests[self.current_floor] and self.direction == "positive":
            picked_up_passengers = self.pick_up_up_passengers()
        elif self.down_requests[self.current_floor] and self.direction == "negative":
            picked_up_passengers = self.pick_up_down_passengers()

        print(f"Active requests: {self.active_requests}")
        return picked_up_passengers

    # This function moves the lift in an upwards direction
    def move_lift_up(self):
        self.current_floor += 1
        self.time_elapsed += self.travel_time
        print(f"Lift moving up to floor {self.current_floor}")

    # This function moves the lift in a downwards direction
    def move_lift_down(self):
        self.current_floor -= 1
        self.time_elapsed += self.travel_time
        print(f"Lift moving down to floor {self.current_floor}")

    # This function uses the previous 2 functions to move the lift depending on its direction
    def move_lift(self):
        if self.direction == "positive":
            self.move_lift_up()
        else:
            self.move_lift_down()

    # This function used to drop the passengers from inside the lift to their destination floor
    def drop_off_passengers(self, picked_up_passengers):
        exit_time_incremented = False

        # This flag checks if passengers have been dropped off
        drop_off_passengers = False

        # Loops through each passenger in a copy of the active_requests list
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

        # This ensures the time only increases by 4 if passengers leave and enter the lift at the same floor and not 8
        if  picked_up_passengers and drop_off_passengers:
            self.time_elapsed -= self.enter_exit_time

    # This function changes the lift direction
    def change_lift_direction(self):
        if self.direction == "positive":
            self.direction = "negative"
        else:
            self.direction = "positive"

    # This function is used to run the MyLift algorithm on the requests
    def run(self):
        while self.check_if_up_requests() or self.check_if_down_requests() or self.check_if_active_requests():

            # It checks if it can pick up passengers at the current floor, moves the lift to the next floor and then checks to see if it can drop off passengers  
            picked_up_passengers = self.pick_up_passengers()
            self.move_lift()
            self.drop_off_passengers(picked_up_passengers)

            # This logic is responsible for changing the lift's direction
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

        # This returns the time it took for the lift algorithm to complete all of the requests
        return self.time_elapsed