#!/usr/bin/python
# Chandra Shankaradithya Narain - uni --> ck2840
import sys
import queue
import math
import heapq
import resource
import time


# Getting data

method = str(sys.argv[1])
istate = str(sys.argv[2])
#method = 'ida'
#istate = '0,8,7,6,5,4,3,2,1'
#istate = '1,2,5,3,4,0,6,7,8'
seed   = istate.split(',')
size_n = len(seed)
rsize  = int(math.sqrt(size_n))
REMOVED = '<data-removed>'


#defining measures:
path_to_goal = 0
cost_to_goal = 0
nodes_expanded = 0
fringe_size = 0
max_fringe_size = 0
search_depth = 0
max_search_depth = 0
running_time = 0
max_ram_usage = 0


# defining goal object
goal = []
for x in range(0,size_n):
    goal.append(x)

goal = str(goal).strip("[]")

# Reformatting seed object
istate = []
for x in range(0,size_n):
    istate.append(int(seed[x]))
istate = str(istate).strip('[]')

    

# Function to convert string to list of integers
def StringToArray(state):
    a = state.split(',')
    barray = []

    for x in range(0,size_n):
        barray.append(int(a[x]))

    return barray

# Function to convert list of integers to string
def ArrayToString(inarray):
    a = str(inarray).strip('[]')
    return a

# Test function to check the goal
def GoalTest(state):
    #print("state"+state)
    #print("goal"+goal)
    if state == goal:
       return True
    else:
       return False 

# Moving Functions
def MoveUp(arr, pos):
    up = []
    # Check if it is valid move
    if pos <= rsize-1: 
       return str(up).strip('[]'), up
    up = arr[:]
    # swap positions
    new_pos = pos - rsize
    temp = up[new_pos]
    up[new_pos] = up[pos]
    up[pos] = temp
    return str(up).strip('[]'), up

def MoveDown(arr, pos):
    down = []
    # Check if it is valid move
    if pos > (size_n - rsize)-1:
       return str(down).strip('[]'), down
    down = arr[:]
    # swap positions
    new_pos = pos + rsize
    temp = down[new_pos]
    down[new_pos] = down[pos]
    down[pos] = temp
    return str(down).strip('[]'), down

def MoveLeft(arr, pos):
    left = []
    # Check if it is valid move
    if (((pos) % rsize) ==  0) or (pos == 0):
       return str(left).strip('[]'), left
    left = arr[:]
    # swap positions
    new_pos = pos - 1
    temp = left[new_pos]
    left[new_pos] = left[pos]
    left[pos] = temp
    return str(left).strip('[]'), left

def MoveRight(arr, pos):
    right = []
    # Check if it is valid move
    if ((pos+1) % rsize) == 0:
       return str(right).strip('[]'), right
    right = arr[:]
    # swap positions
    new_pos = pos + 1
    temp = right[new_pos]
    right[new_pos] = right[pos]
    right[pos] = temp
    return str(right).strip('[]'), right

# Generating neighbours
def Neighbours(state):
    arr = StringToArray(state)
    up = MoveUp(arr)
    down = MoveDown(arr)
    left = MoveLeft(arr)
    right = MoveRight(arr)
    neighbours = []
    if len(up) > 0: 
       neighbours.append(up)
    if len(down) > 0:
       neighbours.append(down)
    if len(left) > 0:
       neighbours.append(left)
    if len(right) > 0:
       neighbours.append(right)
    return neighbours

class Node():

    def __init__(self, parent, state, move):
        self.parent = parent
        self.state = state
        self.move  = move
        self.gcost = 0
        self.hcost = 0
        self.frontier = 0
        self.explored = 0
        self.entry = None
        self.depth = 0
        self.arr  = None

    
def bfs():

    #implementing breadth first search
   
    # creating frontier queue
    frontier = queue.Queue(maxsize=0)

    # creating dictionary  list
    rope = dict()

    # creating moves list
    move_list = []
 
    # Adding first node/state to the list
    parent = 0
    nnode = Node(None, istate, None)
    rope[istate] = nnode
    nnode.arr = StringToArray(istate)

    # adding initial state to python
    frontier.put(nnode)

    # default parameters
    global  cost_to_goal
    global  path_to_goal
    global  fringe_size
    global  max_fringe_size
    global  search_depth
    global  max_search_depth
    global  max_fringe_size
    global  nodes_expanded
    global  max_ram_usage

    # adding max_fringe_size:
    if (frontier.qsize() > max_fringe_size): max_fringe_size = frontier.qsize()

    # Checking if frontier is empty
    while (frontier.qsize() > 0):

        # Getting the state from frontier queue
        snode = frontier.get()
        state = snode.state

        # Testing if Goal is met
        if GoalTest(state):
           search_depth = snode.depth
           while( snode.parent is not None): 
               move_list.append(snode.move)
               snode = snode.parent

           fringe_size = frontier.qsize()
           cost_to_goal = len(move_list)
           move_list.reverse()
           path_to_goal = str(move_list)
           max_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

           return

        # Getting neighbours
        arr = snode.arr
        pos = arr.index(0)

        #nodes expanded
        nodes_expanded = nodes_expanded + 1

        for move in range(0,4):
            if move == 0:
               nstate,narr = MoveUp(arr, pos)
               move_name = 'Up'
            elif move == 1:
               nstate,narr = MoveDown(arr, pos)
               move_name = 'Down'
            elif move == 2:
               nstate,narr = MoveLeft(arr, pos)
               move_name = 'Left'
            else: 
               nstate,narr = MoveRight(arr, pos)
               move_name = 'Right'

            if (len(nstate) > 0) and (nstate not in rope):
                nnode = Node(snode, nstate, move_name)
                nnode.arr = narr
                rope[nstate] = nnode
                nnode.depth = snode.depth + 1
                frontier.put(nnode)
                #max fringe size
                if max_fringe_size < frontier.qsize(): max_fringe_size = frontier.qsize()
                #max search depth
                if max_search_depth < nnode.depth: max_search_depth = nnode.depth
        
    return

def dfs():

    #implementing depth first search

    from collections import deque 

    # creating frontier queue
    frontier = deque()

    # creating dictionary  list
    rope = dict()

    # creating moves list
    move_list = []
 
    # Adding first node/state to the list
    parent = 0
    nnode = Node(None, istate, None)
    nnode.state = istate
    nnode.arr   = StringToArray(istate)
    rope[istate] = nnode

    # default parameters
    global  cost_to_goal
    global  path_to_goal
    global  fringe_size
    global  max_fringe_size
    global  search_depth
    global  max_search_depth
    global  max_fringe_size
    global  nodes_expanded
    global  max_ram_usage

    # adding initial state to python
    frontier.append(nnode)
    nnode.frontier = 1
    nnode.explored = 0

    # adding max_fringe_size:
    if (len(frontier) > max_fringe_size): max_fringe_size = len(frontier)
   
    # Checking if frontier is empty
    while (len(frontier) > 0):

        # Getting the state from frontier queue
        snode = frontier.pop()
        snode.frontier = 0
        snode.explored = 1
        state = snode.state

        # Testing if Goal is met
        if GoalTest(state):
            search_depth = snode.depth
            while (snode.parent is not None):
                   move_list.append(snode.move)
                   snode = snode.parent

            fringe_size = len(frontier)
            cost_to_goal = len(move_list)
            move_list.reverse()
            path_to_goal = str(move_list)
            max_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

            return

        # Getting neighbours
        arr = snode.arr
        pos = arr.index(0)

        #nodes expanded
        nodes_expanded = nodes_expanded + 1

        for move in range(0,4):
            if move == 3:
               nstate, narr = MoveUp(arr, pos)
               move_name = 'Up'
            elif move == 2:
               nstate, narr = MoveDown(arr, pos)
               move_name = 'Down'
            elif move == 1:
               nstate, narr = MoveLeft(arr, pos)
               move_name = 'Left'
            else: 
               nstate, narr = MoveRight(arr, pos)
               move_name = 'Right'

            if (len(nstate) > 0) and (nstate not in rope):
                nnode = Node(snode, nstate, move_name)
                nnode.arr = narr
                frontier.append(nnode)
                rope[nstate] = nnode
                nnode.depth = snode.depth + 1
                # adding max_fringe_size:
                if (len(frontier) > max_fringe_size): max_fringe_size = len(frontier)
                #max search depth
                if max_search_depth < nnode.depth: max_search_depth = nnode.depth
        
    return

# calculate manhattan distance
def Manhattan(state):
    sum = 0
    arr = StringToArray(state)
    for i in range(0,size_n):
        if arr[i] == 0: continue
        xb = int((arr[i])/rsize)
        yb = ((arr[i])%rsize)
        xo = int((i)/rsize)
        yo = (i%rsize)
        sum = sum + abs(xb-xo) + abs(yb-yo)

    return sum
def ast():

    #implementing a star search

    # global count variable
    gcount = 0

    # creating frontier queue
    frontier = []

    # creating dictionary  list
    rope = dict()

    # creating moves list
    move_list = []
 
    # Adding first node/state to the list
    parent = 0
    nnode = Node(None, istate, None)
    nnode.entry = [0, gcount, istate]
    nnode.gcost = 0
    nnode.hcost = Manhattan(istate)
    rope[istate] = nnode
    nnode.arr = StringToArray(istate)

    # Adding to frontier
    heapq.heappush(frontier, nnode.entry)

    # Added to the frontier
    nnode.frontier = 1

    # default parameters
    global  cost_to_goal
    global  path_to_goal
    global  fringe_size
    global  max_fringe_size
    global  search_depth
    global  max_search_depth
    global  max_fringe_size
    global  nodes_expanded
    global  max_ram_usage

    # adding max_fringe_size:
    if (len(frontier) > max_fringe_size): max_fringe_size = len(frontier)

    # Checking if frontier is empty
    while (len(frontier) > 0):

        # Getting the state from frontier queue
        while len(frontier) > 0:
            priority, count, state = heapq.heappop(frontier)
            if state is not REMOVED:
                break

        # getting the nodal entry and updating values
        snode = rope[state]
        snode.frontier = 0
        snode.explored = 1

        # Testing if Goal is met
        if GoalTest(state):
            search_depth = snode.depth
            while (snode.parent is not None):
                move_list.append(snode.move)
                snode = snode.parent

            fringe_size = len(frontier)
            cost_to_goal = len(move_list)
            move_list.reverse()
            path_to_goal = str(move_list)
            max_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
           
            return

        # Getting neighbours
        arr = snode.arr
        pos = arr.index(0)

        #nodes expanded
        nodes_expanded = nodes_expanded + 1

        for move in range(0,4):
            if move == 3:
               nstate, narr = MoveUp(arr, pos)
               move_name = 'Up'
            elif move == 2:
               nstate, narr = MoveDown(arr, pos)
               move_name = 'Down'
            elif move == 1:
               nstate, narr = MoveLeft(arr, pos)
               move_name = 'Left'
            else: 
               nstate, narr = MoveRight(arr, pos)
               move_name = 'Right'

            if len(nstate) > 0:

                # new child insert into the frontier
                if nstate not in rope:
                    nnode = Node(snode, nstate, move_name)
                    rope[nstate] = nnode
                    nnode.frontier = 1
                    nnode.explored = 0
                    nnode.gcost = snode.gcost + 1
                    nnode.hcost = Manhattan(nstate)
                    gcount = gcount + 1
                    cost = nnode.gcost + nnode.hcost
                    nnode.entry = [cost, gcount, nstate]
                    nnode.depth = snode.depth + 1
                    nnode.arr = narr

                    # max search depth
                    if max_search_depth < nnode.depth: max_search_depth = nnode.depth

                    # adding entry to frontier
                    heapq.heappush(frontier, nnode.entry)

                    # adding max_fringe_size:
                    if (len(frontier) > max_fringe_size): max_fringe_size = len(frontier)

                # old one check if explored or not explored
                else:
                    nnode = rope[nstate]
                    if (nnode.explored is not 1) and (nnode.frontier is 1):
                        cost = snode.gcost + 1 + Manhattan(nstate)
                        if  cost < nnode.entry[0]:
                            nnode.entry[-1] = REMOVED
                            gcount = gcount + 1
                            nnode1 = Node(nnode.parent, nstate, nnode.move)
                            nnode1.frontier = 1
                            nnode1.explored = 0
                            nnode1.gcost = snode.gcost + 1
                            nnode1.hcost = cost - 1 - snode.gcost
                            nnode1.entry = [cost, gcount, nstate]
                            rope[nstate] = nnode1
                            nnode1.arr = nnode.arr
                            nnode1.depth = nnode.depth
                            # adding max_fringe_size:
                            if (len(frontier) > max_fringe_size): max_fringe_size = len(frontier)
                            # max search depth
                            if max_search_depth < nnode1.depth: max_search_depth = nnode1.depth
    return


def ida():
    from collections import deque

    # implementing a IDA star search

    found = 0

    #setting initial threshold

    threshold = Manhattan(istate)

    # keeping track of min threshold
    thresmin = threshold


    # default parameters
    global cost_to_goal
    global path_to_goal
    global fringe_size
    global max_fringe_size
    global search_depth
    global max_search_depth
    global max_fringe_size
    global nodes_expanded
    global max_ram_usage

    cost_to_goal = 0
    path_to_goal = 0
    fringe_size  = 0
    max_fringe_size = 0
    search_depth = 0
    max_search_depth = 0
    nodes_expanded = 0
    max_ram_usage = 0

    # iterative threshold loop
    while found is not 1:

        #Creating frontier queue
        frontier = deque()

        # creating dictionary
        rope = dict()

        # creating moves list
        move_list = []

        # Adding first node/state to the list
        nnode = Node(None, istate, None)
        nnode.gcost = 0
        nnode.hcost = Manhattan(istate)
        rope[istate] = nnode
        nnode.arr = StringToArray(istate)

        # Testing if Goal is met
        if GoalTest(istate):
            search_depth = nnode.depth
            while (nnode.parent is not None):
                move_list.append(nnode.move)
                nnode = nnode.parent

            fringe_size = len(frontier)
            cost_to_goal = len(move_list)
            move_list.reverse()
            path_to_goal = str(move_list)
            max_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            return

        # Adding to frontier
        frontier.append(nnode)
        # Added to the frontier
        nnode.frontier = 1

        # Getting the state from frontier queue
        while len(frontier) > 0:

            # adding max_fringe_size:
            if (len(frontier) > max_fringe_size): max_fringe_size = len(frontier)

            # getting the nodal entry and updating values
            snode = frontier.pop()
            snode.frontier = 0
            snode.explored = 1

            state = snode.state

            # Testing if Goal is met
            if GoalTest(state):
                search_depth = snode.depth
                while (snode.parent is not None):
                    move_list.append(snode.move)
                    snode = snode.parent

                fringe_size = len(frontier)
                cost_to_goal = len(move_list)
                move_list.reverse()
                path_to_goal = str(move_list)
                max_ram_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
                return


            # Getting neighbours
            arr = snode.arr
            pos = arr.index(0)

            # expanded nodes count
            nodes_expanded = nodes_expanded + 1

            for move in range(0, 4):
                if move == 3:
                    nstate, narr = MoveUp(arr, pos)
                    move_name = 'Up'
                elif move == 2:
                    nstate, narr = MoveDown(arr, pos)
                    move_name = 'Down'
                elif move == 1:
                    nstate, narr = MoveLeft(arr, pos)
                    move_name = 'Left'
                else:
                    nstate, narr = MoveRight(arr, pos)
                    move_name = 'Right'

                if len(nstate) > 0:

                    # calculate cost
                    cost = snode.gcost + 1 + Manhattan(nstate)

                    if cost <= threshold:
                        # new child insert into the frontier
                        add = False

                        if  nstate not in rope: add = True
                        else:
                            tnode = rope[nstate]
                            if (cost < (tnode.gcost + tnode.hcost)): add = True

                        if  add:
                            nnode = Node(snode, nstate, move_name)
                            nnode.frontier = 1
                            nnode.explored = 0
                            nnode.gcost = snode.gcost + 1
                            nnode.hcost = Manhattan(nstate)
                            nnode.arr = narr
                            rope[nstate] = nnode
                            nnode.depth = snode.depth + 1

                            # max search depth
                            if max_search_depth < nnode.depth: max_search_depth = nnode.depth

                            frontier.append(nnode)

                            # adding max_fringe_size:
                            if (len(frontier) > max_fringe_size): max_fringe_size = len(frontier)

        threshold = threshold+1
    return
mem_start = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
start = time.clock()
if   method == 'bfs': bfs()
elif method == 'dfs': dfs()
elif method == 'ast': ast()
elif method == 'ida': ida()
else: print('Invalid choice of algorithm entered '+method)
stop = time.clock()

running_time = stop - start
# Memory obtained is in bytes converting into MB
mem = (max_ram_usage)/1000000

# writing output file:
file = open("output.txt", "w")
file.write("path_to_goal: "+path_to_goal+'\n')
file.write("cost_of_path: "+str(cost_to_goal)+'\n')
file.write("nodes_expanded: "+str(nodes_expanded)+'\n')
file.write("fringe_size: "+str(fringe_size)+'\n')
file.write("max_fringe_size: "+str(max_fringe_size)+'\n')
file.write("search_depth: "+str(search_depth)+'\n')
file.write("max_search_depth: " +str(max_search_depth)+'\n')
file.write("running_time: "+str(running_time)+'\n')
file.write("max_ram_usage: "+str(mem)+'\n')
file.close()

