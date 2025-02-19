# This is how the main simulation may work

# Import each algorithm
from SCAN import SCAN
from LOOK import LOOK
from MYLIFT import MYLIFT

"""The parameters being passed are: the input file, time taken for the lift to travel between floors, and the time
taken for people to exit the lift at a particular floor. Each of these variables that the values of the functions
are passed to will represent an integer (in seconds), and these integers can be used to plot graphs that show
the time it takes for each algorithm to complete all of the requests in the input file, as well as compare the
performance visually between each of the algorithms."""

SCAN1 = SCAN("../results/data/input1.json", 2, 4)
LOOK1 = LOOK("../results/data/input1.json", 2, 4)
MYLIFT1 = MYLIFT("../results/data/input1.json", 2, 4)

SCAN2 = SCAN("../results/data/input2.json", 2, 4)
LOOK2 = LOOK("../results/data/input2.json", 2, 4)
MYLIFT2 = MYLIFT("../results/data/input2.json", 2, 4)

SCAN3 = SCAN("../results/data/input3.json", 2, 4)
LOOK3 = LOOK("../results/data/input3.json", 2, 4)
MYLIFT3 = MYLIFT("../results/data/input3.json", 2, 4)