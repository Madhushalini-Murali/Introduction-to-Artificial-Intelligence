import csv
import time
import sys

class Node:

    def __init__(self, name:str, parent:str):
        self.name = name
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.name == other.name

    def __lt__(self, other):
         return self.f < other.f

    def __repr__(self):
        return ('({0},{1})'.format(self.position, self.f))
        
#defining the graph class 
class Graph:
    # initializing graph states
    def __init__(self, graph_dict=None, directed=True):
        self.graph_dict = graph_dict or {}

    def join(self, a1, b1, distance):
        self.graph_dict.setdefault(a1, {})[b1] = distance

    def get(self, a2, b2=None):
        links = self.graph_dict.setdefault(a2, {})
        if b2 is None:
            return links
        else:
            return links.get(b2)

    def nodes(self):
        s1 = set([a3 for a3 in self.graph_dict.keys()])
        return list(s1)

def main():
    length = len(sys.argv)
    
    # check for 2 parameters i.e source and goal
    if length<3 or length>3:
        print("ERROR: Not enough or too many input arguments.")
        return
    initial_node = sys.argv[1]
    goal_node = sys.argv[2]
    graph = Graph()
    
    # to construct the US states graph from driving.csv data file
    with open('driving.csv') as driving_data:
        block_b1 = csv.reader(driving_data)
        nodes = next(block_b1)
        for row in block_b1:
            node = row[0]
            for i in range(1, len(row)):
                if int(row[i])>0:
                    graph.join(node, nodes[i], int(row[i]))           
    
    h = {}
    nodes = []
    
    # to construct heuristics graph from straightline.csv data file
    with open('straightline.csv') as straight_data:
        grid_g1 = csv.reader(straight_data)
        nodes = next(grid_g1)
        for row in grid_g1:
            node = row[0]
            if node==goal_node:
                for i in range(1, len(row)):
                    h[nodes[i]]= int(row[i])

    print("Murali, Madhushalini, A20513784 solution:")
    print("Initial state: ", initial_node)
    print("Goal state: ", goal_node) 
    
    # check for valid source and goal 
    if initial_node not in nodes or goal_node not in nodes:
        print("Solution path: FAILURE: NO PATH FOUND")
        print("Number of states on a path: 0")
        print("Path cost: N/A miles")
        print("Execution time: 0 seconds")
        return   

    greedy_Best_First_Search(graph, h, initial_node, goal_node) 
    A_Star(graph, h, nodes[1:], initial_node, goal_node)

#-------------------------------------------------------------------------------------
# Finding the shortest path using Greedy Best First alogorithm
# Traversing from initial node to goal node
def greedy_Best_First_Search(graph, heuristics_value, initial_node, goal_node):
    # starting time of the method 
    start_time = time.time()
    open = []
    closed = []
    initial_node = Node(initial_node, None)
    goal_node = Node(goal_node, None)
    open.append(initial_node)
    
    while len(open) > 0:
        open.sort()
        current_nodec1 = open.pop(0)
        closed.append(current_nodec1)
        
        adjacent_nodes = graph.get(current_nodec1.name)
        # to continue the search from the begining node
        for key, value in adjacent_nodes.items():
            adjacent_nodes = Node(key, current_nodec1)
            if(adjacent_nodes in closed):
                continue
            adjacent_nodes.g = current_nodec1.g + graph.get(current_nodec1.name, adjacent_nodes.name)
            adjacent_nodes.h = heuristics_value.get(adjacent_nodes.name)
            adjacent_nodes.f = adjacent_nodes.h
            if(isOpen(open, adjacent_nodes) == True):
                open.append(adjacent_nodes)

        # to stop the search once the goal state is reached    
        if current_nodec1 == goal_node:
            path_p = []
            cost_c = current_nodec1.g
            while current_nodec1 != initial_node:
                path_p.append(current_nodec1.name)
                current_nodec1 = current_nodec1.parent
            path_p.append(initial_node.name)
            path_p.reverse()
            
            # calculating end time 
            end_time = time.time()
            
            # calculating execution time 
            exce_time = end_time-start_time
            
            # printing the shortest path, number of states, path cost and execution time
            print("Greedy Best First Search:")
            print("Solution Path: ", ', '.join(path_p))
            print("Number of states on a path: ", len(path_p))
            print("Path cost: ", cost_c)
            print("Execution time: ", exce_time)        

#-----------------------------------------------------------------------------------------------------
# Finding the shortest path using A star alogorithm
# Traversing from initial node to goal node

def A_Star(graph, heuristics_value, states, initial_node, goal_node):
    # starting time of the method 
    start_time = time.time()
    
    # defining the distance,visited node,prior node and anchester nodes.
    distance_d1 = {}
    prior_nodep1 = {}
    visited_nodev1 = {}
    anchester_nodea1 = {}
    for state in states:
        distance_d1[state] = float("inf")
        prior_nodep1[state] = float("inf")
        visited_nodev1[state] = False
        anchester_nodea1[state] = None
    distance_d1[initial_node] = 0
    prior_nodep1[initial_node] = heuristics_value[initial_node]
    
    while True:
        la_prior = float("inf")
        la_prior_st = ""
        
        # to find least priority state
        for state in states:
            if prior_nodep1[state] < la_prior and not visited_nodev1[state]:
                la_prior = prior_nodep1[state]
                la_prior_st = state

        # to find adjacent states for least node
        for adjacent_node in graph.get(la_prior_st):
            if not visited_nodev1[adjacent_node]:
                if distance_d1[la_prior_st] + graph.get(la_prior_st, adjacent_node) < distance_d1[adjacent_node]:
                    distance_d1[adjacent_node] = distance_d1[la_prior_st] + graph.get(la_prior_st, adjacent_node)
                    prior_nodep1[adjacent_node] = distance_d1[adjacent_node] + heuristics_value[adjacent_node]
                    anchester_nodea1[adjacent_node] = la_prior_st
        visited_nodev1[la_prior_st] = True

        if la_prior_st == -1:
            return None

        # to stop the search once the goal state is reached
        elif la_prior_st == goal_node:
            cost_c = distance_d1[la_prior_st]
            path_p = []
            while la_prior_st!=initial_node:
                path_p.append(la_prior_st)
                la_prior_st = anchester_nodea1[la_prior_st]
            path_p.append(initial_node)
            path_p.reverse()
            # calculating end time 
            end_time = time.time()
            # calculating method execution time 
            exec_time = end_time-start_time
            # printing the shortest path, number of states, path cost and execution time
            print("A* Search:")
            print("Solution Path: ", ', '.join(path_p))
            print("Number of states on a path: ", len(path_p))
            print("Path cost: ", cost_c)
            print("Execution time: ", exec_time)
            return None


def isOpen(open, adjacent_node):
    for node in open:
        if (adjacent_node == node and adjacent_node.f >= node.f):
            return False
    return True



if __name__ == "__main__": main()