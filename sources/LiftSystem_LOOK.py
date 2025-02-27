from PriorityQueue_LOOK import PriorityQueue_LOOK
from Lift import Lift
from Request import Request
class LiftSystem_LOOK:
    def __init__(self, total_floors, travel_time=2, exit_time=4):
        self.total_floors = total_floors
        self.Lift = Lift(capacity=5, travel_time=travel_time, exit_time=exit_time)  # UPDATED: Initialize Lift with travel_time and exit_time
        self.priority_queue = PriorityQueue_LOOK(self.Lift)

    def run(self):
        """
        Runs the LOOK algorithm and returns the total time taken.
        """
        while self.priority_queue.Active_Queue or self.priority_queue.Waiting_Queue:
            if self.Lift.lift_direction == "positive":
                self.priority_queue.MinHeap()
                next_stop = min([floor for floor in self.priority_queue.MinHeap_Queue if floor > self.Lift.current_floor], default=None)
            else:
                self.priority_queue.MaxHeap()
                next_stop = max([floor for floor in self.priority_queue.MaxHeap_Queue if floor < self.Lift.current_floor], default=None)

            if next_stop is None:
                print("No more requests. Lift is idle.")
                break

            # Move lift to next stop
            self.Lift.time_elapsed += abs(next_stop - self.Lift.current_floor) * self.Lift.travel_time  # UPDATED: Use self.Lift.travel_time
            self.Lift.current_floor = next_stop

            # Handle requests at current floor
            self.priority_queue.Removing_requests_from_Active_and_MaxMinHeap()
            self.Lift.time_elapsed += len([req for req in self.priority_queue.Active_Queue if req.destination_floor == self.Lift.current_floor]) * self.Lift.exit_time  # UPDATED: Use self.Lift.exit_time

            # Reload from Waiting Queue if Active Queue is empty
            if not self.priority_queue.Active_Queue and self.priority_queue.Waiting_Queue:
                self.priority_queue.Loading_Waiting_to_Active()

        return self.Lift.time_elapsed  # UPDATED: Return self.Lift.time_elapsed
    
    #Picks up passengers based on priority and available space
    def pick_up_passengers(self, request:Request):
        print(f"Adding request: {request.start_floor} -> {request.destination_floor}")  # Debugging
        self.priority_queue.loading_Request_into_Active_Waiting(request)
        self.priority_queue.Loading_Waiting_to_Active()

        # Print the queue to see if requests are being added
        print(f"Active Queue: {[f'{req.start_floor}->{req.destination_floor}' for req in self.priority_queue.Active_Queue]}")
        print(f"Waiting Queue: {[f'{req.start_floor}->{req.destination_floor}' for req in self.priority_queue.Waiting_Queue]}")


    def request_move_lift(self):
        print("🚀 Starting LOOK algorithm processing...")

        while self.priority_queue.Active_Queue or self.priority_queue.Waiting_Queue or self.priority_queue.MaxHeap_Queue or self.priority_queue.MinHeap_Queue:
            print(f"Active Queue: {[f'{req.start_floor}->{req.destination_floor}' for req in self.priority_queue.Active_Queue]}")
            print(f"Waiting Queue: {[f'{req.start_floor}->{req.destination_floor}' for req in self.priority_queue.Waiting_Queue]}")
            print(f"MinHeap Queue: {self.priority_queue.MinHeap_Queue}")
            print(f"MaxHeap Queue: {self.priority_queue.MaxHeap_Queue}")

            # If Active Queue is empty, check for waiting requests or switch direction
            if not self.priority_queue.Active_Queue:
                if self.priority_queue.Waiting_Queue:
                    self.priority_queue.Loading_Waiting_to_Active()
                elif self.Lift.lift_direction == "positive" and self.priority_queue.MaxHeap_Queue:
                    print("🔄 No more upward requests. Switching to downward.")
                    self.Lift.lift_direction = "negative"
                    self.priority_queue.MaxHeap()
                elif self.Lift.lift_direction == "negative" and self.priority_queue.MinHeap_Queue:
                    print("🔄 No more downward requests. Switching to upward.")
                    self.Lift.lift_direction = "positive"
                    self.priority_queue.MinHeap()
                else:
                    print("✅ No more requests left. Lift stopping.")
                    return

            # Get the next stop based on direction
            if self.Lift.lift_direction == "positive":
                self.priority_queue.MinHeap()
                next_stop = min([floor for floor in self.priority_queue.MinHeap_Queue if floor > self.Lift.current_floor], default=None)
            else:
                self.priority_queue.MaxHeap()
                next_stop = max([floor for floor in self.priority_queue.MaxHeap_Queue if floor < self.Lift.current_floor], default=None)

            if next_stop is None:
                print("❌ No valid next stop, but there are remaining requests. Checking again...")
                continue  # Ensure it re-checks remaining requests

            # 🚀 Move the lift
            print(f"🚀 Lift moving from {self.Lift.current_floor} to floor {next_stop}...")
            self.Lift.current_floor = next_stop
            print(f"Before Removing: MinHeap Queue: {self.priority_queue.MinHeap_Queue}")
            print(f"Before Removing: MaxHeap Queue: {self.priority_queue.MaxHeap_Queue}")

            # Check if the current floor is a destination for any request
            self.priority_queue.Removing_requests_from_Active_and_MaxMinHeap()

            print(f"After Removing: MinHeap Queue: {self.priority_queue.MinHeap_Queue}")
            print(f"After Removing: MaxHeap Queue: {self.priority_queue.MaxHeap_Queue}")

            # If Active Queue is empty but there are still waiting requests, load them
            if not self.priority_queue.Active_Queue and self.priority_queue.Waiting_Queue:
                self.priority_queue.Loading_Waiting_to_Active()

        print("✅ All LOOK requests processed. Lift stopping.")

    def add_request(self, request:Request):
        # Handles new requests dynamically.
        if request.request_direction() is None:
            print(f"Invalid request: Start floor {request.start_floor} == Destination floor {request.destination_floor}")
            return
        self.pick_up_passengers(request)  # Add request to queue

class LOOK:
    def __init__(self, total_floors_and_capacity, requests, time_between_floors, time_to_exit):
        self.total_floors = total_floors_and_capacity[0]
        self.capacity = total_floors_and_capacity[1]
        self.requests = requests
        self.time_between_floors = time_between_floors
        self.time_to_exit = time_to_exit

    def calculate_total_time(self):
        # Initialize the lift system with the given parameters
        lift_system = LiftSystem_LOOK(self.total_floors, self.time_between_floors, self.time_to_exit)
        lift_system.Lift.capacity = self.capacity  # Set lift capacity

        # Add requests to the system
        for start_floor, destinations in self.requests.items():
            for destination_floor in destinations:
                lift_system.add_request(Request(start_floor, destination_floor))

        # Run the simulation and return the total time elapsed
        return lift_system.run()

    def get_total_time(self):
        return self.calculate_total_time()

    def run(self):
        return self.calculate_total_time()
    
if __name__ == "__main__":
    # Create lift system
    lift_system = LiftSystem_LOOK(total_floors=10)

    # Add test requests
    request1 = Request(1, 5)  # Moving up
    request2 = Request(3, 7)  # Moving up
    request3 = Request(8, 2)  # Moving down
    request4 = Request(4, 7)  # Moving up
    request5 = Request(6, 1)  # Moving down

    # Add requests to the system
    lift_system.add_request(request1)
    lift_system.add_request(request2)
    lift_system.add_request(request3)
    lift_system.add_request(request4)
    lift_system.add_request(request5)

    # Start moving the lift
    print("\n Starting Lift System Execution...\n")
    lift_system.request_move_lift()
