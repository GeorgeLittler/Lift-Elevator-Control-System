from priority_queue import priority_queue

class Lift:
    def __init__(self, total_floors, capacity):
        self.current_floor = 0
        self.capacity = capacity
        self.direction = 1 #1 is up, -1 is down
        self.total_floors = total_floors
        self.priority_queue = priority_queue()

    #Picks up passengers based on priority and available space
    def pick_up_passengers(self, request):
        self.priority_queue.loading_Request_into_Active_Waiting(request)  #Add request to the queue
        self.priority_queue.Loading_Waiting_to_Active() #Move passengers from waiting to active if there is space


    #Moves the lift based on requests in the active queue
    def move_lift(self):
        while self.priority_queue.Active_Queue:
            if self.direction == 1:  #Moving up
                self.priority_queue.MinHeap()  #Sort requests in ascending order
            else:  #Moving down
                self.priority_queue.MaxHeap()  #Sort requests in descending order

            #Serve the next request
            if self.direction == 1:
                next_stop = self.priority_queue.MinHeap_Queue[0]
            else:
                next_stop = self.priority_queue.MaxHeap_Queue[0]

            print(f"Moving to floor {next_stop}...")

            self.current_floor = next_stop  #Update current floor
            self.priority_queue.Removing_requests_from_Active_and_MaxMinHeap()  #Remove served requests

            #If Active Queue is empty, check Waiting Queue
            if not self.priority_queue.Active_Queue:
                self.priority_queue.Loading_Waiting_to_Active()

                #Change direction if needed
                if not self.priority_queue.Active_Queue and self.priority_queue.Waiting_Queue:
                    self.direction *= -1

            print(f"Lift currently at floor {self.current_floor}")

    def add_request(self, request):
        """ Handles new requests dynamically. """
        self.pick_up_passengers(request)  # Add request to queue