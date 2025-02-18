import json
from check_floors_and_capacity import check_floors_and_capacity

def validate_requests(json_filename, dataset_index=0):
    # Use function to get total floors
    total_floors, _ = check_floors_and_capacity(json_filename, dataset_index)

    with open(json_filename, "r") as f:
        data = json.load(f)

    # Extract requests for the dataset
    requests_data = data[dataset_index]["requests"]
    
    valid_requests = {}

    # Loop over requests
    for floor in requests_data:
        current_floor = int(floor)  # Convert floor number to integer
        requests = []  # Create an empty list for converted requests

        # Convert request strings to integers using a loop
        for req in requests_data[floor]:
            requests.append(int(req))

        updated_requests = []  # Create an empty list for updated requests

        # Ensure all requests are within valid floor range using a loop
        for request in requests:
            if request < 1:
                updated_requests.append(1)
            elif request > total_floors:
                updated_requests.append(total_floors)
            else:
                updated_requests.append(request)

        valid_requests[current_floor] = updated_requests

    return valid_requests

# Example usage:
requests = validate_requests("../results/data/input1.json", dataset_index=0)
print(requests)
