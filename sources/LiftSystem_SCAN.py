from LiftSystem_LOOK import LiftSystem_LOOK
from Request import Request
from PriorityQueue_SCAN import PriorityQueue_SCAN
class LiftSystem_SCAN(LiftSystem_LOOK):
    def __init__(self, total_floors):
        super().__init__(total_floors)  # Initialize the base class
        self.priority_queue = PriorityQueue_SCAN(self.Lift)  # Use the SCAN-specific priority queue


    def request_move_lift(self):
        print("🚀 Starting to process requests using SCAN algorithm...")

        while self.priority_queue.Active_Queue or self.priority_queue.Waiting_Queue:
            print(f"Active Queue: {[f'{req.start_floor}->{req.destination_floor}' for req in self.priority_queue.Active_Queue]}")
                    
            if self.Lift.lift_direction == "positive":
                self.priority_queue.MinHeap()
                next_stop = self.priority_queue.get_next_stop()
            else:
                self.priority_queue.MaxHeap()
                next_stop = self.priority_queue.get_next_stop()

            if next_stop is None:
                print("No more requests. Lift is idle.")
                break

            print(f"Next stop: {next_stop}")

            
            if not self.priority_queue.Active_Queue:
                if self.Lift.lift_direction=="positive":
                    if not self.priority_queue.MinHeap_Queue:
                        next_stop=self.priority_queue.check_direction_change()
                        print(f"🚀 Lift moving to floor {next_stop}...")
                        self.Lift.current_floor =next_stop
                        if self.Lift.current_floor==self.priority_queue.total_floors:
                            print("🔄 Reached top floor. Changing direction to downward.")
                            self.Lift.lift_direction = "negative"
                            self.priority_queue.Loading_Waiting_to_Active()
                elif self.Lift.lift_direction=="negative":
                    if not self.priority_queue.MaxHeap_Queue:
                        next_stop=self.priority_queue.check_direction_change()
                        print(f"🚀 Lift moving to floor {next_stop}...")
                        self.Lift.current_floor =next_stop
                        if self.Lift.current_floor==0:
                            print("🔄 Reached bottom floor. Changing direction to upward.")
                            self.Lift.lift_direction = "positive"
                            self.priority_queue.Loading_Waiting_to_Active()

            else:
                print(f"🚀 Lift moving to floor {next_stop}...")
                self.Lift.current_floor = next_stop
                print(f"Before Removing: MinHeap Queue: {self.priority_queue.MinHeap_Queue}")
                print(f"Before Removing: MaxHeap Queue: {self.priority_queue.MaxHeap_Queue}")

                self.priority_queue.Removing_requests_from_Active_and_MaxMinHeap()  # ✅ Remove requests & update heaps
                print(f"After Removing: MinHeap Queue: {self.priority_queue.MinHeap_Queue}")
                print(f"After Removing: MaxHeap Queue: {self.priority_queue.MaxHeap_Queue}")


            # Update the queues after moving
            self.priority_queue.update_queues()

            # Check if the lift needs to change direction
            self.priority_queue.check_direction_change()

            # Reload from Waiting Queue if Active Queue is empty
            
            if not self.priority_queue.Active_Queue and self.priority_queue.Waiting_Queue:
                next_stop=self.priority_queue.check_direction_change()
                print(f"🚀 Lift moving to floor {next_stop}...")
                self.Lift.current_floor =next_stop
                if self.Lift.current_floor==self.priority_queue.total_floors:
                    print("🔄 Reached top floor. Changing direction to downward.")
                    self.Lift.lift_direction = "negative"
                    self.priority_queue.Loading_Waiting_to_Active()
                elif self.Lift.current_floor==0:
                    print("🔄 Reached bottom floor. Changing direction to upward.")
                    self.Lift.lift_direction = "positive"
                    self.priority_queue.Loading_Waiting_to_Active()
                    
if __name__ == "__main__":
    # Create lift system
    lift_system = LiftSystem_SCAN(total_floors=10)

    # Add test requests
    request1 = Request(1, 5)  # Moving up
    request2 = Request(3, 7)  # Moving up
    request3 = Request(8, 2)  # Moving down
    request4 = Request(4, 7)  # Moving up
    request5 = Request(6, 1)  # Moving down

    # Add requests to the system
    lift_system.add_request(request1)
    lift_system.add_request(request2)
    lift_system.add_request(request3)
    lift_system.add_request(request4)
    lift_system.add_request(request5)

    # Start moving the lift
    print("\n Starting Lift System Execution using SCAN algorithm...\n")
    lift_system.request_move_lift()