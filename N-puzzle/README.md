### N-Puzzle game
wikipage: https://heuristicswiki.wikispaces.com/N+-+Puzzle

Solved using:

1. BFS (Breadth First Search)
2. DFS (Depth First Search)
3. A*
4. IDA


The board argument will be a comma-separated list of integers containing no spaces. For
example, to use the bread-first search strategy to solve the input board given by the starting
configuration {0,8,7,6,5,4,3,2,1}, the program will be executed like so (with no spaces between
commas):
$ python driver.py bfs 0,8,7,6,5,4,3,2,1

When executed, your program will create / write to a file called output.txt, containing the
following statistics:
path_to_goal: the sequence of moves taken to reach the goal
cost_of_path: the number of moves taken to reach the goal
nodes_expanded: the number of nodes that have been expanded
fringe_size: the size of the frontier set when the goal node is found
max_fringe_size: the maximum size of the frontier set in the lifetime of the algorithm
search_depth: the depth within the search tree when the goal node is found
max_search_depth: the maximum depth of the search tree in the lifetime of the algorithm
running_time: the total running time of the search instance, reported in seconds
max_ram_usage: the maximum RAM usage in the lifetime of the process as measured by
the ru_maxrss attribute in the resource module, reported in megabytes
