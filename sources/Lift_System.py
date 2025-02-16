from priority_queue import priorityQueue
from Lift import Lift
from request import Request
class Lift_System:
    def __init__(self, total_floors):
        self.total_floors = total_floors
        self.Lift=Lift()
        self.priority_queue = priorityQueue(self.Lift)
        
       

    #Picks up passengers based on priority and available space
    def pick_up_passengers(self, request:Request):
        print(f"Adding request: {request.start_floor} -> {request.destination_floor}")  # Debugging
        self.priority_queue.loading_Request_into_Active_Waiting(request)
        self.priority_queue.Loading_Waiting_to_Active()

        # Print the queue to see if requests are being added
        print(f"Active Queue: {[f'{req.start_floor}->{req.destination_floor}' for req in self.priority_queue.Active_Queue]}")
        print(f"Waiting Queue: {[f'{req.start_floor}->{req.destination_floor}' for req in self.priority_queue.Waiting_Queue]}")


    def request_move_lift(self):
        print("🚀 Starting to process requests...")

        while self.priority_queue.Active_Queue or self.priority_queue.Waiting_Queue:
            print(f"Active Queue: {[f'{req.start_floor}->{req.destination_floor}' for req in self.priority_queue.Active_Queue]}")

            if not self.priority_queue.MinHeap_Queue and not self.priority_queue.MaxHeap_Queue:
                print("🔄 Changing direction as no more requests in current direction")
            
            # ✅ If there are requests in the Waiting Queue, move them to Active
                if self.priority_queue.Waiting_Queue:
                    self.priority_queue.Loading_Waiting_to_Active()
                    self.Lift.lift_direction = self.priority_queue.Active_Queue[0].request_direction()
                
                # ✅ Ensure heaps are updated correctly after switching direction
                    if self.Lift.lift_direction == "positive":
                        self.priority_queue.MinHeap()
                    else:
                        self.priority_queue.MaxHeap()
                
                    print(f"Lift direction set to: {self.Lift.lift_direction}")
                else:
                    print("No more requests to process. Exiting...")
                    return  # ✅ Exit if no requests left

        # 🚀 Update MinHeap or MaxHeap
            if self.Lift.lift_direction == "positive":
                self.priority_queue.MinHeap()
                next_stop = min([floor for floor in self.priority_queue.MinHeap_Queue if floor > self.Lift.current_floor], default=None)
            else:
                self.priority_queue.MaxHeap()
                next_stop = max([floor for floor in self.priority_queue.MaxHeap_Queue if floor < self.Lift.current_floor], default=None)

            if next_stop is None:
                print("No valid next stop. Exiting...")
                return

        # 🚀 Move the lift
            print(f"🚀 Lift moving to floor {next_stop}...")
            self.Lift.current_floor = next_stop
            print(f"Before Removing: MinHeap Queue: {self.priority_queue.MinHeap_Queue}")
            print(f"Before Removing: MaxHeap Queue: {self.priority_queue.MaxHeap_Queue}")

            self.priority_queue.Removing_requests_from_Active_and_MaxMinHeap()  # ✅ Remove requests & update heaps
            print(f"After Removing: MinHeap Queue: {self.priority_queue.MinHeap_Queue}")
            print(f"After Removing: MaxHeap Queue: {self.priority_queue.MaxHeap_Queue}")

        # ✅ Reload from Waiting Queue if Active Queue is empty
            if not self.priority_queue.Active_Queue and self.priority_queue.Waiting_Queue:
                self.priority_queue.Loading_Waiting_to_Active()



    def add_request(self, request:Request):
        # Handles new requests dynamically.
        if request.request_direction() is None:
            print(f"Invalid request: Start floor {request.start_floor} == Destination floor {request.destination_floor}")
            return
        self.pick_up_passengers(request)  # Add request to queue

if __name__ == "__main__":
    # Create lift system
    lift_system = Lift_System(total_floors=10)

    # Add test requests
    request1 = Request(1, 5)  # Moving up
    request2 = Request(3, 7)  # Moving up
    request3 = Request(8, 2)  # Moving down
    request4 = Request(4, 9)  # Moving up
    request5 = Request(6, 1)  # Moving down

    # Add requests to the system
    lift_system.add_request(request1)
    lift_system.add_request(request2)
    lift_system.add_request(request3)
    lift_system.add_request(request4)
    lift_system.add_request(request5)

    # Start moving the lift
    print("\n Starting Lift System Execution...\n")
    lift_system.request_move_lift()
