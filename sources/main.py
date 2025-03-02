import os
import csv

#import each algorithm
from LiftSystem_SCAN import SCAN
from LiftSystem_LOOK import LOOK
from MyLift import MyLift

from Request import Request

#import helper functions
from check_floors_and_capacity import check_floors_and_capacity
from validate_requests import validate_requests
from write_performance_to_csv import write_performance_to_csv

def run_simulation(input_file_path):
    # Define the time constants for lift operations
    TIME_TAKEN_FOR_LIFT_TO_TRAVEL_BETWEEN_FLOORS = 2
    TIME_TAKEN_FOR_PEOPLE_TO_EXIT_LIFT = 4

    # Extract building parameters from the input file
    total_floors, max_capacity = check_floors_and_capacity(input_file_path, dataset_index=0)
    requests_data = validate_requests(input_file_path, dataset_index=0)
    
    # Count the total number of requests in the dataset
    total_requests = sum(len(destinations) for destinations in requests_data.values())
    
    # Convert the request data into a list of Request objects
    requests = []
    for start_floor, destination_floors in requests_data.items():
        for destination_floor in destination_floors:
            requests.append(Request(start_floor, destination_floor))

    scan_time = SCAN(total_floors, max_capacity, requests_data, TIME_TAKEN_FOR_LIFT_TO_TRAVEL_BETWEEN_FLOORS, TIME_TAKEN_FOR_PEOPLE_TO_EXIT_LIFT).calculate_total_time()
    look_time = LOOK(total_floors, max_capacity, requests_data, TIME_TAKEN_FOR_LIFT_TO_TRAVEL_BETWEEN_FLOORS, TIME_TAKEN_FOR_PEOPLE_TO_EXIT_LIFT).calculate_total_time()
    
    #create and run MyLift simulation
    mylift = MyLift(total_floors, max_capacity, TIME_TAKEN_FOR_LIFT_TO_TRAVEL_BETWEEN_FLOORS, TIME_TAKEN_FOR_PEOPLE_TO_EXIT_LIFT)
    
    for request in requests:
        mylift.add_request(request)
    mylift.sort_requests()
    mylift_time = mylift.run()

    return scan_time, look_time, mylift_time, total_requests

def write_performance_to_csv(results):
    algorithms = ["SCAN", "LOOK", "MYLIFT"]

    #writes performance results for each input file
    for i, (input_file, times) in enumerate(results.items(), start=1):
        input_file_name = f"lift_performance_input{i}.csv"
        print(f"Writing to {input_file_name}")
        with open(input_file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Algorithm", "Avg_Wait_Time", "Requests_Served", "Efficiency_Score"])
            
            for algorithm in algorithms:
                algorithm_data = times.get(algorithm, {})
                avg_wait_time = algorithm_data.get("time", 0)  
                requests_served = algorithm_data.get("requests", 0)  

                if not isinstance(avg_wait_time, (int, float)):
                    avg_wait_time = 0  
                
                efficiency_score = requests_served / avg_wait_time if avg_wait_time > 0 else 0
                
                writer.writerow([algorithm, avg_wait_time, requests_served, efficiency_score])

    #overall averages across all input files
    avg_wait_times = {algorithm: 0 for algorithm in algorithms}
    avg_requests_served = {algorithm: 0 for algorithm in algorithms}
    avg_efficiency_scores = {algorithm: 0 for algorithm in algorithms}
    
    num_files = len(results)

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

    #final averages
    for algorithm in algorithms:
        avg_wait_times[algorithm] /= num_files
        avg_requests_served[algorithm] /= num_files
        avg_efficiency_scores[algorithm] /= num_files

    #write aggregate data to lift_performance.csv
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
    #define the base directory which is project root
    project_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    #define the paths to input data files
    input_files = [
        os.path.join(project_directory, "results/data/input1.json"),
        os.path.join(project_directory, "results/data/input2.json"),
        os.path.join(project_directory, "results/data/input3.json")
    ]

    results = {}

    #run simulations for each input file
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

    write_performance_to_csv(results)

    return results

if __name__ == "__main__":
    main()
