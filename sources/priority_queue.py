#function loading request into priority queues (Active and waiting to limit the people get on the queue)
#check if the active queue is equal to capasity limit or not if not full continue
    #if they are going the direction add them into the active 
    #elseif they are going opposite put them in waiting 
#else if the active queue is full put them in waiting 


#function loading waitingQueue to activeQueue 
#check if the active queue is equal to capasity limit if not
    #ADDING SOMETHING
    #load the element[0] of the waiting queue to the active queue element[n] 
    # and delete it from waiting queue  

#Function Minheap(ActiveQueue)
# if direction positive in all requests in lift continue
    #Loop the all elements(requests) in active Queue
        #Then take the both elements of requests and store it in list
    #return that list and put it in sortingBubble function 
    #function sorting bubble_for minheap(the list)
    #sort the order by bubble sort meaning get every element and compare it with every element in list
        #loop through each element 
            #if element[n] > element[n+1]
                #store value of element[n] in the place element[n+1]
                #call function sorting bubble
            #elseif element[n] == element[n+1]
                #get rid of one n+1 by moving every request at the left move one right
                #by using "del list[n+1]
            #else don't do anything(don't add this line)
    #return the MinHeap queue
#else return Error

#Function Maxheap(ActiveQueue)
# if direction negative in all requests in lift continue
    #Loop the all elements(requests) in active Queue
        #Then take the both element of requests and store it in list
    #return that list and put it in sortingBubble function 
    #function sorting bubble_for maxheap(the list)
    #sort the order by bubble sort meaning get every element and compare it with every element in list
        #loop through each element 
            #if element[n] < element[n+1]
                #store value of element[n] in the place element[n+1]
                #call function sorting bubble
            #elseif element[n] == element[n+1]
                #get rid of one n+1 by moving every request at the left move one right
                #by using "del list[n+1]
            #else don't do anything(don't add this line)
    #return the MaxHeap queue
#else return Error


#function removing element from queues(Active Queue,Queue(an input of Max or MinHeap))
    #loop i the number of elements in Queue(Min/Heap)
        #if current.place.lift==Queue[i]
            #del Queue[i]
            #Loop(k) the requests at ActiveQueue 
                #if ActiveQueue[k] (a request) is [VISITED,VISITED]
                    #del ActiveQueue[k]
                #loop (j) the elements in request
                    #if request[j]==current.place.lift
                        #then put VISITED in the place request[j] 


