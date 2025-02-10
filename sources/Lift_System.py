from priority_queue import priority_queue
from Lift import Lift
from request import Request
class Lift_System:
    def __init__(self, total_floors):
        self.total_floors = total_floors
        self.priority_queue = priority_queue()
       

    #Picks up passengers based on priority and available space
    def pick_up_passengers(self, request):
        self.priority_queue.loading_Request_into_Active_Waiting(request)  #Add request to the queue
        self.priority_queue.Loading_Waiting_to_Active() #Move passengers from waiting to active if there is space


    #Moves the lift based on requests in the active queue
    def request_move_lift(self):
        while self.priority_queue.Active_Queue:
            if self.priority_queue.direction == "positive":  #Moving up
                self.priority_queue.MinHeap()  #Sort requests in ascending order
            else:  #Moving down
                self.priority_queue.MaxHeap()  #Sort requests in descending order

            #Serve the next request
            if self.priority_queue.direction == "positive":
                next_stop = self.priority_queue.MinHeap_Queue[0]
            else:
                next_stop = self.priority_queue.MaxHeap_Queue[0]

            print(f"Moving to floor {next_stop}...")

            Lift.current_floor = next_stop  #Update current floor
            self.priority_queue.Removing_requests_from_Active_and_MaxMinHeap()  #Remove served requests

            #If Active Queue is empty, check Waiting Queue
            if not self.priority_queue.Active_Queue:
                self.priority_queue.Loading_Waiting_to_Active()

                #Change direction if needed
                if not self.priority_queue.Active_Queue and self.priority_queue.Waiting_Queue:
                    self.direction ="negative"

            print(f"Lift currently at floor {Lift.current_floor}")

    def add_request(self, request:Request):
        # Handles new requests dynamically.
        self.pick_up_passengers(request)  # Add request to queue

request1=Request(1,2)
lifo=Lift_System(8)
priority_queue()
Lift()
lifo.add_request(request1)
