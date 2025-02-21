from collections import defaultdict
from QueueObject import Queue
from Request import Request
from Lift import Lift

class Elevator:
    def __init__(self, floors, capacity, initial_floor=0):
        self.floors = floors  # Total number of floors
        self.Lift = Lift()  # Lift capacity
        self.current_floor = initial_floor  # Elevator starts here

        # Separate queues for UP and DOWN direction
        self.up_queue = Queue()
        self.down_queue = Queue()
        self.passenger_destinations = defaultdict(int)  # Tracks people inside the elevator

    def add_request(self, floor, destinations):
        """ Adds floor requests to appropriate queue """
        if 0 <= floor < self.floors:
            if Request.destination_floor > Request.start_floor:
                self.up_queue.enqueue(Request)  # Request to go UP
            elif Request.destination_floor < Request.start_floor:
                self.down_queue.enqueue(Request)  # Request to go DOWN

    def determine_initial_direction(self):
        """ Determines if the elevator should move UP or DOWN based on nearest request """
        if self.up_queue.peek() and (not self.down_queue.peek() or self.up_queue.peek().start_floor < self.down_queue.peek().start_floor):
            return "UP"
        elif self.down_queue.peek():
            return "DOWN"
        return "IDLE"

    def scan_algorithm(self):
        """ Implements the SCAN (Elevator) algorithm """
        if not self.up_queue.ppek() and not self.down_queue.peek() and not self.passenger_dewstinations:
            print("No pending requests.")
            return

        # Sort queues to process requests in order
        highest_floor = self.floors - 1
        lowest_floor = 0
        current_passenger_count = 0  # Track number of passengers currently in the lift

        skipped_passengers_up = []  # Store skipped passengers during UP phase
        skipped_passengers_down = []  # Store skipped passengers during DOWN phase

        # Process UP direction
        print("\nMoving UP:")
        while self.up_queue.peek():
            request = self.up_queue.dequeue()

            # Check if there's enough space for the passenger
            if current_passenger_count < self.Lift.capacity:
                self.current_floor = request.start_floor
                print(
                    f" Elevator stopping at floor {self.current_floor} - Picking up passenger for floor {request.destination_floor}")
                current_passenger_count += 1  # Add the passenger to the lift
                self.passenger_destinations[request.destination_floor] += 1
            else:
                # If lift is full, store the passenger to retry later
                skipped_passengers_up.append(request)
                print(f" Elevator full, can't pick up passenger at floor {request.start_floor} - Skipping for now")
                break  # Stop picking up more passengers if the lift is full

        # Drop passengers at their destination floors (grouped)
        while self.passenger_destinations:
            next_floor = min(self.passenger_destinations.keys())
            self.current_floor = next_floor
            print(
                f" Elevator stopping at floor {self.current_floor} - Dropping off {self.passenger_destinations[next_floor]} passengers")
            current_passenger_count -= self.passenger_destinations[next_floor]  # Remove passengers from the lift
            del self.passenger_destinations[next_floor]

        # Move to the top floor before reversing direction
        while self.current_floor < highest_floor:
            self.current_floor += 1
            print(f" Elevator passing floor {self.current_floor}")

        # Re-enqueue skipped passengers
        while skipped_passengers_up:
            passenger = skipped_passengers_up.pop(0)
            self.up_queue.enqueue(passenger)  # Re-add the passengers back to the queue
            print(f" Re-enqueueing skipped passenger for floor {passenger.destination_floor}")

        # Process DOWN direction
        print("\nMoving DOWN:")
        while self.down_queue.peek():
            request = self.down_queue.dequeue()

            # Check if there's enough space for the passenger
            if current_passenger_count < self.Lift.capacity:
                self.current_floor = request.start_floor
                print(
                    f" Elevator stopping at floor {self.current_floor} - Picking up passenger for floor {request.destination_floor}")
                current_passenger_count += 1  # Add the passenger to the lift
                self.passenger_destinations[request.destination_floor] += 1
            else:
                # If lift is full, store the passenger to retry later
                skipped_passengers_down.append(request)
                print(f" Elevator full, can't pick up passenger at floor {request.start_floor} - Skipping for now")
                break  # Stop picking up more passengers if the lift is full

        # Drop passengers at their destination floors (grouped)
        while self.passenger_destinations:
            next_floor = max(self.passenger_destinations.keys())
            self.current_floor = next_floor
            print(
                f" Elevator stopping at floor {self.current_floor} - Dropping off {self.passenger_destinations[next_floor]} passengers")
            current_passenger_count -= self.passenger_destinations[next_floor]  # Remove passengers from the lift
            del self.passenger_destinations[next_floor]

        # Move to the bottom floor before reversing again
        while self.current_floor > lowest_floor:
            self.current_floor -= 1
            print(f" Elevator passing floor {self.current_floor}")

        # Re-enqueue skipped passengers
        while skipped_passengers_down:
            passenger = skipped_passengers_down.pop(0)
            self.down_queue.enqueue(passenger)  # Re-add the passengers back to the queue
            print(f" Re-enqueueing skipped passenger for floor {passenger.destination_floor}")

def read_input_file(filename):
    """ Reads input file and extracts elevator configurations """
    try:
        with open(filename, "r") as file:
            lines = file.readlines()

        floors, capacity = 0, 0
        requests = {}

        for line in lines:
            line = line.strip()

            if line.startswith("#") or not line:
                continue

            if "," in line and floors == 0:
                # Read total floors and lift capacity
                floors, capacity = map(int, line.split(","))
            else:
                # Read floor requests
                floor_data = line.split(":")
                floor_num = int(floor_data[0].strip())

                if floor_data[1].strip():
                    destinations = list(map(int, floor_data[1].split(",")))
                else:
                    destinations = []

                requests[floor_num] = destinations

        return floors, capacity, requests
    except Exception as e:
        print(f"Error reading input file: {e}")
        return None, None, None

def main():
    print("Welcome to the Elevator System (SCAN Algorithm)")

    filename = input("Enter the input file name (e.g., input.txt): ")
    floors, capacity, requests = read_input_file(filename)

    if floors is None or capacity is None:
        print("Invalid input file. Exiting.")
        return

    print(f"Building has {floors} floors, Lift Capacity: {capacity}")
    print(f"Floor Requests: {requests}")

    elevator = Elevator(floors, capacity)

    for floor, destinations in requests.items():
        for destination in destinations:
            request = Request(floor, destination)
            elevator.add_request(request)

    print("\n Processing requests using SCAN algorithm:")
    elevator.scan_algorithm()

if __name__ == "__main__":
    main()
