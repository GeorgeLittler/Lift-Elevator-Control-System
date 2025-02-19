# This is how the main simulation may work

# Import each algorithm
from SCAN import SCAN
from LOOK import LOOK
from MYLIFT import MYLIFT

# Import helper functions - the first returns the total floors and capacity, and the second returns the requests data
from check_floors_and_capacity import check_floors_and_capacity
from validate_requests import validate_requests

# Defines constants to be used in each algorithm
TIME_TAKEN_FOR_LIFT_TO_TRAVEL_BETWEEN_FLOORS = 2
TIME_TAKEN_FOR_PEOPLE_TO_EXIT_LIFT = 4

'''
Below we are testing each of the 3 algorithms on each of the 3 input JSON files (subject to change). Each algorithm should return an
integer (in seconds), which represents how long it takes for the algorithm to complete every request. These
integers can then be used to compare and visualise the performance of each algorithm against the others by using
graphs/charts.
'''

# This is defining the filepath to the first input file
input1_file_path = "../results/data/input1.json"

SCAN1 = SCAN(check_floors_and_capacity(input1_file_path, dataset_index=0),
             validate_requests(input1_file_path, dataset_index=0),
             TIME_TAKEN_FOR_LIFT_TO_TRAVEL_BETWEEN_FLOORS, TIME_TAKEN_FOR_PEOPLE_TO_EXIT_LIFT)

LOOK1 = LOOK(check_floors_and_capacity(input1_file_path, dataset_index=0),
             validate_requests(input1_file_path, dataset_index=0),
             TIME_TAKEN_FOR_LIFT_TO_TRAVEL_BETWEEN_FLOORS, TIME_TAKEN_FOR_PEOPLE_TO_EXIT_LIFT)

MYLIFT1 = MYLIFT(check_floors_and_capacity(input1_file_path, dataset_index=0),
                validate_requests(input1_file_path, dataset_index=0),
                TIME_TAKEN_FOR_LIFT_TO_TRAVEL_BETWEEN_FLOORS, TIME_TAKEN_FOR_PEOPLE_TO_EXIT_LIFT)


input2_file_path = "../results/data/input2.json"

SCAN2 = SCAN(check_floors_and_capacity(input2_file_path, dataset_index=0),
             validate_requests(input2_file_path, dataset_index=0),
             TIME_TAKEN_FOR_LIFT_TO_TRAVEL_BETWEEN_FLOORS, TIME_TAKEN_FOR_PEOPLE_TO_EXIT_LIFT)

LOOK2 = LOOK(check_floors_and_capacity(input2_file_path, dataset_index=0),
             validate_requests(input2_file_path, dataset_index=0),
             TIME_TAKEN_FOR_LIFT_TO_TRAVEL_BETWEEN_FLOORS, TIME_TAKEN_FOR_PEOPLE_TO_EXIT_LIFT)

MYLIFT2 = MYLIFT(check_floors_and_capacity(input2_file_path, dataset_index=0),
                validate_requests(input2_file_path, dataset_index=0),
                TIME_TAKEN_FOR_LIFT_TO_TRAVEL_BETWEEN_FLOORS, TIME_TAKEN_FOR_PEOPLE_TO_EXIT_LIFT)


input3_file_path = "../results/data/input3.json"

SCAN3 = SCAN(check_floors_and_capacity(input3_file_path, dataset_index=0),
             validate_requests(input3_file_path, dataset_index=0),
             TIME_TAKEN_FOR_LIFT_TO_TRAVEL_BETWEEN_FLOORS, TIME_TAKEN_FOR_PEOPLE_TO_EXIT_LIFT)

LOOK3 = LOOK(check_floors_and_capacity(input3_file_path, dataset_index=0),
             validate_requests(input3_file_path, dataset_index=0),
             TIME_TAKEN_FOR_LIFT_TO_TRAVEL_BETWEEN_FLOORS, TIME_TAKEN_FOR_PEOPLE_TO_EXIT_LIFT)

MYLIFT3 = MYLIFT(check_floors_and_capacity(input3_file_path, dataset_index=0),
                validate_requests(input3_file_path, dataset_index=0),
                TIME_TAKEN_FOR_LIFT_TO_TRAVEL_BETWEEN_FLOORS, TIME_TAKEN_FOR_PEOPLE_TO_EXIT_LIFT)