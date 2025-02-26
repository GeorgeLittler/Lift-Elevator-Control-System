# Import each algorithm
'''from SCAN import SCAN
from LOOK import LOOK'''
from MyLift import MyLift

from Request import Request

# Import helper functions - the first returns total floors and capacity, and the second returns the request data
from check_floors_and_capacity import check_floors_and_capacity
from validate_requests import validate_requests


def run_simulation(input_file_path):
    """
    Runs each of the 3 algorithms on the given input file and returns the time it took to complete all requests.
    """
    # Defines constants used in each algorithm
    TIME_TAKEN_FOR_LIFT_TO_TRAVEL_BETWEEN_FLOORS = 2
    TIME_TAKEN_FOR_PEOPLE_TO_EXIT_LIFT = 4

    # Load data
    total_floors, max_capacity= check_floors_and_capacity(input_file_path, dataset_index=0)  # (floors, capacity)
    requests_data = validate_requests(input_file_path, dataset_index=0)  # List of requests

    # Convert requests to Request objects for MyLift
    requests = []
    for start_floor, destination_floors in requests_data.items():
        for destination_floor in destination_floors:
            requests.append(Request(start_floor, destination_floor))

    # Run SCAN and LOOK algorithms
    '''scan_time = SCAN(total_floors, max_capacity, requests_data, TIME_TAKEN_FOR_LIFT_TO_TRAVEL_BETWEEN_FLOORS, TIME_TAKEN_FOR_PEOPLE_TO_EXIT_LIFT)
    look_time = LOOK(total_floors, max_capacity, requests_data, TIME_TAKEN_FOR_LIFT_TO_TRAVEL_BETWEEN_FLOORS, TIME_TAKEN_FOR_PEOPLE_TO_EXIT_LIFT)
    '''

    # Run MyLift algorithm
    mylift = MyLift(total_floors, max_capacity, TIME_TAKEN_FOR_LIFT_TO_TRAVEL_BETWEEN_FLOORS, TIME_TAKEN_FOR_PEOPLE_TO_EXIT_LIFT)
    
    for request in requests:
        mylift.add_request(request)  # Add each request to MyLift's queue

    mylift_time = mylift.run()

    return mylift_time


def main():
    # List containing each of the input file paths
    input_files = [
        "../results/data/input1.json",
        "../results/data/input2.json",
        "../results/data/input3.json"
    ]

    # Define results dictionary which will hold times for each algorithm for each input file
    results = {}

    for i, file_path in enumerate(input_files, start=1):
        mylift_time = run_simulation(file_path)
        results[f"input{i}"] = {
            "MYLIFT": mylift_time
        }

    # Print results
    for input_file, times in results.items():
        print(f"\nResults for {input_file}:")
        for algorithm, time in times.items():
            print(f"  {algorithm}: {time} seconds")

    return results


if __name__ == "__main__":
    main()
