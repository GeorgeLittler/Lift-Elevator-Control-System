class Lift1:
    def __init__(self, total_floors, max_capacity, travel_time=2, enter_exit_time=4):
        self.start_floor = 1
        self.current_floor = self.start_floor
        self.total_floors = total_floors
        self.start_capacity = 0
        self.current_capacity = self.start_capacity
        self.max_capacity = max_capacity
        self.available_capacity = self.max_capacity - self.current_capacity
        self.travel_time = travel_time
        self.enter_exit_time = enter_exit_time
        self.time_elapsed = 0
        self.direction = "positive"
        self.lift_direction = None
        self.visited_floors = set()  # Track visited floors

