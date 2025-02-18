import pandas as pd

# This function checks that total floors and capacity are set to reasonable numbers and updates them if not
def check_floors_and_capacity(csv_filename):
    df = pd.read_csv(csv_filename)
    
    # Total floors and capacity should be the first and second values in the first row
    try:
        total_floors, capacity = int(df.iloc[0, 0]), int(df.iloc[0, 1])
    except (IndexError, ValueError):
        raise ValueError("Error: The file doesn't have valid numerical values for total floors and capacity.")

    # Checks if total floors is between 5 and 40 and updates its value if not
    if total_floors < 5:
        total_floors = 5
        print(f"Total floors updated to: {total_floors}")
    elif total_floors > 40:
        total_floors = 40
        print(f"Total floors updated to: {total_floors}")
    
    # Checks if capacity is between 3 and 12 and updates its value if not
    if capacity < 3:
        capacity = 3
        print(f"Capacity updated to: {capacity}")
    elif capacity > 12:
        capacity = 12
        print(f"Capacity updated to: {capacity}")

    return total_floors, capacity
