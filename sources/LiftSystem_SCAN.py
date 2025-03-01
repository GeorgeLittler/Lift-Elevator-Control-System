from LiftSystem_LOOK import LiftSystem_LOOK
from Request import Request
from PriorityQueue_SCAN import PriorityQueue_SCAN
class LiftSystem_SCAN(LiftSystem_LOOK):
    def __init__(self, total_floors, travel_time=2, exit_time=4):
        super().__init__(total_floors, travel_time, exit_time)  #initialising base class with travel_time and exit_time
        self.priority_queue = PriorityQueue_SCAN(self.Lift)

    def run(self):#Runs the SCAN algorithm and returns the total time taken.
        while self.priority_queue.Active_Queue or self.priority_queue.Waiting_Queue or self.priority_queue.MinHeap_Queue or self.priority_queue.MaxHeap_Queue:

            if self.Lift.lift_direction == "positive":
                self.priority_queue.MinHeap()
                next_stop = self.priority_queue.get_next_stop()
            else:
                self.priority_queue.MaxHeap()
                next_stop = self.priority_queue.get_next_stop()

            if next_stop is None:
                print("No more requests. Lift is idle.")
                break

            #moving lift to next stop
            self.Lift.time_elapsed += abs(next_stop - self.Lift.current_floor) * self.Lift.travel_time  #use self.Lift.travel_time
            self.Lift.current_floor = next_stop

            #handle requests at current floor
            self.priority_queue.Removing_requests_from_Active_and_MaxMinHeap()
            for req in self.priority_queue.Active_Queue:
                if req.destination_floor==self.Lift.current_floor:
                    self.Lift.time_elapsed += self.Lift.exit_time
                    break
            
                elif req.start_floor==self.Lift.current_floor:
                    self.Lift.time_elapsed += self.Lift.exit_time
                    break
            #updating queues and check for direction changes
            self.priority_queue.update_queues()
            self.priority_queue.check_direction_change()

            #reload from Waiting Queue if Active Queue is empty
            if not self.priority_queue.Active_Queue and self.priority_queue.Waiting_Queue:
                next_stop = self.priority_queue.check_direction_change()
                self.Lift.time_elapsed += abs(next_stop - self.Lift.current_floor) * self.Lift.travel_time  #use self.Lift.travel_time
                self.Lift.current_floor = next_stop

                if self.Lift.current_floor == self.priority_queue.total_floors:
                    self.Lift.lift_direction = "negative"
                    self.priority_queue.Loading_Waiting_to_Active()
                elif self.Lift.current_floor == 0:
                    self.Lift.lift_direction = "positive"
                    self.priority_queue.Loading_Waiting_to_Active()

        return self.Lift.time_elapsed  #return self.Lift.time_elapsed
   
    def request_move_lift(self):
        print("Starting SCAN algorithm processing...")

        while self.priority_queue.Active_Queue or self.priority_queue.Waiting_Queue or self.priority_queue.MaxHeap_Queue:
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
                    self.Lift.lift_direction = "negative"
                    self.priority_queue.MaxHeap()
                elif self.Lift.lift_direction == "negative" and self.priority_queue.MinHeap_Queue:
                    print("No more downward requests. Switching to upward.")
                    self.Lift.lift_direction = "positive"
                    self.priority_queue.MinHeap()
                else:
                    print("No more requests left. Lift stopping.")
                    return

            #get the next stop based on direction
            next_stop = self.priority_queue.get_next_stop()

            if next_stop is None:
                print("No valid next stop, but there are remaining requests. Checking again...")
                continue  #ensuring it re checks remaining requests
            
            
            #move the lift
            print(f"Lift moving from {self.Lift.current_floor} to floor {next_stop}...")
            self.Lift.current_floor = next_stop
            print(f"Before Removing: MinHeap Queue: {self.priority_queue.MinHeap_Queue}")
            print(f"Before Removing: MaxHeap Queue: {self.priority_queue.MaxHeap_Queue}")

            self.priority_queue.Removing_requests_from_Active_and_MaxMinHeap()

            print(f"After Removing: MinHeap Queue: {self.priority_queue.MinHeap_Queue}")
            print(f"After Removing: MaxHeap Queue: {self.priority_queue.MaxHeap_Queue}")

            #if Active Queue is empty but there are still waiting requests, load them
            if not self.priority_queue.Active_Queue and self.priority_queue.Waiting_Queue:
                self.priority_queue.Loading_Waiting_to_Active()

        print("All SCAN requests processed. Lift stopping.")

class SCAN:
    def __init__(self, total_floors, max_capacity, requests, time_between_floors, time_to_exit):
        self.total_floors = total_floors
        self.capacity = max_capacity
        self.requests = requests
        self.time_between_floors = time_between_floors
        self.time_to_exit = time_to_exit

    def calculate_total_time(self):
        #initialise the lift system with the given parameters
        lift_system = LiftSystem_SCAN(self.total_floors, self.time_between_floors, self.time_to_exit)
        lift_system.Lift.capacity = self.capacity  # Set lift capacity

        #add requests to the system
        for start_floor, destinations in self.requests.items():
            for destination_floor in destinations:
                lift_system.add_request(Request(start_floor, destination_floor))

        #run the simulation and return the total time elapsed
        return lift_system.run()

                     
if __name__ == "__main__":
    #create lift system
    lift_system = LiftSystem_SCAN(total_floors=10)

    # add test requests
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
    print("\n Starting Lift System Execution using SCAN algorithm...\n")
    lift_system.request_move_lift()