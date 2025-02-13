from request import Request
from Lift import Lift
class priorityQueue:
    def __init__(self, lift_instance: Lift):
        self.lift = lift_instance
        self.Active_Queue: list[Request] = [] 
        self.Waiting_Queue: list[Request]= []
        self.MinHeap_Queue=[]
        self.MaxHeap_Queue=[]
        
    
    def loading_Request_into_Active_Waiting(self, request: Request):
        request_dir = request.request_direction()

        print(f"\n Checking request: {request.start_floor} -> {request.destination_floor} (Direction: {request_dir})")
        print(f" Lift direction: {self.lift.lift_direction} | Current floor: {self.lift.current_floor}")
        print(f"📋 Active Queue: {[f'{r.start_floor}->{r.destination_floor}' for r in self.Active_Queue]}")
        print(f"📋 Waiting Queue: {[f'{r.start_floor}->{r.destination_floor}' for r in self.Waiting_Queue]}")

        if len(self.Active_Queue) < self.lift.capacity:
            if len(self.Active_Queue) == 0:
            #  First request sets the lift direction
                self.lift.lift_direction = request_dir
                self.Active_Queue.append(request)
                print(f" First request sets direction. Added {request.start_floor}->{request.destination_floor} to Active Queue")
            else:
            #  Only add to Active Queue if request moves in the **same** direction as the lift
                if request_dir == self.lift.lift_direction:
                #  Ensure request is in logical order with the lift's movement
                    if (self.lift.lift_direction == "positive" and request.start_floor >= self.lift.current_floor and request.destination_floor > request.start_floor) or \
                   (self.lift.lift_direction == "negative" and request.start_floor <= self.lift.current_floor and request.destination_floor < request.start_floor):
                        self.Active_Queue.append(request)
                        print(f" Added {request.start_floor}->{request.destination_floor} to Active Queue")
                    else:
                        self.Waiting_Queue.append(request)
                        print(f"⏳ Added {request.start_floor}->{request.destination_floor} to Waiting Queue (not in logical order)")
                else:
                #  If request moves in **opposite direction**, always put it in waiting queue
                    self.Waiting_Queue.append(request)
                    print(f"⏳ Added {request.start_floor}->{request.destination_floor} to Waiting Queue (opposite direction)")
        else:
        # If Active Queue is full, move to Waiting Queue
            self.Waiting_Queue.append(request)
            print(f"⏳ Active Queue full. Added {request.start_floor}->{request.destination_floor} to Waiting Queue")




    def direction(self,the_direction):#set direction for lift 
        return the_direction
    
    def Loading_Waiting_to_Active(self):
    # ✅ Only load from waiting queue if Active Queue is completely empty
        if len(self.Active_Queue) == 0:
            for request in self.Waiting_Queue[:]:  # Loop through a copy of the list
                self.lift.lift_direction = request.request_direction()  # 🔥 Reset direction dynamically
            
            # ✅ Only move requests that match the new direction
                if (self.lift.lift_direction == "positive" and request.start_floor > self.lift.current_floor) or \
               (self.lift.lift_direction == "negative" and request.start_floor < self.lift.current_floor):
                    self.Active_Queue.append(request)
                    self.Waiting_Queue.remove(request)
                    print(f"✅ Moved {request.start_floor}->{request.destination_floor} from Waiting Queue to Active Queue")



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
        # ✅ Remove **all occurrences** of current floor from MinHeap and MaxHeap
        if self.lift.current_floor in self.MinHeap_Queue:
            self.MinHeap_Queue = [floor for floor in self.MinHeap_Queue if floor != self.lift.current_floor]
        if self.lift.current_floor in self.MaxHeap_Queue:
            self.MaxHeap_Queue = [floor for floor in self.MaxHeap_Queue if floor != self.lift.current_floor]

    # ✅ Remove completed requests from Active Queue
        completed_requests = [req for req in self.Active_Queue if req.destination_floor == self.lift.current_floor]

        for request in completed_requests:
            self.Active_Queue.remove(request)
            print(f"✅ Request {request.start_floor}->{request.destination_floor} completed. Removed from Active Queue.")

    # ✅ **Rebuild MinHeap after modification**
        if self.lift.lift_direction == "positive" and self.Active_Queue:
            remaining_start_floors = {req.start_floor for req in self.Active_Queue}
            remaining_dest_floors = {req.destination_floor for req in self.Active_Queue}
            self.MinHeap_Queue = sorted(remaining_start_floors | remaining_dest_floors)

    # ✅ **Only switch direction after MinHeap is fully empty**
        if self.lift.lift_direction == "positive" and not self.MinHeap_Queue and not self.Active_Queue:
            print("🔄 Changing direction as MinHeap is empty. Moving Waiting Queue to Active Queue.")
            self.Loading_Waiting_to_Active()

            if self.Active_Queue:
                self.lift.lift_direction = self.Active_Queue[0].request_direction()
                print(f"🚦 Lift direction switched to {self.lift.lift_direction}")

            # ✅ **Now build MaxHeap after direction switch**
                if self.lift.lift_direction == "negative":
                    remaining_start_floors = {req.start_floor for req in self.Active_Queue}
                    remaining_dest_floors = {req.destination_floor for req in self.Active_Queue}
                    self.MaxHeap_Queue = sorted(remaining_start_floors | remaining_dest_floors, reverse=True)

    # ✅ **Print MinHeap and MaxHeap only after modification**
        print(f"📌 Updated MinHeap Queue: {self.MinHeap_Queue}")
        print(f"📌 Updated MaxHeap Queue: {self.MaxHeap_Queue}")


