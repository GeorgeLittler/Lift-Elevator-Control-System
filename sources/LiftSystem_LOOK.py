
from PriorityQueue_LOOK import PriorityQueue_LOOK
from Lift1 import Lift1
from Request import Request
class LiftSystem_LOOK:
    def __init__(self, total_floors, travel_time=2, exit_time=4):
        self.Lift = Lift1(total_floors=total_floors,max_capacity=5, travel_time=travel_time, enter_exit_time=exit_time) #initialising lift with travel_time and exit_time
        self.priority_queue = PriorityQueue_LOOK(self.Lift)
        

    def run(self):#runs the LOOK algorithm and returns the total time taken.
        
        print("Starting LOOK algorithm...")
        while self.priority_queue.Active_Queue or self.priority_queue.Waiting_Queue or self.priority_queue.MinHeap_Queue or self.priority_queue.MaxHeap_Queue:
            print(f"Current Floor: {self.Lift.current_floor}, Direction: {self.Lift.lift_direction}")
            print(f"Active Queue: {[f'{req.start_floor}->{req.destination_floor}' for req in self.priority_queue.Active_Queue]}")
            print(f"Waiting Queue: {[f'{req.start_floor}->{req.destination_floor}' for req in self.priority_queue.Waiting_Queue]}")
            print(f"MinHeap Queue: {self.priority_queue.MinHeap_Queue}")
            print(f"MaxHeap Queue: {self.priority_queue.MaxHeap_Queue}")

            #If this is the first move in the sequence, choose the closest floor instead of following direction
            if self.priority_queue.just_started or not self.priority_queue.Active_Queue:
                 #Collect all possible stops from the Active Queue
                all_stops = ([req.start_floor for req in self.priority_queue.Active_Queue] +
                         [req.destination_floor for req in self.priority_queue.Active_Queue])
                #Find the closest floor to the current position
                next_stop = min(all_stops, key=lambda x: abs(x - self.Lift.current_floor), default=None)
                self.priority_queue.just_started = False  #reseting flag after the first move
            else:
                #If the lift is moving upwards, use the MinHeap to find the next stop
                if self.Lift.lift_direction == "positive":
                    self.priority_queue.MinHeap()
                    next_stop = min([floor for floor in self.priority_queue.MinHeap_Queue 
                         if floor > self.Lift.current_floor], default=None)
                else:
                    #If the lift is moving downwards, use the MaxHeap to find the next stop
                    self.priority_queue.MaxHeap()
                    next_stop = max([floor for floor in self.priority_queue.MaxHeap_Queue 
                         if floor < self.Lift.current_floor], default=None)
                #If no more requests in the current direction, switch direction
                if next_stop is None:
                    print("No more requests in this direction. Switching direction.")
                    if self.Lift.lift_direction == "positive":
                        self.Lift.lift_direction = "negative"
                        self.priority_queue.MaxHeap()
                        next_stop = max([floor for floor in self.priority_queue.MaxHeap_Queue 
                             if floor < self.Lift.current_floor], default=None)
                    else:
                        self.Lift.lift_direction = "positive"
                        self.priority_queue.MinHeap()
                        next_stop = min([floor for floor in self.priority_queue.MinHeap_Queue 
                             if floor > self.Lift.current_floor], default=None)

                    if next_stop is None:
                        print("No more requests left. Lift stopping.")
                        break  #Exit the loop if no more requests are left

            #Eensuring next_stop is not None before calculating travel_distance
            if next_stop is None:
                print("No valid next stop found. Exiting...")
                break

            print(f"Next Stop: {next_stop}")  

            #Calculate the travel time based on the distance to the next stop
            travel_distance = abs(next_stop - self.Lift.current_floor)
            travel_time = travel_distance * self.Lift.travel_time  #2 seconds per floor
            self.Lift.time_elapsed += travel_time

            # Move lift to next stop
            self.Lift.current_floor = next_stop
            self.Lift.visited_floors.add(next_stop)  #Mark the floor as visited

            #handling requests at current floor , if there is passengers leaving the floor
            self.priority_queue.Removing_requests_from_Active_and_MaxMinHeap()

            #reloading from Waiting Queue if Active Queue is empty
            if not self.priority_queue.Active_Queue and self.priority_queue.Waiting_Queue:
                self.priority_queue.Loading_Waiting_to_Active()

        return self.Lift.time_elapsed
    
    #picks up passengers based on priority and available space
    def pick_up_passengers(self, request:Request):
        #print(f"Adding request: {request.start_floor} -> {request.destination_floor}")  #Debugging
        self.priority_queue.loading_Request_into_Active_Waiting(request)
        self.priority_queue.Loading_Waiting_to_Active()

        # Print the queue to see if requests are being added ,I used this for debugging 
        #print(f"Active Queue: {[f'{req.start_floor}->{req.destination_floor}' for req in self.priority_queue.Active_Queue]}")
        #print(f"Waiting Queue: {[f'{req.start_floor}->{req.destination_floor}' for req in self.priority_queue.Waiting_Queue]}")

    def request_move_lift(self):
        print("Starting LOOK algorithm processing...")

        while self.priority_queue.Active_Queue or self.priority_queue.Waiting_Queue or self.priority_queue.MaxHeap_Queue or self.priority_queue.MinHeap_Queue:
            print(f"Active Queue: {[f'{req.start_floor}->{req.destination_floor}' for req in self.priority_queue.Active_Queue]}")
            print(f"Waiting Queue: {[f'{req.start_floor}->{req.destination_floor}' for req in self.priority_queue.Waiting_Queue]}")
            print(f"MinHeap Queue: {self.priority_queue.MinHeap_Queue}")
            print(f"MaxHeap Queue: {self.priority_queue.MaxHeap_Queue}")

            #if Active Queue is empty, check for waiting requests or switch direction
            if not self.priority_queue.Active_Queue:
                if self.priority_queue.Waiting_Queue:
                    self.priority_queue.Loading_Waiting_to_Active()
                elif self.Lift.lift_direction == "positive" and self.priority_queue.MaxHeap_Queue:
                    print("No more upward requests. Switching to downward.")
                    self.priority_queue.just_started = True
                    self.Lift.lift_direction = "negative"
                    self.priority_queue.MaxHeap()
                elif self.Lift.lift_direction == "negative" and self.priority_queue.MinHeap_Queue:
                    print("No more downward requests. Switching to upward.")
                    self.priority_queue.just_started = True
                    self.Lift.lift_direction = "positive"
                    self.priority_queue.MinHeap()
                elif not self.priority_queue.Waiting_Queue and not self.priority_queue.MaxHeap_Queue and not self.priority_queue.MinHeap_Queue:
                    print("No more requests left. Lift stopping.")
                    break  #exit the loop when no more requests are left

            #if this is the first move in the sequence, choose the closest floor instead of following direction
            if self.priority_queue.just_started or not self.priority_queue.Active_Queue:
                all_stops = ([req.start_floor for req in self.priority_queue.Active_Queue] +
                          [req.destination_floor for req in self.priority_queue.Active_Queue])
                next_stop = min(all_stops, key=lambda x: abs(x - self.Lift.current_floor), default=None)
                self.priority_queue.just_started = False  #reseting flag after the first move
            else:
                if self.Lift.lift_direction == "positive":
                    self.priority_queue.MinHeap()
                    next_stop = min([floor for floor in self.priority_queue.MinHeap_Queue if floor > self.Lift.current_floor], default=None)
                else:
                    self.priority_queue.MaxHeap()
                    next_stop = max([floor for floor in self.priority_queue.MaxHeap_Queue if floor < self.Lift.current_floor], default=None)

            if next_stop is None:
                print("No valid next stop, but there are remaining requests. Checking again...")
                continue  #ensuring it re checks remaining requests

            #move the lift
            print(f"Lift moving from {self.Lift.current_floor} to floor {next_stop}...")
            self.Lift.current_floor = next_stop
            print(f"Before Removing: MinHeap Queue: {self.priority_queue.MinHeap_Queue}")
            print(f"Before Removing: MaxHeap Queue: {self.priority_queue.MaxHeap_Queue}")

            #check if the current floor is a destination for any request
            self.priority_queue.Removing_requests_from_Active_and_MaxMinHeap()

            print(f"After Removing: MinHeap Queue: {self.priority_queue.MinHeap_Queue}")
            print(f"After Removing: MaxHeap Queue: {self.priority_queue.MaxHeap_Queue}")

            #if Active Queue is empty but there are still waiting requests, load them
            if not self.priority_queue.Active_Queue and self.priority_queue.Waiting_Queue:
                self.priority_queue.Loading_Waiting_to_Active()

        print("All LOOK requests processed. Lift stopping.")

    def add_request(self, request:Request):
        #handles new requests dynamically
        if request.request_direction() is None:
            print(f"Invalid request: Start floor {request.start_floor} == Destination floor {request.destination_floor}")
            return
        self.pick_up_passengers(request)  #add request to queue

class LOOK:
    def __init__(self, total_floors, max_capacity, requests, time_between_floors, time_to_exit):
        self.total_floors = total_floors
        self.capacity = max_capacity
        self.requests = requests
        self.time_between_floors = time_between_floors
        self.time_to_exit = time_to_exit

    def calculate_total_time(self):
        #initialise the lift system with the given parameters
        lift_system = LiftSystem_LOOK(self.total_floors, self.time_between_floors, self.time_to_exit)
        lift_system.Lift.max_capacity = self.capacity  # Set lift capacity

        #add requests to the system
        for start_floor, destinations in self.requests.items():
            for destination_floor in destinations:
                lift_system.add_request(Request(start_floor, destination_floor))

        #run the simulation and return the total time elapsed
        return lift_system.run()

if __name__ == "__main__":
    #create lift system
    lift_system = LiftSystem_LOOK(total_floors=10)

    #add test requests
    request1 = Request(1, 5)  #up
    request2 = Request(3, 7)  #up
    request3 = Request(8, 2)  #down
    request4 = Request(4, 7)  #up
    request5 = Request(6, 1)  #down

    #add requests to the system
    lift_system.add_request(request1)
    lift_system.add_request(request2)
    lift_system.add_request(request3)
    lift_system.add_request(request4)
    lift_system.add_request(request5)

    #start moving the lift
    print("\n Starting Lift System Execution...\n")
    lift_system.request_move_lift()


