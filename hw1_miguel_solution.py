import random
import time
import networkx # version 3.1 shall be used
import igraph # version 0.10.8 shall be used



def createGraphs(numLists, numVertices, probs):

    edgesList = []

    for listIdx in range(numLists):

        V = list(range(1, numVertices[listIdx]+1))

        # create a list E containing pairs (i, j) from the elements in V where i is less than j, and each pair is included in the list with a certain probability prob
        E = [(i,j) for i in V for j in V if i < j and random.random() < probs[listIdx]]

        #print("vertices:", V)
        #print("edges:", E)

        edgesList.append(E)

    return edgesList

random.seed(10)

numLists = 10                           # 100 if more memory is available, otherwise use 10
smallGraphMinSize = 5
smallGraphMaxSize = 10
largeGraphMinSize = 1000                # 10000 if more memory is available, otherwise use 1000
largeGraphMaxSize = 2000                # 20000 if more memory is available, otherwise use 2000

smallSparseGraphMinEdgeProb = 0.01
smallSparseGraphMaxEdgeProb = 0.03
smallDenseGraphMinEdgeProb = 0.1
smallDenseGraphMaxEdgeProb = 0.2
largeSparseGraphMinEdgeProb = 0.00001   # 0.000001 if more memory is available, otherwise use 0.00001
largeSparseGraphMaxEdgeProb = 0.00003   # 0.000003 if more memory is available, otherwise use 0.00003
largeDenseGraphMinEdgeProb = 0.0001     # 0.00001 if more memory is available, otherwise use 0.0001
largeDenseGraphMaxEdgeProb = 0.0003     # 0.00003 if more memory is available, otherwise use 0.0003

numVertices_smallSparse = [random.randint(smallGraphMinSize, smallGraphMaxSize) for _ in range(numLists)]
probs_smallSparse = [random.uniform(smallSparseGraphMinEdgeProb, smallSparseGraphMaxEdgeProb) for _ in range(numLists)]
edgesList_smallSparse = createGraphs(numLists, numVertices_smallSparse, probs_smallSparse)
#print(edgesList_smallSparse)

numVertices_smallDense = [random.randint(smallGraphMinSize, smallGraphMaxSize) for _ in range(numLists)]
probs_smallDense = [random.uniform(smallDenseGraphMinEdgeProb, smallDenseGraphMaxEdgeProb) for _ in range(numLists)]
edgesList_smallDense = createGraphs(numLists, numVertices_smallDense, probs_smallDense)
#print(edgesList_smallDense)

numVertices_largeSparse = [random.randint(largeGraphMinSize, largeGraphMaxSize) for _ in range(numLists)]
probs_largeSparse = [random.uniform(largeSparseGraphMinEdgeProb, largeSparseGraphMaxEdgeProb) for _ in range(numLists)]
edgesList_largeSparse = createGraphs(numLists, numVertices_largeSparse, probs_largeSparse)
#print(edgesList_largeSparse)

numVertices_largeDense = [random.randint(largeGraphMinSize, largeGraphMaxSize) for _ in range(numLists)]
probs_largeDense = [random.uniform(largeDenseGraphMinEdgeProb, largeDenseGraphMaxEdgeProb) for _ in range(numLists)]
edgesList_largeDense = createGraphs(numLists, numVertices_largeDense, probs_largeDense)
#print(edgesList_largeDense)



def evaluateAlgo(edgesList, algo, numLists):

    numConnectedComponents_total = 0
    time_total = 0

    for edges in edgesList:
        start = time.perf_counter()
        numConnectedComponents = algo(edges)
        end = time.perf_counter()
        timeUsed = end - start

        #print("number of connected components:", numConnectedComponents_reference)
        #print(f"CPU time used: {time_reference} seconds")

        time_total = time_total + timeUsed
        numConnectedComponents_total = numConnectedComponents_total + numConnectedComponents

    numConnectedComponents_avg = numConnectedComponents_total / numLists
    time_avg = time_total / numLists

    print(f"Average number of connected components: {numConnectedComponents_avg}")
    print(f"Average CPU time used: {time_avg} seconds")
    print("\n")

    return numConnectedComponents_avg, time_total


def connected_components(edges):
    G = networkx.Graph()
    G.add_edges_from(edges)
    Components = list(networkx.connected_components(G))
    return len(Components)

#print(networkx.__version__)

numConnectedComponents_reference_avg_smallSparse, time_reference_avg_smallSparse = evaluateAlgo(edgesList_smallSparse, connected_components, numLists)

numConnectedComponents_reference_avg_smallDense, time_reference_avg_smallDense = evaluateAlgo(edgesList_smallDense, connected_components, numLists)

numConnectedComponents_reference_avg_largeSparse, time_reference_avg_largeSparse = evaluateAlgo(edgesList_largeSparse, connected_components, numLists)

numConnectedComponents_reference_avg_largeDense, time_reference_avg_largeDense = evaluateAlgo(edgesList_largeDense, connected_components, numLists)


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


numConnectedComponents_alternative1_avg_smallSparse, time_alternative1_avg_smallSparse = evaluateAlgo(edgesList_smallSparse, connected_components_alternative1, numLists)

numConnectedComponents_alternative1_avg_smallDense, time_alternative1_avg_smallDense = evaluateAlgo(edgesList_smallDense, connected_components_alternative1, numLists)

numConnectedComponents_alternative1_avg_largeSparse, time_alternative1_avg_largeSparse = evaluateAlgo(edgesList_largeSparse, connected_components_alternative1, numLists)

numConnectedComponents_alternative1_avg_largeDense, time_alternative1_avg_largeDense = evaluateAlgo(edgesList_largeDense, connected_components_alternative1, numLists)


def connected_components_alternative2(edges):

    graph = igraph.Graph.TupleList(edges)

    components = graph.clusters()
    #here should we use the connected_components() method since clusters is deprecated

    return len(components)

numConnectedComponents_alternative2_avg_smallSparse, time_alternative2_avg_smallSparse = evaluateAlgo(edgesList_smallSparse, connected_components_alternative2, numLists)

numConnectedComponents_alternative2_avg_smallDense, time_alternative2_avg_smallDense = evaluateAlgo(edgesList_smallDense, connected_components_alternative2, numLists)

numConnectedComponents_alternative2_avg_largeSparse, time_alternative2_avg_largeSparse = evaluateAlgo(edgesList_largeSparse, connected_components_alternative2, numLists)

numConnectedComponents_alternative2_avg_largeDense, time_alternative2_avg_largeDense = evaluateAlgo(edgesList_largeDense, connected_components_alternative2, numLists)


#OUTPUT:
print(f"Alternative 1 output is the same as reference (smallSparse)? {numConnectedComponents_alternative1_avg_smallSparse == numConnectedComponents_reference_avg_smallSparse}")
print(f"Alternative 1 output is the same as reference (smallDense)? {numConnectedComponents_alternative1_avg_smallDense == numConnectedComponents_reference_avg_smallDense}")
print(f"Alternative 1 output is the same as reference (largeSparse)? {numConnectedComponents_alternative1_avg_largeSparse == numConnectedComponents_reference_avg_largeSparse}")
print(f"Alternative 1 output is the same as reference (largeDense)? {numConnectedComponents_alternative1_avg_largeDense == numConnectedComponents_reference_avg_largeDense}")

print("\n")

print(f"Alternative 2 output is the same as reference (smallSparse)? {numConnectedComponents_alternative2_avg_smallSparse == numConnectedComponents_reference_avg_smallSparse}")
print(f"Alternative 2 output is the same as reference (smallDense)? {numConnectedComponents_alternative2_avg_smallDense == numConnectedComponents_reference_avg_smallDense}")
print(f"Alternative 2 output is the same as reference (largeSparse)? {numConnectedComponents_alternative2_avg_largeSparse == numConnectedComponents_reference_avg_largeSparse}")
print(f"Alternative 2 output is the same as reference (largeDense)? {numConnectedComponents_alternative2_avg_largeDense == numConnectedComponents_reference_avg_largeDense}")

print("\n")
print("\n")
print("\n")

print(f"Reference CPU time used: {time_reference_avg_smallSparse:.5f} seconds (smallSparse)")
print(f"Alternative 1 CPU time used: {time_alternative1_avg_smallSparse:.5f} seconds (smallSparse)")
print(f"Alternative 2 CPU time used: {time_alternative2_avg_smallSparse:.5f} seconds (smallSparse)")

print("\n")

print(f"Reference CPU time used: {time_reference_avg_smallDense:.5f} seconds (smallDense)")
print(f"Alternative 1 CPU time used: {time_alternative1_avg_smallDense:.5f} seconds (smallDense)")
print(f"Alternative 2 CPU time used: {time_alternative2_avg_smallDense:.5f} seconds (smallDense)")

print("\n")

print(f"Reference CPU time used: {time_reference_avg_largeSparse:.5f} seconds (largeSparse)")
print(f"Alternative 1 CPU time used: {time_alternative1_avg_largeSparse:.5f} seconds (largeSparse)")
print(f"Alternative 2 CPU time used: {time_alternative2_avg_largeSparse:.5f} seconds (largeSparse)")

print("\n")

print(f"Reference CPU time used: {time_reference_avg_largeDense:.5f} seconds (largeDense)")
print(f"Alternative 1 CPU time used: {time_alternative1_avg_largeDense:.5f} seconds (largeDense)")
print(f"Alternative 2 CPU time used: {time_alternative2_avg_largeDense:.5f} seconds (largeDense)")