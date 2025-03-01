import os
import csv

#import each algorithm
from LiftSystem_SCAN import SCAN
from LiftSystem_LOOK import LOOK
from MyLift import MyLift

from Request import Request

#import helper functions ,the first returns total floors and capacity, and the second returns the request data
from check_floors_and_capacity import check_floors_and_capacity
from validate_requests import validate_requests



def run_simulation(input_file_path):#runs each of the 3 algorithms on the given input file and returns the time it took to complete all requests.
    #defines constants used in each algorithm
    TIME_TAKEN_FOR_LIFT_TO_TRAVEL_BETWEEN_FLOORS = 2
    TIME_TAKEN_FOR_PEOPLE_TO_EXIT_LIFT = 4

    #load data
    total_floors, max_capacity= check_floors_and_capacity(input_file_path, dataset_index=0) #floors, capacity
    requests_data = validate_requests(input_file_path, dataset_index=0) #list of requests
    
    # new total requests
    total_requests = sum(len(destinations) for destinations in requests_data.values())
    
    requests = []
    for start_floor, destination_floors in requests_data.items():
        for destination_floor in destination_floors:
            requests.append(Request(start_floor, destination_floor))

    total_requests = len(requests)

    #run the algorithms
    scan_time = SCAN(total_floors, max_capacity, requests_data, TIME_TAKEN_FOR_LIFT_TO_TRAVEL_BETWEEN_FLOORS, TIME_TAKEN_FOR_PEOPLE_TO_EXIT_LIFT).calculate_total_time()
    look_time = LOOK(total_floors, max_capacity, requests_data, TIME_TAKEN_FOR_LIFT_TO_TRAVEL_BETWEEN_FLOORS, TIME_TAKEN_FOR_PEOPLE_TO_EXIT_LIFT).calculate_total_time()
    
    mylift = MyLift(total_floors, max_capacity, TIME_TAKEN_FOR_LIFT_TO_TRAVEL_BETWEEN_FLOORS, TIME_TAKEN_FOR_PEOPLE_TO_EXIT_LIFT)
    
    for request in requests:
<<<<<<< HEAD
        mylift.add_request(request)  #add each request to MyLift's queue
=======
        mylift.add_request(request)

    mylift.sort_requests()
>>>>>>> 6e22badd636515ca8f54fd0298044ddce9ff7e0e

    mylift_time = mylift.run()

    return scan_time, look_time, mylift_time, total_requests


def write_performance_to_csv(results):
    algorithms = ["SCAN", "LOOK", "MYLIFT"]

    # Write individual input results
    for i, (input_file, times) in enumerate(results.items(), start=1):
        input_file_name = f"lift_performance_input{i}.csv"
        print(f"Writing to {input_file_name}")
        with open(input_file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Algorithm", "Avg_Wait_Time", "Requests_Served", "Efficiency_Score"])
            
            for algorithm in algorithms:
                algorithm_data = times.get(algorithm, {})
                avg_wait_time = algorithm_data.get("time", 0)  # Extract time
                requests_served = algorithm_data.get("requests", 0)  # Extract requests

                if not isinstance(avg_wait_time, (int, float)):
                    avg_wait_time = 0  # Fallback for safety
                
                efficiency_score = requests_served / avg_wait_time if avg_wait_time > 0 else 0
                
                writer.writerow([algorithm, avg_wait_time, requests_served, efficiency_score])

    # Compute average results across inputs
    avg_wait_times = {algorithm: 0 for algorithm in algorithms}
    avg_requests_served = {algorithm: 0 for algorithm in algorithms}
    avg_efficiency_scores = {algorithm: 0 for algorithm in algorithms}
    
    num_files = len(results)

    # Compute total sums for averaging
    for times in results.values():
        for algorithm in algorithms:
            algorithm_data = times.get(algorithm, {})
            wait_time = algorithm_data.get("time", 0)
            requests = algorithm_data.get("requests", 0)

            if not isinstance(wait_time, (int, float)):
                wait_time = 0  
            
            avg_wait_times[algorithm] += wait_time
            avg_requests_served[algorithm] += requests
            avg_efficiency_scores[algorithm] += (requests / wait_time if wait_time > 0 else 0)

    # Compute actual averages
    for algorithm in algorithms:
        avg_wait_times[algorithm] /= num_files
        avg_requests_served[algorithm] /= num_files
        avg_efficiency_scores[algorithm] /= num_files

    # Write aggregate data to `lift_performance.csv`
    with open("lift_performance.csv", mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Algorithm", "Avg_Wait_Time", "Requests_Served", "Efficiency_Score"])
        for algorithm in algorithms:
            writer.writerow([
                algorithm, 
                avg_wait_times[algorithm], 
                avg_requests_served[algorithm], 
                avg_efficiency_scores[algorithm]
            ])
        
    print("CSV files have been created successfully.")



def main():
<<<<<<< HEAD
    #define the base directory which is project root
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
=======
    # Define the base directory (project root)
    project_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
>>>>>>> 6e22badd636515ca8f54fd0298044ddce9ff7e0e

    #list containing each of the input file paths
    input_files = [
        os.path.join(project_directory, "results/data/input1.json"),
        os.path.join(project_directory, "results/data/input2.json"),
        os.path.join(project_directory, "results/data/input3.json")
    ]

<<<<<<< HEAD
    #print resolved paths for debugging
    print("Resolved input file paths:")
    for file_path in input_files:
        print(file_path)

    #define results dictionary which will hold times for each algorithm for each input file
=======
    # Define results dictionary which will hold times for each algorithm for each input file
>>>>>>> 6e22badd636515ca8f54fd0298044ddce9ff7e0e
    results = {}

    for i, file_path in enumerate(input_files, start=1):
        scan_time, look_time, mylift_time, total_requests = run_simulation(file_path)
        results[f"input{i}"] = {
            "SCAN": {"time": scan_time, "requests": total_requests},
            "LOOK": {"time": look_time, "requests": total_requests},
            "MYLIFT": {"time": mylift_time, "requests": total_requests}
        }

    #printing results
    for input_file, times in results.items():
        print(f"\nResults for {input_file}:")
        for algorithm, data in times.items():
            print(f"  {algorithm}: {data['time']} seconds, Requests Served: {data['requests']}")


    #results to CSV files
    write_performance_to_csv(results)

    return results

if __name__ == "__main__":
    main()