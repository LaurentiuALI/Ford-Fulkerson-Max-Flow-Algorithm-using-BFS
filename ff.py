class Graph:

    def __init__(self, graph):
        self.graph = graph  # original graph
        self.residual_graph = [[cell for cell in row] for row in graph]  # cloned graph
        self.latest_augmenting_path = [[0 for cell in row] for row in graph]  # empty graph with same dimension as graph
        self.current_flow = [[0 for cell in row] for row in graph]  # empty graph with same dimension as graph

    def breadth(self, source, sink):
        visited = []
        queue = []
        prev = [None for x in range(len(self.graph))]

        visited.append(source)
        queue.append(source)

        while queue:
            s = queue.pop(0)
            for index, neighbour in enumerate(self.residual_graph[s]):
                if neighbour != 0 and index not in visited:
                    visited.append(index)
                    queue.append(index)
                    prev[index] = s

        path = [sink]
        curr = sink
        while prev[curr] is not None:
            path.append(prev[curr])
            curr = prev[curr]
        if len(path) == 1 and sink in path:
            return None

        return path

    def update_residual_graph(self):
        for row in range(len(self.residual_graph)):
            for column in range(len(self.residual_graph)):
                if self.latest_augmenting_path[row][column] >= 0:
                    self.residual_graph[row][column] = self.residual_graph[row][column] - self.latest_augmenting_path[row][column]
                elif self.latest_augmenting_path[row][column] < 0:
                    self.residual_graph[row][column] = self.residual_graph[row][column] - self.latest_augmenting_path[row][column]
                    self.residual_graph[column][row] = self.current_flow[row][column]

        for row in range(len(self.residual_graph)):
            for column in range(len(self.residual_graph)):
                if self.current_flow[row][column] != 0:
                    self.residual_graph[column][row] = self.current_flow[row][column]


    def find_min_in_path(self, path):
        mins = []
        for item in range(len(path)):
            if item < len(path)-1:
                mins.append(self.residual_graph[path[item+1]][path[item]])
        self.update_latest_augmenting_path(path, min(mins))
        self.update_current_flow(path, min(mins))
        self.update_residual_graph()
        if min(mins) > 0:
            return min(mins)
        return 0


    def update_latest_augmenting_path(self, path, mins):
        for item in range(len(path)):
            if item<len(path) - 1:
                if self.graph[ path[item+1] ][ path[item] ] > 0:
                    self.latest_augmenting_path[path[item+1]][path[item]] += mins
                elif self.graph[ path[item+1] ][ path[item] ] == 0:
                    self.latest_augmenting_path[path[item]][path[item+1]] -= mins


    def update_current_flow(self, path, mins):
        for item in range(len(path)):
            if item<len(path) - 1:
                if self.graph[ path[item+1] ][ path[item] ] > 0:
                    self.current_flow[path[item + 1]][path[item]] += mins
                elif self.graph[path[item + 1]][path[item]] == 0:
                    self.current_flow[path[item]][path[item + 1]] -= mins




    def ff_step(self, source, sink):
        """
        Perform a single flow augmenting iteration from source to sink
        Update the latest augmenting path, the residual graph and the current flow by the maximum possible amount according to your chosen path.
        The path must be chosen based on BFS.
        @param source the source's vertex id
        @param sink the sink's vertex id
        @return the amount by which the flow has increased.
        """
        self.latest_augmenting_path = [[0 for cell in row] for row in self.graph]


        path = self.breadth(source, sink)

        if path is not None:
            increasing_flow = self.find_min_in_path(path)
            return increasing_flow
        if path is None:
            return 0



    def ford_fulkerson(self, source, sink):
        """
        Execute the ford-fulkerson algorithm (i.e., repeated calls of ff_step())
        @param source the source's vertex id
        @param sink the sink's vertex id
        @return the max flow from source to sink
        """
        while self.ff_step(source,sink) != 0:
            self.ff_step(source,sink)

        maximal_flow = 0
        for row in self.current_flow[0]:
            maximal_flow += row
        return maximal_flow