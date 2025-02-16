from collections import deque

class Elevator:
    def __init__(self, floors, capacity, initial_floor=0):
        self.floors = floors  # Total number of floors
        self.capacity = capacity  # Lift capacity
        self.current_floor = initial_floor  # Elevator starts here

        # Separate queues for UP and DOWN direction
        self.up_queue = deque()
        self.down_queue = deque()
        self.passenger_destinations = deque()  # Tracks people inside the elevator

    def add_request(self, floor, destinations):
        """ Adds floor requests to appropriate queue """
        if 0 <= floor < self.floors:
            for dest in destinations:
                if dest > floor:
                    self.up_queue.append((floor, dest))  # Requests to go UP
                elif dest < floor:
                    self.down_queue.append((floor, dest))  # Requests to go DOWN

    def determine_initial_direction(self):
        """ Determines if the elevator should move UP or DOWN based on nearest request """
        if self.up_queue and (not self.down_queue or min(self.up_queue)[0] < max(self.down_queue)[0]):
            return "UP"
        elif self.down_queue:
            return "DOWN"
        return "IDLE"

    def scan_algorithm(self):
        """ Implements the SCAN (Elevator) algorithm """
        if not self.up_queue and not self.down_queue:
            print("No pending requests.")
            return

        # Sort queues to process requests in order
        self.up_queue = deque(sorted(self.up_queue, key=lambda x: x[0]))
        self.down_queue = deque(sorted(self.down_queue, key=lambda x: x[0], reverse=True))

        # Determine starting direction
        direction = self.determine_initial_direction()
        if direction == "IDLE":
            print("No valid requests to process.")
            return

        highest_floor = self.floors - 1
        lowest_floor = 0

        # Process UP direction
        print("\n Moving UP:")
        while self.up_queue:
            request = self.up_queue.popleft()
            pickup_floor, destination = request
            self.current_floor = pickup_floor
            print(f" Elevator stopping at floor {pickup_floor} - Picking up passenger for floor {destination}")

            # Add passenger's destination to queue
            self.passenger_destinations.append(destination)

            # Move toward destination floors in order
            while self.passenger_destinations:
                self.current_floor = min(self.passenger_destinations)
                print(f" Elevator stopping at floor {self.current_floor} - Dropping off passenger")
                self.passenger_destinations.remove(self.current_floor)

        # Move to the top floor before reversing direction
        while self.current_floor < highest_floor:
            self.current_floor += 1
            print(f" Elevator passing floor {self.current_floor}")

        # Process DOWN direction
        print("\n Moving DOWN:")
        while self.down_queue:
            request = self.down_queue.popleft()
            pickup_floor, destination = request
            self.current_floor = pickup_floor
            print(f" Elevator stopping at floor {pickup_floor} - Picking up passenger for floor {destination}")

            # Add passenger's destination to queue
            self.passenger_destinations.append(destination)

            # Move toward destination floors in order
            while self.passenger_destinations:
                self.current_floor = max(self.passenger_destinations)
                print(f" Elevator stopping at floor {self.current_floor} - Dropping off passenger")
                self.passenger_destinations.remove(self.current_floor)

        # Move to the bottom floor before reversing again
        while self.current_floor > lowest_floor:
            self.current_floor -= 1
            print(f" Elevator passing floor {self.current_floor}")

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
        elevator.add_request(floor, destinations)

    print("\n Processing requests using SCAN algorithm:")
    elevator.scan_algorithm()

if __name__ == "__main__":
    main()
