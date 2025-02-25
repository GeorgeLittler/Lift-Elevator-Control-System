from PriorityQueue_LOOK import PriorityQueue_LOOK
from Lift import Lift
from Request import Request

class PriorityQueue_SCAN(PriorityQueue_LOOK):
    def __init__(self, lift_instance: Lift):
        super().__init__(lift_instance)  # Initialize the base class
        self.total_floors = 10  # Total floors in the building (can be passed as a parameter if needed)

    def get_next_stop(self):
        if self.lift.lift_direction == "positive":
            # Ensure the lift moves to the top floor before switching direction
            if self.Active_Queue or self.MinHeap_Queue:
                next_stop = min([floor for floor in self.MinHeap_Queue if floor > self.lift.current_floor], default=None)
                if next_stop is not None:
                    return next_stop
        # If no more requests in the current direction, move to the top floor before switching
            if self.lift.current_floor < self.total_floors:
                return self.total_floors

        else:
            # Ensure the lift moves to the bottom before switching direction
            if self.Active_Queue or self.MaxHeap_Queue:
                next_stop = max([floor for floor in self.MaxHeap_Queue if floor < self.lift.current_floor], default=None)
                if next_stop is not None:
                    return next_stop
            # If no more requests in the current direction, move to floor 0 before switching
            if self.lift.current_floor > 0:
                return 0

        return None  # No more stops
    
    def Removing_requests_from_Active_and_MaxMinHeap(self):
    
        # ✅ Remove all occurrences of the current floor from MinHeap and MaxHeap
        self.MinHeap_Queue = [floor for floor in self.MinHeap_Queue if floor != self.lift.current_floor]
        self.MaxHeap_Queue = [floor for floor in self.MaxHeap_Queue if floor != self.lift.current_floor]

        # ✅ Remove completed requests from Active Queue
        completed_requests = [req for req in self.Active_Queue if req.destination_floor == self.lift.current_floor]

        for request in completed_requests:
            self.Active_Queue.remove(request)
            print(f"✅ Request {request.start_floor}->{request.destination_floor} completed. Removed from Active Queue.")

        # ✅ Rebuild MinHeap and MaxHeap after modification
        if self.lift.lift_direction == "positive":
            self.MinHeap_Queue = sorted(
            {req.start_floor for req in self.Active_Queue} | {req.destination_floor for req in self.Active_Queue}
            )
        elif self.lift.lift_direction == "negative":
            self.MaxHeap_Queue = sorted(
            {req.start_floor for req in self.Active_Queue} | {req.destination_floor for req in self.Active_Queue},
            reverse=True
        )

        # ✅ Ensure direction only changes after reaching the highest or lowest floor
        if self.lift.lift_direction == "positive":
            if not self.MinHeap_Queue and not self.Active_Queue and self.lift.current_floor == self.total_floors:
                print("🔄 Reached top floor. Changing direction to downward.")
                self.lift.lift_direction = "negative"
                self.Loading_Waiting_to_Active()

        elif self.lift.lift_direction == "negative":
            if not self.MaxHeap_Queue and not self.Active_Queue and self.lift.current_floor == 0:
                print("🔄 Reached bottom floor. Changing direction to upward.")
                self.lift.lift_direction = "positive"
                self.Loading_Waiting_to_Active()

        # ✅ Debugging output to verify the heap is fully updated
        print(f"📌 Updated MinHeap Queue: {self.MinHeap_Queue}")
        print(f"📌 Updated MaxHeap Queue: {self.MaxHeap_Queue}")

    def update_queues(self):
        """Update the queues after the lift moves to a new floor."""
        if self.lift.lift_direction == "positive":
            # Remove all requests served at the current floor from MinHeap_Queue
            self.MinHeap_Queue = [floor for floor in self.MinHeap_Queue if floor != self.lift.current_floor]
            # Remove all requests served at the current floor from Active_Queue
            self.Active_Queue = [req for req in self.Active_Queue if req.destination_floor != self.lift.current_floor]
        else:
            # Remove all requests served at the current floor from MaxHeap_Queue
            self.MaxHeap_Queue = [floor for floor in self.MaxHeap_Queue if floor != self.lift.current_floor]
            # Remove all requests served at the current floor from Active_Queue
            self.Active_Queue = [req for req in self.Active_Queue if req.destination_floor != self.lift.current_floor]

    def check_direction_change(self):
        """Check if the lift needs to change direction (only at the top or bottom floor)."""
        if not self.Active_Queue:
            if self.lift.lift_direction== "positive":
                return self.total_floors

            elif self.lift.lift_direction=="negative":
                return 0
                
                