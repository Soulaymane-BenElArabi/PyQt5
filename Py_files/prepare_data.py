from pandas import read_excel


def prepare_graph(filename):
    """This function reads the excel file and turn it to a dictionary """
    try:
        file = read_excel(filename)
        # file = pandas.read_excel(filename)
        # Create the  adjacency matrix from the excel file
        graph = []  # This list is going to contain the matrix
        graph.append(list(file.columns[1:]))  # We start appending to our list
        for i in range(len(list(file.columns[1:]))):
            graph.append(list(file.iloc[i, 1:]))
            
        # Create a dictionnary
        dictio = {}
        x = False
        for vertex in range(len(graph[0])):
            temp_dict = {}
            for weight_index in range(len(graph[vertex + 1])):
                if graph[vertex + 1][weight_index] != 0:
                    if graph[vertex + 1][weight_index] > 0:
                        temp_dict[graph[0][weight_index]] = graph[vertex + 1][weight_index]
                    else:
                        x = True
                        temp_dict[graph[0][weight_index]] = graph[vertex + 1][weight_index]

            dictio[graph[0][vertex]] = temp_dict
        vertices = graph[0]
        result = [dictio, vertices, x]
        return result
    except TypeError:
        return -1


def Dijkstra_algo(graph, from_v, to_v):
    """This function finds the shortest path using Dijkstra algorithm"""
    global min_val
    path = {}  # shortest distance between vertices
    adj_vertex = {}  # from it we will explore it's adjacent vertices
    queue = []  # Where we will append unvisited vertices and remove those that have been visited
    graph = graph
    # Initialize distances from the path
    for vertex in graph:
        path[vertex] = float("inf")  # all distances initialized to infintive
        adj_vertex[vertex] = None
        queue.append(vertex)
    path[from_v] = 0  # starting vertex's distance to 0

    while queue:
        # find min distance which wasn't marked as current
        key_min = queue[0]
        min_val = path[key_min]
        for i in range(1, len(queue)):
            if path[queue[i]] < min_val:
                key_min = queue[i]
                min_val = path[key_min]  # it will contain min distance to key_min in every iteration
        cur = key_min  # Current vertex
        queue.remove(cur)  # remove cur from queue because it was visited

        for i in graph[cur]:  # for adjacent vertices we search min distance from cur
            alternate = graph[cur][i] + path[cur]  # we calculate the distance
            if path[i] > alternate:  # if the path to adjacent vertex is smaller than path from cur
                path[i] = alternate  #
                adj_vertex[i] = cur

    # Now we will store the vertices of the shortest path in the  queue list
    # so we can colorize afterward
    x = to_v
    # the ascendant of the algorithm
    shortest = []
    shortest.append(x)
    while True:
        x = adj_vertex[x]
        if x is None:  # if we reach the initial vertex we stop appending to queue
            break
        shortest.append(x)
    shortest.reverse()  # We reverse the path so it will start from initial vertex to destination vertex
    dist_path = [shortest, min_val]
    return dist_path
