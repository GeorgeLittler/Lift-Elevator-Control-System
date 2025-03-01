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
    

    requests = []
    for start_floor, destination_floors in requests_data.items():
        for destination_floor in destination_floors:
            requests.append(Request(start_floor, destination_floor))

    #run the algorithms
    scan_time = SCAN(total_floors, max_capacity, requests_data, TIME_TAKEN_FOR_LIFT_TO_TRAVEL_BETWEEN_FLOORS, TIME_TAKEN_FOR_PEOPLE_TO_EXIT_LIFT).calculate_total_time()
    look_time = LOOK(total_floors, max_capacity, requests_data, TIME_TAKEN_FOR_LIFT_TO_TRAVEL_BETWEEN_FLOORS, TIME_TAKEN_FOR_PEOPLE_TO_EXIT_LIFT).calculate_total_time()
    
    mylift = MyLift(total_floors, max_capacity, TIME_TAKEN_FOR_LIFT_TO_TRAVEL_BETWEEN_FLOORS, TIME_TAKEN_FOR_PEOPLE_TO_EXIT_LIFT)
    
    for request in requests:
        mylift.add_request(request)  #add each request to MyLift's queue

    mylift_time = mylift.run()

    return scan_time, look_time, mylift_time


def write_performance_to_csv(results):#writes the performance results to CSV files and creates both individual input CSVs and the aggregate average CSV.
    algorithms = ["SCAN", "LOOK", "MYLIFT"]
    
    #gather individual input data
    for i, (input_file, times) in enumerate(results.items(), start=1):
        input_file_name = f"lift_performance_input{i}.csv"
        print(f"Writing to {input_file_name}")  #debugging print for file path
        with open(input_file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Algorithm", "Avg_Wait_Time", "Requests_Served", "Efficiency_Score"])
            for algorithm, time in times.items():
                #placeholder calculations for Avg_Wait_Time, Requests_Served, and Efficiency_Score
                avg_wait_time = time  #example placeholder; should be refined based on actual data
                requests_served = len(times)  #example placeholder; should be refined based on actual requests processed
                efficiency_score = requests_served / avg_wait_time  #example formula; should be refined
                writer.writerow([algorithm, avg_wait_time, requests_served, efficiency_score])

    #prepare aggregate/average data
    avg_wait_times = {algorithm: 0 for algorithm in algorithms}
    avg_requests_served = {algorithm: 0 for algorithm in algorithms}
    avg_efficiency_scores = {algorithm: 0 for algorithm in algorithms}
    
    num_files = len(results)
    
    #averages for each algorithm
    for times in results.values():
        for algorithm in algorithms:
            avg_wait_times[algorithm] += times[algorithm]  #placeholder, needs refinement
            avg_requests_served[algorithm] += len(times)  #placeholder, needs refinement
            avg_efficiency_scores[algorithm] += len(times) / times[algorithm]  #placeholder formula
    
    for algorithm in algorithms:
        avg_wait_times[algorithm] /= num_files
        avg_requests_served[algorithm] /= num_files
        avg_efficiency_scores[algorithm] /= num_files

    #average data to aggregate CSV
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
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

    #list containing each of the input file paths
    input_files = [
        os.path.join(BASE_DIR, "results/data/input1.json"),
        os.path.join(BASE_DIR, "results/data/input2.json"),
        os.path.join(BASE_DIR, "results/data/input3.json")
    ]

    #print resolved paths for debugging
    print("Resolved input file paths:")
    for file_path in input_files:
        print(file_path)

    #define results dictionary which will hold times for each algorithm for each input file
    results = {}

    for i, file_path in enumerate(input_files, start=1):
        scan_time, look_time, mylift_time = run_simulation(file_path)
        results[f"input{i}"] = {
            "SCAN": scan_time,
            "LOOK": look_time,
            "MYLIFT": mylift_time
        }

    #printing results
    for input_file, times in results.items():
        print(f"\nResults for {input_file}:")
        for algorithm, time in times.items():
            print(f"  {algorithm}: {time} seconds")


    #results to CSV files
    write_performance_to_csv(results)

    return results


if __name__ == "__main__":
    main()