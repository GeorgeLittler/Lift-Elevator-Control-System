import json
import os

def check_floors_and_capacity(json_filename, dataset_index=0):
    """
    Checks that total floors and capacity are set to reasonable numbers and updates them if not.
    
    Args:
        json_filename (str): Path to the JSON file (relative or absolute).
        dataset_index (int): Index of the dataset to use (default: 0).
    
    Returns:
        tuple: (total_floors, capacity)
    
    Raises:
        FileNotFoundError: If the JSON file does not exist.
        ValueError: If the JSON file does not have valid numerical values for total floors and capacity.
    """
    # Resolve the relative path to an absolute path
    json_filename = os.path.abspath(json_filename)
    print(f"Resolved JSON file path: {json_filename}")  # Debugging

    try:
        # Open and load the JSON file
        with open(json_filename, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: JSON file not found at {json_filename}")

    # Get the specified dataset (default: first dataset)
    dataset = data[dataset_index]
    total_floors = dataset.get("total_floors")
    capacity = dataset.get("capacity")

    # Ensure total_floors and capacity are valid numbers
    if not isinstance(total_floors, int) or not isinstance(capacity, int):
        raise ValueError("Error: JSON file does not have valid numerical values for total floors and capacity.")

    # Ensure total floors is between 5 and 40
    if total_floors < 5:
        total_floors = 5
        print(f"Total floors updated to: {total_floors}")
    elif total_floors > 40:
        total_floors = 40
        print(f"Total floors updated to: {total_floors}")
    
    # Ensure capacity is between 3 and 12
    if capacity < 3:
        capacity = 3
        print(f"Capacity updated to: {capacity}")
    elif capacity > 12:
        capacity = 12
        print(f"Capacity updated to: {capacity}")

    return total_floors, capacity