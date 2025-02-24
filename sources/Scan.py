from collections import defaultdict
from QueueObject import Queue
from Request import Request
from Lift import Lift

class Elevator:
    def __init__(self, floors, initial_floor=0):
        self.floors = floors  # Total number of floors
        self.Lift = Lift()  # Lift capacity
        self.current_floor = initial_floor  # Elevator starts here

        # Separate queues for UP and DOWN direction
        self.up_queue = Queue()
        self.down_queue = Queue()
        self.passenger_destinations = defaultdict(int)  # Tracks people inside the elevator
        self.current_passenger_count = 0

    def add_request(self, request):
        """ Adds floor requests to appropriate queue """
        if 0 <= request.start_floor < self.floors:
            if request.destination_floor > request.start_floor:
                if self.current_passenger_count < self.Lift.capacity + 1:
                    self.up_queue.enqueue(request)
                    print(f"Added request UP: {request.start_floor} -> {request.destination_floor}")
                else:
                    print(f"Lift full. Skipping request UP: {request.start_floor} -> {request.destination_floor}")
            elif request.destination_floor < request.start_floor:
                if self.current_passenger_count < self.Lift.capacity + 1:
                    self.down_queue.enqueue(request)  # Request to go DOWN
                    print(f"Added request DOWN: {request.start_floor} -> {request.destination_floor}")
                else:
                    print(f"Lift full. Skipping request DOWN: {request.start_floor} -> {request.destination_floor}")

    def scan_algorithm(self):
        """ Implements the SCAN (Elevator) algorithm """
        if not self.up_queue.peek() and not self.down_queue.peek() and not self.passenger_destinations:
            print("No pending requests.")
            return

        highest_floor = self.floors
        lowest_floor = 1

        skipped_passengers_up = []  # Store skipped passengers during UP phase
        skipped_passengers_down = []  # Store skipped passengers during DOWN phase

        # Process UP direction
        print("\nMoving UP:")
        while self.up_queue.peek():
            request = self.up_queue.dequeue()

            # Check if there's enough space for the passenger
            if self.current_passenger_count < self.Lift.capacity + 1:
                self.current_floor = request.start_floor
                print(f" Elevator stopping at floor {self.current_floor} - Picking up passenger for floor {request.destination_floor}")
                self.current_passenger_count += 1  # Add the passenger to the lift
                self.passenger_destinations[request.destination_floor] += 1
            else:
                # If lift is full, store the passenger to retry later
                skipped_passengers_up.append(request)
                print(f" Elevator full, can't pick up passenger at floor {request.start_floor} - Skipping for now")
                    

        # Drop passengers at their destination floors
        while self.passenger_destinations:
            next_floor = min(self.passenger_destinations.keys())
            self.current_floor = next_floor
            print(f" Elevator stopping at floor {self.current_floor} - Dropping off {self.passenger_destinations[next_floor]} passengers")
            self.current_passenger_count -= self.passenger_destinations[next_floor]  # Remove passengers from the lift
            del self.passenger_destinations[next_floor]

        # Move to the top floor before reversing direction
        while self.current_floor < highest_floor:
            self.current_floor += 1
            print(f" Elevator passing floor {self.current_floor}")

        # Re-enqueue skipped passengers
        while skipped_passengers_up:
            passenger = skipped_passengers_up.pop(0)
            self.up_queue.enqueue(passenger)  # Re-add the passengers back to the queue
            
        # Process DOWN direction
        print("\nMoving DOWN:")

        # Sort the down_queue in descending order to process from highest to lowest
        down_requests = []
        while not self.down_queue.is_empty():
            down_requests.append(self.down_queue.dequeue())

        # Sort in descending order by start_floor for correct downward movement
        down_requests.sort(key=lambda req: req.start_floor, reverse=True)
        for request in down_requests:

            # Check if there's enough space for the passenger
            if self.current_passenger_count < self.Lift.capacity + 1:
                self.current_floor = request.start_floor
                print(f" Elevator stopping at floor {self.current_floor} - Picking up passenger for floor {request.destination_floor}")
                self.current_passenger_count += 1  # Add the passenger to the lift
                self.passenger_destinations[request.destination_floor] += 1
            else:
                # If lift is full, store the passenger to retry later
                skipped_passengers_down.append(request)
                print(f" Elevator full, can't pick up passenger at floor {request.start_floor} - Skipping for now")
                 # Stop picking up more passengers if the lift is full

        # Drop passengers at their destination floors (grouped)
        while self.passenger_destinations:
            next_floor = max(self.passenger_destinations.keys())
            self.current_floor = next_floor
            print(f" Elevator stopping at floor {self.current_floor} - Dropping off {self.passenger_destinations[next_floor]} passengers")
            self.current_passenger_count -= self.passenger_destinations[next_floor]  # Remove passengers from the lift
            del self.passenger_destinations[next_floor]

        # Move to the bottom floor before reversing again
        while self.current_floor > lowest_floor:
            self.current_floor -= 1
            print(f" Elevator passing floor {self.current_floor}")

        # Re-enqueue skipped passengers
        while skipped_passengers_down:
            passenger = skipped_passengers_down.pop(0)
            self.down_queue.enqueue(passenger)  # Re-add the passengers back to the queue
            
    def run(self):
        """ Main loop for processing requests """
        while not self.up_queue.is_empty() or not self.down_queue.is_empty() or self.passenger_destinations:
            self.scan_algorithm()

def main():
    print("Welcome to the Elevator System (SCAN Algorithm)")

    floors = 12
    capacity = 6  # Lift Capacity

    elevator = Elevator(floors, capacity)

    # Sample requests
    requests = {
        1: [5, 3, 8, 10],
        2: [4, 6, 11, 12],
        3: [2, 4, 9],
        4: [12, 10, 2],
        5: [7, 9, 11],
        6: [10, 3, 8],
    }

    print(f"Building has {floors} floors, Lift Capacity: {capacity}")
    print(f"Floor Requests: {requests}")

    elevator = Elevator(floors, capacity)

    for floor, destinations in requests.items():
        for destination in destinations:
            request = Request(floor, destination)
            elevator.add_request(request)

    print("\n Processing requests using SCAN algorithm:")
    elevator.run()

if __name__ == "__main__":
    main()