import csv

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