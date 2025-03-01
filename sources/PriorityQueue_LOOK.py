from Request import Request
from Lift import Lift
from Request import Request
from Lift import Lift

class PriorityQueue_LOOK:
    def __init__(self, lift_instance: Lift):
        #initialises the priority queue with a lift instance and empty queues
        self.lift = lift_instance
        self.Active_Queue: list[Request] = []#holds requests currently being processed
        self.Waiting_Queue: list[Request] = []#holds requests waiting to be processed
        self.MinHeap_Queue = []#used for sorting floors in ascending order
        self.MaxHeap_Queue = []#used for sorting floors in descending order
        self.just_started = False#flag to check if the lift just started

    def loading_Request_into_Active_Waiting(self, request: Request):
        #loads a request into either the active or waiting queue based on conditions
        request_dir = request.request_direction()

        if len(self.Active_Queue) < self.lift.capacity:
            if not self.Active_Queue:
                #if active queue is empty, set lift direction and add the request
                self.lift.lift_direction = request_dir
                self.Active_Queue.append(request)
                print(f"First request sets direction. Added {request.start_floor}->{request.destination_floor} to Active Queue")
            else:
                if request_dir == self.lift.lift_direction:
                     #if request direction matches lift direction, check logical order
                    if (self.lift.lift_direction == "positive" and request.start_floor >= self.lift.current_floor and request.destination_floor > request.start_floor) or \
                       (self.lift.lift_direction == "negative" and request.start_floor <= self.lift.current_floor and request.destination_floor < request.start_floor):
                        self.Active_Queue.append(request)
                        print(f"Added {request.start_floor}->{request.destination_floor} to Active Queue")
                    else:
                         #if not in logical order, add to waiting queue
                        self.Waiting_Queue.append(request)
                        print(f"Added {request.start_floor}->{request.destination_floor} to Waiting Queue (not in logical order)")
                else:
                    #if request direction is opposite, add to waiting queue
                    self.Waiting_Queue.append(request)
                    print(f"Added {request.start_floor}->{request.destination_floor} to Waiting Queue (opposite direction)")
        else:
            #if active queue is full, add to waiting queue
            self.Waiting_Queue.append(request)
            print(f"Active Queue full. Added {request.start_floor}->{request.destination_floor} to Waiting Queue")

    def Loading_Waiting_to_Active(self):
        #moves requests from waiting queue to active queue if active queue is empty
        if not self.Active_Queue and self.Waiting_Queue:
            #sort waiting queue based on lift direction
            self.Waiting_Queue.sort(key=lambda r: r.start_floor, reverse=self.lift.lift_direction == "negative")
            moving_requests = [req for req in self.Waiting_Queue if req.request_direction() == self.lift.lift_direction]

            if moving_requests:
                #set lift direction and move requests to active queue
                self.lift.lift_direction = moving_requests[0].request_direction()
                for request in moving_requests[:self.lift.capacity]:
                    self.Active_Queue.append(request)
                    self.Waiting_Queue.remove(request)
                    print(f"Moved {request.start_floor}->{request.destination_floor} from Waiting Queue to Active Queue")

                #update min or max heap based on lift direction
                if self.lift.lift_direction == "positive":
                    self.MinHeap()
                else:
                    self.MaxHeap()

    def MinHeap(self):
        #sorts floors in ascending order for the min heap
        self.MinHeap_Queue = sorted({req.start_floor for req in self.Active_Queue} | {req.destination_floor for req in self.Active_Queue})

    def MaxHeap(self):
        #sorts floors in descending order for the max heap
        self.MaxHeap_Queue = sorted({req.start_floor for req in self.Active_Queue} | {req.destination_floor for req in self.Active_Queue}, reverse=True)

    def Removing_requests_from_Active_and_MaxMinHeap(self):
        #removes completed requests from active queue and updates heaps
        completed_requests = [req for req in self.Active_Queue if req.destination_floor == self.lift.current_floor]
        for request in completed_requests:
            self.Active_Queue.remove(request)
            print(f"Request {request.start_floor}->{request.destination_floor} completed. Removed from Active Queue.")

        #update time elapsed based on completed requests
        self.lift.time_elapsed += len(completed_requests) * self.lift.exit_time

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
            


