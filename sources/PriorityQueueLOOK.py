from Request import Request
from Lift import Lift
from BasePriorityQueue import BasePriorityQueue

class PriorityQueueLOOK(BasePriorityQueue):
    def __init__(self, lift_instance: Lift):
        super().__init__(lift_instance)  #initialising the base class
        self.just_started = False#flag to check if the lift just started

    def Removing_requests_from_Active_and_MaxMinHeap(self):
        #removes completed requests from active queue and updates heaps
        completed_requests = [req for req in self.Active_Queue if req.destination_floor == self.lift.current_floor]
        for request in completed_requests:
            self.Active_Queue.remove(request)
            print(f"Request {request.start_floor}->{request.destination_floor} completed. Removed from Active Queue.")

        #update time elapsed based on completed requests
        self.lift.time_elapsed += len(completed_requests) * self.lift.enter_exit_time

        #update min or max heap based on lift direction
        if self.lift.lift_direction == "positive":
            self.MinHeap_Queue = sorted({req.start_floor for req in self.Active_Queue} | {req.destination_floor for req in self.Active_Queue})
        else:
            self.MaxHeap_Queue = sorted({req.start_floor for req in self.Active_Queue} | {req.destination_floor for req in self.Active_Queue}, reverse=True)
        
        #change lift direction if no more requests in current direction
        if self.lift.lift_direction == "positive" and not self.MinHeap_Queue:
            print("Changing direction to downward as no more requests in upward direction.")
            self.lift.lift_direction = "negative"
            self.just_started = True
            self.Loading_Waiting_to_Active()
            self.MaxHeap()
        elif self.lift.lift_direction == "negative" and not self.MaxHeap_Queue:
            print("Changing direction to upward as no more requests in downward direction.")
            self.lift.lift_direction = "positive"
            self.just_started = True
            self.Loading_Waiting_to_Active()
            self.MinHeap()

        #stop lift if no more requests are left
        if not self.Active_Queue and not self.Waiting_Queue and not self.MinHeap_Queue and not self.MaxHeap_Queue:
            print("No more requests left. Lift stopping.")
            




