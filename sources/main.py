# Import each algorithm
from SCAN import SCAN
from LOOK import LOOK
from MYLIFT import MYLIFT

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

    # Get total floors, capacity, and requests
    total_floors_and_capacity = check_floors_and_capacity(input_file_path, dataset_index=0)
    requests = validate_requests(input_file_path, dataset_index=0)

    # Run the algorithms
    scan_time = SCAN(total_floors_and_capacity, requests, TIME_TAKEN_FOR_LIFT_TO_TRAVEL_BETWEEN_FLOORS, TIME_TAKEN_FOR_PEOPLE_TO_EXIT_LIFT)
    look_time = LOOK(total_floors_and_capacity, requests, TIME_TAKEN_FOR_LIFT_TO_TRAVEL_BETWEEN_FLOORS, TIME_TAKEN_FOR_PEOPLE_TO_EXIT_LIFT)
    mylift_time = MYLIFT(total_floors_and_capacity, requests, TIME_TAKEN_FOR_LIFT_TO_TRAVEL_BETWEEN_FLOORS, TIME_TAKEN_FOR_PEOPLE_TO_EXIT_LIFT)

    return scan_time, look_time, mylift_time


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
        scan_time, look_time, mylift_time = run_simulation(file_path)
        results[f"input{i}"] = {
            "SCAN": scan_time,
            "LOOK": look_time,
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
