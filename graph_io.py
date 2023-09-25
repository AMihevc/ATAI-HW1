import networkx
import time
import random
import gzip
import sys
from hw1_prof_solution import connected_components

#increase recursion limit for our method to work properly with large graphs
sys.setrecursionlimit(10001)

# Manuel's recursive solution
def connected_components_alternative1(edges):
    def dfs(node):
        visited.add(node)
        component.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor)

    graph = {}
    for u, v in edges:
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []
        graph[u].append(v)
        graph[v].append(u)

    visited = set()
    components = []

    for node in graph:
        if node not in visited:
            component = []
            dfs(node)
            components.append(component)

    return len(components)

#Professor's function to crate a set of random graphs
def mk_instance(n, k, r):
    """Set random seed to 'r' and create a graph withn 'n' vertices and (up to) n * k edges."""
    random.seed(r)
    V = list(range(1,n+1))
    E = set()
    for _ in range(n*k):
        i = random.randint(1,n)
        j = random.randint(1,n)
        if i != j:
            i, j = min(i,j), max(i,j)
            E.add((i,j))
    return V, E

#Professor's function to write a graph to a file
def write_instance(V, E, filename):
    """Write a graph instance to a file (loosely, in a format used in DIMACS challenges)."""
    with open(filename, "w") as f:
        f.write(f"Nodes {n}\n")
        f.write(f"Edges {len(E)}\n")
        for (i,j) in E:
            f.write(f"E {i} {j}\n")

#Professor's function to read a graph from a file
def read_instance(filename):
    """Read a graph from a file."""
    try:
        if len(filename)>3 and filename[-3:] == ".gz":  # file compressed with gzip
            import gzip
            f = gzip.open(filename, "rt")
        else:   # usual, uncompressed file
            f = open(filename)
    except IOError:
        print("could not open file", filename)
        exit(-1)

    edges = set()
    for line in f:
        if line[0:6].lower() == 'edges ':
            e, n_edges = line.split()
            n_edges = int(n_edges)
        elif line[0:6].lower() == 'nodes ':
            e, n_nodes = line.split()
            n_nodes = int(n_nodes)
        elif line[0:2].lower() == 'e ':
            e, i, j = line.split()
            i, j = int(i), int(j)
            i, j = min(i,j), max(i,j)
            edges.add((i,j))
    f.close()

    assert n_edges == len(edges)
    vertices = list(range(1,n_nodes+1))
    return vertices, list(edges)


if __name__ == "__main__":
    
    #time keeping
    total_time_prof = 0
    total_time_own = 0

    #creating and testing graphs

    #for n in [100, 1000, 10000, 100000, 1000000]: # old for loop (too big for my computer)
    for n in [100, 1000, 10000]: #number of vertices
        for k in [1, 2, 5, 10]: #n*k = max number of edges
            for r in range(1,11): #r is the random seed
                
                # # uncomment for creating files with graphs (may be rather large):
                # V, E = mk_instance(n, k, r)
                # filename = f"G{n}-{k}-{r}.graph"
                # write_instance(V, E, filename)
                # print(n, k, len(E), connected_components(V, E))


                # # uncomment for reading graphs from files and solving with 'default' method:
                # filename = f"G{n}-{k}-{r}.graph"
                # V, E = read_instance(filename)
                # start = time.process_time()
                # ncomponents = connected_components(V,E)
                # end = time.process_time()
                # cpu = end - start
                # print(f"{filename}: {ncomponents} components, {cpu} seconds")
                
                # uncomment for creating benchmark set in memory and solving with 'default' method:
                V, E = mk_instance(n, k, r)
                
                # ncomponents = connected_components(V,E) #this is the original line but it doesn't work with the "old" solution (too many arguments)
                start_prof = time.process_time()
                ncomponents_prof = connected_components(E) # defult method provided by the professor
                end_prof = time.process_time()
                
                # only time our own method
                start = time.process_time()
                ncomponents_own = connected_components_alternative1(E) # our own recursive method
                end = time.process_time()
                
                #check if the result of the 2 methods is equal
                if ncomponents_prof != ncomponents_own:
                    print(f"ERROR: number of components differs! at {n}, {k}, {r}")
                    continue
                
                #add the time to the total time
                cpu_prof = end_prof - start_prof
                total_time_prof += cpu_prof

                #add the time to the total time
                cpu = end - start
                total_time_own += cpu

                #output of results
                filename = f"G{n}-{k}-{r} from memory"
                print(f"{filename}: {ncomponents_own} components, {cpu} seconds")
    
    #output of total time
    print(f"Total time for the professor's method: {total_time_prof} seconds")
    print(f"Total time for our own method: {total_time_own} seconds")

    # # uncomment for reading a graphs from a particular file and solving with 'default' method
    # if len(sys.argv) != 2:
    #     print(f"usage: {sys.argv[0]} filename\nwhere filename is the instance to be solved")
    # filename = sys.argv[1]
    # V, E = read_instance(filename)
    # start = time.process_time()
    # ncomponents = connected_components(V,E)
    # end = time.process_time()
    # cpu = end - start
    # print(f"{filename}: {ncomponents} components, {cpu} seconds")