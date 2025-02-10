from request import Request
from Lift import Lift
class priority_queue:
    def __init__(self):
        self.Active_Queue=[]
        self.Waiting_Queue=[]
        self.MinHeap_Queue=[]
        self.MaxHeap_Queue=[]
        
    def loading_Request_into_Active_Waiting(self,request):#function loading request into priority queues (Active and waiting to limit the people get on the queue) 
        if len(self.Active_Queue) < Lift.capasity:#check if the active queue is equal to capasity limit or not if not full continue
            if len(self.Active_Queue) == 0:
                self.direction(Request.request_direction(request))

            else:
                if Request.request_direction(request) == self.direction:#if they are going the direction add them into the active 
                    if self.direction == "positive":
                        if Lift.current_floor > request[0]:
                            self.Waiting_Queue.append(request)

                        elif Lift.current_floor <= request[0]:
                            self.Active_Queue.append(request)

                    elif self.direction == "negative":
                        if Lift.current_floor < request[0]:
                            self.Waiting_Queue.append(request)

                        elif Lift.current_floor >= request[0]:
                            self.Active_Queue.append(request)

                else:
                    self.Waiting_Queue.append(request)#elseif they are going opposite put them in waiting 

        elif len(self.Active_Queue) == Lift.capasity:#else if the active queue is full put them in waiting 
            self.Waiting_Queue.append(request)

    def direction(the_direction):#set direction for lift 
        return the_direction
    
    def Loading_Waiting_to_Active(self):#function loading waitingQueue to activeQueue 
        if len(self.Active_Queue) < Lift.capasity:#check if the active queue is equal to capacity limit if not
            for i in range(len(self.Waiting_Queue)):#loop through every single request in waiting 
                if len(self.Active_Queue) == Lift.capasity:
                    break

                elif len(self.Active_Queue) == 0:
                    self.direction(Request.request_direction(self.Waiting_Queue[i]))

                else:
                    if Request.request_direction(self.Waiting_Queue[i]) == self.direction:#if they are going the direction add them into the active 
                        if self.direction == "positive":#if they are going positive direction
                            if Lift.current_floor <= self.Waiting_Queue[i][0]:#be sure that the lift didn't already past that floor
                                self.Active_Queue.append(self.Waiting_Queue[i])
                                del self.Waiting_Queue[i]# and delete it from waiting queue

                        elif self.direction == "negative":#if they are going negative direction
                            if Lift.current_floor >= self.Waiting_Queue[i][0]:#be usre that the lift didn't already past that floor
                                self.Active_Queue.append(self.Waiting_Queue[i][0]) 
                                del self.Waiting_Queue[i]# and delete it from waiting queue

    def MinHeap(self):#Function Minheap(ActiveQueue)
        if self.direction=="positive":# if direction positive in all requests in lift continue
            for i in range(len(self.Active_Queue)):#Loop the all elements(requests) in active Queue
                for j in range(len(self.Active_Queue[i])):
                    self.MinHeap_Queue.append(self.Active_Queue[i][j])#Then take the both elements of requests and store it in list

        def sorting_bubble_MinHeap():
            for i in range(len(self.MinHeap_Queue)):#sort the order by bubble sort meaning get every element and compare it with every element in list
                #loop through each element
                if self.MinHeap_Queue[i] > self.MinHeap_Queue[i+1]:#if element[n] > element[n+1]
                    value_i=self.MinHeap_Queue[i]#store value of element[n] in the place element[n+1]
                    value_ii=self.MaxHeap_Queue[i+1]
                    self.MinHeap_Queue[i]=value_ii
                    self.MinHeap_Queue[i+1]=value_i
                    return sorting_bubble_MinHeap(self,self.MinHeap_Queue)#call function sorting bubble

                elif self.MinHeap_Queue[i] == self.MinHeap_Queue[i+1]:#else if element[n] == element[n+1]
                    del self.MinHeap_Queue[i+1]#get rid of one n+1 by moving every request at the left move one right by using "del list[n+1]

    def MaxHeap(self):#Function Maxheap(ActiveQueue)
        if self.direction == "negative":# if direction negative in all requests in lift continue
            for i in range(len(self.Active_Queue)):#Loop the all elements(requests) in active Queue
                for j in range(len(self.Active_Queue[i])):
                    self.MaxHeap_Queue.append(self.Active_Queue[i][j])#Then take the both elements of requests and store it in list

        def sorting_bubble_MaxHeap():
            for i in range(len(self.MaxHeap_Queue)):#sort the order by bubble sort meaning get every element and compare it with every element in list
                #loop through each element
                if self.MaxHeap_Queue[i] < self.MaxHeap_Queue[i+1]:#if element[n] < element[n+1]
                    value_i=self.MaxHeap_Queue[i]#store value of element[n] in the place element[n+1]
                    value_ii=self.MaxHeap_Queue[i+1]
                    self.MaxHeap_Queue[i]=value_ii
                    self.MaxHeap_Queue[i+1]=value_i
                    return sorting_bubble_MaxHeap(self,self.MaxHeap_Queue)#call function sorting bubble

                elif self.MaxHeap_Queue[i] == self.MaxHeap_Queue[i+1]:#elseif element[n] == element[n+1]
                    del self.MaxHeap_Queue[i+1]#get rid of one n+1 by moving every request at the left move one right by using "del list[n+1]

    def Removing_requests_from_Active_and_MaxMinHeap(self):#function removing element from queues(Active Queue,Queue(an input of Max or MinHeap))
        if len(self.MinHeap_Queue) > 0:#if there is requests in MinHeap Queue
            #for i in range(len(self.MinHeap_Queue)):#loop through each elements in MinHeap U CAN DELETE THIS SINCE IT WILL ALWAYS IN FIRST ELEMENT IN MINHEAPQUEUE
            if Lift.current_floor == self.MinHeap_Queue[0]:#if current.place.lift is same with an floor on MinHeap
                del self.MinHeap_Queue[0]#remove it from MinHeap Queue

                for j in range(len(self.Active_Queue)):#Loop(j) the requests at ActiveQueue 
                    if self.Active_Queue[j] == ["VISITED","VISITED"]:#if ActiveQueue[j] (a request) is [VISITED,VISITED]
                        del self.Active_Queue[j]#that person is not in elevator so we can remove it from the Active Queue
                    for k in range(len(self.Active_Queue[j])):#loop (k) the elements in requests
                        if self.Active_Queue[j][k] == Lift.current_floor:#if a request element is equal to current place of the lift
                           self.Active_Queue[j][k] == "VISITED"# that person is in elevator and elevator been in their floor so put VISITED in the place request[j]



