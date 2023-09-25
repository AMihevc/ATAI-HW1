import networkx
import time
import random
import gzip
import sys
import igraph
from hw1_prof_solution import connected_components

# increase recursion limit for our method to work properly with large graphs
sys.setrecursionlimit(100001)

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

# A second alternative solution using igraph
def connected_components_alternative2(edges):

    graph = igraph.Graph.TupleList(edges)

    components = graph.connected_components()
    # here should we use the connected_components() method since clusters is deprecated

    return len(components)


# Professor's function to crate a set of random graphs
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

# Professor's function to write a graph to a file
def write_instance(V, E, filename):
    """Write a graph instance to a file (loosely, in a format used in DIMACS challenges)."""
    with open(filename, "w") as f:
        f.write(f"Nodes {n}\n")
        f.write(f"Edges {len(E)}\n")
        for (i,j) in E:
            f.write(f"E {i} {j}\n")

# Professor's function to read a graph from a file
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
    
    # time keeping
    total_time_prof = 0
    total_time_own = 0
    total_time_alt2 = 0
    flag = False

    # for n in [100, 1000, 10000, 100000, 1000000]: # old for loop (too big for my computer)
    for n in [100, 1000, 10000, 100000]: #number of vertices
        for k in [1, 2, 5, 10]: #n*k = max number of edges
            for r in range(1,11): #r is the random seed
                filename = f"G{n}-{k}-{r}.graph"
                
                # # uncomment for creating files with graphs (may be rather large):
                # V, E = mk_instance(n, k, r)
                # write_instance(V, E, filename)

                # # uncomment for reading graphs from files method: 
                V, E = read_instance(filename)
                
                # # uncomment for creating benchmark set in memory method:
                # V, E = mk_instance(n, k, r)
                
                # profs method
                start_prof = time.process_time()
                ncomponents_prof = connected_components(E) # defult method provided by the professor
                end_prof = time.process_time()
                
                # only time our own method
                start = time.process_time()
                ncomponents_own = connected_components_alternative1(E) # our own recursive method
                end = time.process_time()
                
                # only time our own method
                start_alt2 = time.process_time()
                ncomponents_alt2 = connected_components_alternative2(E) # our own recursive method
                end_alt2 = time.process_time()

                # check if the result of the alt1 and default method are the same
                if ncomponents_prof != ncomponents_own:
                    print(f"ERROR: number of components differs alt1 at {n}, {k}, {r}")
                    flag = True
                    continue
                
                # check if the result of the alt2 and default method are the same
                if ncomponents_prof != ncomponents_own:
                    print(f"ERROR: number of components differs alt2 at {n}, {k}, {r}")
                    flag = True
                    continue

                # add the time to the total time prof 
                cpu_prof = end_prof - start_prof
                total_time_prof += cpu_prof

                # add the time to the total time alt1 
                cpu = end - start
                total_time_own += cpu

                # add the time to the total time alt2
                cpu_alt2 = end_alt2 - start_alt2
                total_time_alt2 += cpu_alt2

                # # output of results
                # print(f"{filename}: {ncomponents_own} components, {cpu} seconds")
                
                # # instead of printing this to the terminal, we write it to a file
                with open("results.txt", "a") as f:
                    f.write(f"{filename}: {ncomponents_own} components, Alt1: {cpu} seconds, Alt2: {cpu_alt2} seconds\n")

    
    # catching the mismatch
    if flag: 
        print("ERROR: There was a mismatch in number of components between the default and our method.")
    
    # output of total time
    print(f"Total time for the professor's method: {total_time_prof} seconds")
    print(f"Total time for our alt1 method: {total_time_own} seconds")
    print(f"Total time for our alt2 method: {total_time_alt2} seconds")

    # also write the total time to the file
    with open("results.txt", "a") as f:
        f.write(f"Total time for the professor's method: {total_time_prof} seconds\n")
        f.write(f"Total time for our alt1 method: {total_time_own} seconds\n")
        f.write(f"Total time for our alt2 method: {total_time_alt2} seconds\n")


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