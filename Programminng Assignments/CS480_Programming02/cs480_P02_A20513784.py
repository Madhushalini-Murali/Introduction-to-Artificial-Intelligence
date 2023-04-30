import csv
import sys
from collections import defaultdict


class GivenValue:
    """
    This class is used to implement the utility functions required to read the data from the provided input files that  
    that includes the reading graph data ,reading park data and zones data
    """
    def __init__(self) -> None:
        self.parks = self.read_parks_data()
        self.graph= self.read_graph_data()
        self.zones = self.read_zones_data()
        self.map_city_zone = self.map_city_zone_data()

     # to read graphs
    def read_graph_data(self) -> dict:
        num_rows = []
        g_graph = defaultdict(list)
        with open("driving2.csv", 'r') as file:
            csvreader = csv.reader(file)
            for row_1 in csvreader:
                num_rows.append(row_1)
        for i in range(1, len(num_rows)):
            for j in range(1, len(num_rows[0])):
                value = int(num_rows[i][j])
                if(value != -1):
                    g_graph[num_rows[i][0]].append([num_rows[0][j], value])
        return g_graph
    
    def map_city_zone_data(self) -> dict:
        return self.read_data("zones.csv")    
        
    # to read zones    
    def read_zones_data(self) -> dict:
        num_rows = []
        z_zones = defaultdict(list)
        with open("zones.csv", 'r') as file:
            csvreader = csv.reader(file)
            for row_1 in csvreader:
                num_rows.append(row_1)
        for i in range(1, len(num_rows[0])):
            z_zones[int(num_rows[1][i])].append(num_rows[0][i])
        return z_zones
        
    # to read parks     
    def read_parks_data(self) -> dict:
        return self.read_data("parks.csv")    

    def read_data(self, arg0):
        num_rows = []
        with open(arg0, 'r') as file:
            csvreader = csv.reader(file)
            for row_1 in csvreader:
                num_rows.append(row_1)
        return {num_rows[0][i]: int(num_rows[1][i]) for i in range(1, len(num_rows[0]))}


class Back_Tracking:
    """
    This class is used to implement a Backtracking search (algorithm) to find a solution to a CSP Problem.
    """
    def __init__(self, parks_data, zones_data, graph_data, map_citi_zone_data, initial_state, min_num_of_parks) -> None:
        self.parks = parks_data
        self.zones = zones_data
        self.graph= graph_data
        self.map_citi_zone = map_citi_zone_data
        self.initial = initial_state
        self.min_parks = min_num_of_parks

    def search_backtracking(self):
        a_assgn = {self.map_citi_zone[self.initial]: self.initial}
        return self.backtracking(a_assgn, 0, self.parks[self.initial])

    # function to start the Backtracker given a problem and an assignment
    def backtracking(self, a_assgn, c_cost, no_of_parks):
        if a_assgn.get(12) is not None and no_of_parks >= self.min_parks:
            return [a_assgn, c_cost, no_of_parks]
        # To get a variable that is not assigned
        a1 = self.not_assigned_var(a_assgn)
        # The assignment that satisfies all the constraints or is null 
        for c_city in self.zones[a1]:
            #creating inference
            if self.ret_inference(a_assgn, a1, c_city):
                a_assgn[a1] = c_city
                r_result = self.backtracking(a_assgn, c_cost + self.read_cost(
                    self.graph[a_assgn[a1-1]], c_city), no_of_parks + self.parks[c_city])
                if r_result is not None:
                    return r_result
                a_assgn.pop(a1, None)
        return None

    # Return inferences
    def ret_inference(self, a_assgn, a1, c_city):
        return any(item[0] == c_city for item in self.graph[a_assgn[a1 - 1]])
       
    # Returns an assigned variable to try to assign.
    def not_assigned_var(self, a_assgn):
        z_zones = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        z_zones = z_zones[::-1]
        for zone1 in z_zones:
            if a_assgn.get(zone1) is not None:
                return zone1 + 1
        return None
        
    def read_cost(self, list, c_city):
        for item in list:
            if item[0] == c_city:
                return item[1]
        return -1
    
    
if __name__ == '__main__':
    length = len(sys.argv)
    # to print an error message if the input parameters is not two (none, one, or more than two)
    if( length != 3):
        print("ERROR: Not enough or too many input arguments.")
        sys.exit(1)
    # to read input parameters/values
    initial_state = sys.argv[1]
    min_num_parks = int(sys.argv[2])
    print("Murali, Madhushalini , A20513784 solution:")
    print("Initial state: "+initial_state)
    print("Minimum no of parks: "+str(min_num_parks))
    value1 = GivenValue()
    try:
        # to implement backtracking for a given city and parks by taking data from the given input files zones.csv, drivings2.csv and parks.csv
        bt_algorithm = Back_Tracking(value1.parks, value1.zones, value1.graph, value1.map_city_zone, initial_state, min_num_parks)
        r_result = bt_algorithm.search_backtracking()
    except:
        r_result = None
    # to retrieve the path nodes from the result object  
    req_path = ",".join(r_result[0].values()) if r_result is not None else "FAILURE: NO PATH FOUND"
    # count number of states in the required path   
    no_of_states = str(len(req_path.split(","))) if r_result is not None else "0"
    # to retrieve cost from the result object  
    c_cost = str(r_result[1]) if r_result is not None else "0"
    # to retrieve number of parks from result object  
    parks = str(r_result[2]) if r_result is not None else "0"
    print("Solution path: "+req_path)
    print("No of states on a path: "+no_of_states)
    print("Path cost: "+c_cost)
    print("Number of national parks visited: "+parks)
