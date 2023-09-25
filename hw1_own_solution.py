import time
import random


class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v):
        if u in self.graph:
            self.graph[u].append(v)
        else:
            self.graph[u] = [v]

        if v in self.graph:
            self.graph[v].append(u)
        else:
            self.graph[v] = [u]

    def dfs(self, node, visited, component):
        visited[node] = True
        component.append(node)
        for neighbor in self.graph[node]:
            if not visited[neighbor]:
                self.dfs(neighbor, visited, component)

    def connected_components(self):
        visited = {}
        components = []

        for node in self.graph:
            visited[node] = False

        for node in self.graph:
            if not visited[node]:
                component = []
                self.dfs(node, visited, component)
                components.append(component)

        return components


# Example usage:
if __name__ == "__main__":
    graph = Graph()
    graph.add_edge(0, 1)
    graph.add_edge(0, 2)
    graph.add_edge(1, 2)
    graph.add_edge(3, 4)
    graph.add_edge(5, 6)

    components = graph.connected_components()
    print("Number of connected components:", len(components))
    
    # print("Connected Components:")
    # for component in components:
    #     print(component)

#unfinised as it is very similar to Manuel's solution so we switched to using that one for our evaluation