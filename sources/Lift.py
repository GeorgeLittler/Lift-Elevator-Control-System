class Lift:
    def __init__(self, total_floors, max_capacity, travel_time=2, exit_time=4):
        self.start_floor = 1
        self.total_floors = total_floors
        self.start_capacity = 0
        self.max_capacity = max_capacity
        self.travel_time = travel_time
        self.exit_time = exit_time
        self.time_elapsed = 0
        self.direction = "UP"