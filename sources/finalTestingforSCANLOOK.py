from LiftSystem_LOOK import LOOK
from LiftSystem_SCAN import SCAN
from Request import Request

# Test data
total_floors_and_capacity = {
    'total_floors': 10,  # Building has 10 floors
    'capacity': 5        # Lift can carry 5 passengers at a time
}

# List of requests: each request is a dictionary with 'start_floor' and 'destination_floor'
requests = [
    {'start_floor': 1, 'destination_floor': 5},  # Passenger 1: Floor 1 -> Floor 5
    {'start_floor': 3, 'destination_floor': 7},  # Passenger 2: Floor 3 -> Floor 7
    {'start_floor': 8, 'destination_floor': 2},  # Passenger 3: Floor 8 -> Floor 2
    {'start_floor': 4, 'destination_floor': 9},  # Passenger 4: Floor 4 -> Floor 9
    {'start_floor': 6, 'destination_floor': 1},  # Passenger 5: Floor 6 -> Floor 1
    {'start_floor': 2, 'destination_floor': 8},  # Passenger 6: Floor 2 -> Floor 8
    {'start_floor': 5, 'destination_floor': 3},  # Passenger 7: Floor 5 -> Floor 3
    {'start_floor': 7, 'destination_floor': 4},  # Passenger 8: Floor 7 -> Floor 4
    {'start_floor': 9, 'destination_floor': 6},  # Passenger 9: Floor 9 -> Floor 6
    {'start_floor': 0, 'destination_floor': 10}  # Passenger 10: Floor 0 -> Floor 10
]

# Constants for simulation
TIME_BETWEEN_FLOORS = 2  # Time taken to travel between floors (in seconds)
TIME_TO_EXIT = 4         # Time taken for passengers to exit the lift (in seconds)

# Test LOOK algorithm
print("Testing LOOK algorithm...")
look_system = LOOK(total_floors_and_capacity, requests, TIME_BETWEEN_FLOORS, TIME_TO_EXIT)
look_time = look_system.run()
print(f"LOOK Algorithm: Total time elapsed = {look_time} seconds\n")

# Test SCAN algorithm
print("Testing SCAN algorithm...")
scan_system = SCAN(total_floors_and_capacity, requests, TIME_BETWEEN_FLOORS, TIME_TO_EXIT)
scan_time = scan_system.run()
print(f"SCAN Algorithm: Total time elapsed = {scan_time} seconds\n")