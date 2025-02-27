from Request import Request
from Lift import Lift
class PriorityQueue_LOOK:
    def __init__(self, lift_instance: Lift):
        self.lift = lift_instance
        self.Active_Queue: list[Request] = [] 
        self.Waiting_Queue: list[Request]= []
        self.MinHeap_Queue=[]
        self.MaxHeap_Queue=[]
        
    
    def loading_Request_into_Active_Waiting(self, request: Request):
        request_dir = request.request_direction()

        if len(self.Active_Queue) < self.lift.capacity:
            if not self.Active_Queue:
                # First request sets the lift direction
                self.lift.lift_direction = request_dir
                self.Active_Queue.append(request)
                print(f" First request sets direction. Added {request.start_floor}->{request.destination_floor} to Active Queue")
            else:
                # Only add to Active Queue if request moves in the **same** direction as the lift
                if request_dir == self.lift.lift_direction:
                    # Ensure request is in logical order with the lift's movement
                    if (self.lift.lift_direction == "positive" and request.start_floor >= self.lift.current_floor and request.destination_floor > request.start_floor) or \
                   (self.lift.lift_direction == "negative" and request.start_floor <= self.lift.current_floor and request.destination_floor < request.start_floor):
                        self.Active_Queue.append(request)
                        print(f" Added {request.start_floor}->{request.destination_floor} to Active Queue")
                    else:
                        self.Waiting_Queue.append(request)
                        print(f"⏳ Added {request.start_floor}->{request.destination_floor} to Waiting Queue (not in logical order)")
                else:
                    # If request moves in **opposite direction**, always put it in waiting queue
                    self.Waiting_Queue.append(request)
                    print(f"⏳ Added {request.start_floor}->{request.destination_floor} to Waiting Queue (opposite direction)")
        else:
            # If Active Queue is full, move to Waiting Queue
            self.Waiting_Queue.append(request)
            print(f"⏳ Active Queue full. Added {request.start_floor}->{request.destination_floor} to Waiting Queue")


    
    def Loading_Waiting_to_Active(self):
        if len(self.Active_Queue) == 0 and self.Waiting_Queue:
            # Determine new direction based on the first waiting request
            self.Waiting_Queue.sort(key=lambda r: r.start_floor, reverse=self.lift.lift_direction == "negative")

            # Take all requests moving in the correct direction
            moving_requests = [req for req in self.Waiting_Queue if req.request_direction() == self.lift.lift_direction]
        
            if moving_requests:
                # Set lift direction based on the first request
                self.lift.lift_direction = moving_requests[0].request_direction()

                # Move all matching requests to Active Queue
                
                for request in moving_requests:
                    if len(self.Active_Queue) < self.lift.capacity:
                        self.Active_Queue.append(request)
                        self.Waiting_Queue.remove(request)
                        print(f"✅ Moved {request.start_floor}->{request.destination_floor} from Waiting Queue to Active Queue")
            
                # Update heaps accordingly
                if self.lift.lift_direction == "positive":
                    self.MinHeap()
                else:
                    self.MaxHeap()

    def MinHeap(self):  # Function MinHeap(ActiveQueue)
        if self.lift.lift_direction == "positive":
        # Include both start and destination floors
            self.MinHeap_Queue = sorted(
            {req.start_floor for req in self.Active_Queue} |  # Start floors
            {req.destination_floor for req in self.Active_Queue}  # Destination floors
        )


    def MaxHeap(self):  # Function Maxheap(ActiveQueue)
        if self.lift.lift_direction == "negative":
        # Include both start and destination floors
            self.MaxHeap_Queue = sorted(
            {req.start_floor for req in self.Active_Queue} |  # Start floors
            {req.destination_floor for req in self.Active_Queue},  # Destination floors
            reverse=True
        )


            
    def Removing_requests_from_Active_and_MaxMinHeap(self):
        # Remove completed requests from Active Queue
        completed_requests = [req for req in self.Active_Queue if req.destination_floor == self.lift.current_floor]
        for request in completed_requests:
            self.Active_Queue.remove(request)
            print(f"✅ Request {request.start_floor}->{request.destination_floor} completed. Removed from Active Queue.")

        # Update time_elapsed for passenger exit
        self.lift.time_elapsed += len(completed_requests) * self.lift.exit_time

        # Rebuild MinHeap or MaxHeap based on direction
        if self.lift.lift_direction == "positive":
            self.MinHeap_Queue = sorted({req.start_floor for req in self.Active_Queue} | {req.destination_floor for req in self.Active_Queue})
        else:
            self.MaxHeap_Queue = sorted({req.start_floor for req in self.Active_Queue} | {req.destination_floor for req in self.Active_Queue}, reverse=True)

        # Only change direction if there are no more requests in the current direction
        if self.lift.lift_direction == "positive" and not self.MinHeap_Queue:
            print("🔄 Changing direction as no more requests in upward direction.")
            self.lift.lift_direction = "negative"
            self.Loading_Waiting_to_Active()
            self.MaxHeap()

        elif self.lift.lift_direction == "negative" and not self.MaxHeap_Queue:
            print("🔄 Changing direction as no more requests in downward direction.")
            self.lift.lift_direction = "positive"
            self.Loading_Waiting_to_Active()
            self.MinHeap()

        print(f"📌 Updated MinHeap Queue: {self.MinHeap_Queue}")
        print(f"📌 Updated MaxHeap Queue: {self.MaxHeap_Queue}")