# DFS vs. BFS

Before we start our lab work for today, here's a refresher for both the DFS and BFS algorithms:

## Depth-First Search (DFS)
Depth-first search (DFS) is an algorithm for traversing or searching tree or graph data structures. The algorithm starts at the root node (selecting some arbitrary node as the root node in the case of a graph) and explores as far as possible along each branch before backtracking. (Wikipedia)

### DFS - Example
_For the following graph_:

<img src="https://upload.wikimedia.org/wikipedia/commons/6/61/Graph.traversal.example.svg" />

A depth-first search starting at the node A, assuming that the left edges in the shown graph are chosen before right edges, and assuming the search remembers previously visited nodes and will not repeat them (since this is a small graph), will visit the nodes in the following order: A, B, D, F, E, C, G. The edges traversed in this search form a Trémaux tree, a structure with important applications in graph theory. Performing the same search **without remembering previously visited nodes** results in visiting the nodes in the order A, B, D, F, E, A, B, D, F, E, etc. forever, caught in the A, B, D, F, E cycle and never reaching C or G.

## Breadth-First Search (BFS)
Breadth-first search (BFS) is an algorithm for searching a tree data structure for a node that satisfies a given property. It starts at the tree root and explores all nodes at the present depth prior to moving on to the nodes at the next depth level. Extra memory, usually a queue, is needed to keep track of the child nodes that were encountered but not yet explored.

### BFS - Example
_For the following graph_:

<img src="https://media.geeksforgeeks.org/wp-content/uploads/bfs-5.png" />

In the following graph, we start traversal from vertex 2. When we come to vertex 0, we look for all adjacent vertices of it. 2 is also an adjacent vertex of 0. If we don’t mark visited vertices, then 2 will be processed again and it will become a non-terminating process. A Breadth-First Traversal of the following graph is 2, 0, 3, 1.


# Lab Work
In this lab, you'll get practice with depth-first search and
breadth-first search with some interactive exercises.

Start a new notebook on your virtual machine, then paste+run this code
in a cell (you don't need to read it):

```python
from IPython.core.display import display, HTML
from graphviz import Digraph

class test_graph:
    def __init__(self):
        self.nodes = {}
        self.traverse_order = None # in what order were nodes checked?
        self.next_guess = 0
        self.colors = {}

    def node(self, name):
        name = str(name).upper()
        self.nodes[name] = Node(self, name)

    def edge(self, src, dst):
        src, dst = str(src).upper(), str(dst).upper()
        for name in [src, dst]:
            if not name in self.nodes:
                self.node(name)
        self.nodes[src].children.append(self.nodes[dst])

    def _repr_svg_(self):
        g = Digraph(engine='neato')
        for n in self.nodes:
            g.node(n, fillcolor=self.colors.get(n, "white"), style="filled")
            children = self.nodes[n].children
            for i, child in enumerate(children):
                g.edge(n, child.name, penwidth=str(len(children) - i), len="1.5")
        return g._repr_svg_()

    def dfs(self, src, dst):
        src, dst = str(src).upper(), str(dst).upper()
        self.traverse_order = []
        self.next_guess = 0
        self.colors = {}
        self.visited = set()
        self.path = self.nodes[src].dfs(dst)
        display(HTML("now call .visit(???) to identify the first node explored"))
        display(self)

    def bfs(self, src, dst):
        src, dst = str(src).upper(), str(dst).upper()
        self.traverse_order = []
        self.next_guess = 0
        self.colors = {}
        self.path = self.nodes[src].bfs(dst)
        display(HTML("now call .visit(???) to identify the first node explored"))
        display(self)
    
    def visit(self, name):
        name = str(name).upper()
        if self.traverse_order == None:
            print("please call dfs or bfs first")
        if self.next_guess == len(self.traverse_order):
            print("no more nodes to explore")
            return
        self.colors = {}
        for n in self.traverse_order[:self.next_guess]:
            self.colors[n] = "yellow"
        if name == self.traverse_order[self.next_guess]:
            display(HTML("Correct..."))
            self.colors[name] = "yellow"
            self.next_guess += 1
        else:
            display(HTML("<b>Oops!</b> Please guess again."))
            self.colors[name] = "red"
        display(self)
        if self.next_guess == len(self.traverse_order):
            if self.path == None:
                display(HTML("You're done, there is no path!"))
            else:
                seq = input("What path was found? [enter nodes, comma separated]: ")
                seq = tuple(map(str.strip, seq.upper().split(",")))
                if seq == tuple(map(str.upper, self.path)):
                    print("Awesome!!!")
                else:
                    print("actually, expected was: ", ",".join(self.path))

    
class Node:
    def __init__(self, graph, name):
        self.graph = graph
        self.name = name
        self.children = []

    def __repr__(self):
        return "node %s" % self.name

    def dfs(self, dst):
        if self.name in self.graph.visited:
            return None
        
        self.graph.traverse_order.append(self.name)
        
        self.graph.visited.add(self.name)

        if self.name == dst:
            return (self.name, )
        for child in self.children:
            childpath = child.dfs(dst)
            if childpath:
                return (self.name, ) + childpath
        return None

    def backtrace(self):
        nodes = []
        node = self
        while node != None:
            nodes.append(node.name)
            node = node.back
        return tuple(reversed(nodes))

    def bfs(self, dst):
        added = set()
        todo = [self]
        self.back = None
        added.add(self.name)

        while len(todo) > 0:
            curr = todo.pop(0)
            self.graph.traverse_order.append(curr.name)

            if curr.name == dst:
                return curr.backtrace()
            else:
                for child in curr.children:
                    if not child.name in added:
                        todo.append(child)
                        child.back = curr
                        added.add(child.name)

        return None
```

## Problem 1 [4-node, DFS]

Paste the following to a cell:

```python
g = test_graph()
g.edge(1, 2)
g.edge(4, 3)
g.edge(1, 3)
g.edge(2, 4)
g
```

It should look something like this:

<img src="1.png" width=300>

Node 1 has two children: nodes 2 and 3.  The thicker line to node 2
indicates node 2 is in the `children` list before node 3.

Let's do a DFS from node 1 to 3.  Paste the following:

```python
g.dfs(1, 3)
```

You should see something like this:

<img src="2.png" width=500>

Try calling the visit function with

```python
g.visit(1)
```

The visited node should look like this:

<img src="3.png" width=300>

Keep making `g.visit(????)` calls until you complete the depth first search.

Once the target node is reach, you'll be prompted to enter the path
from source to destination.  Do so and type enter to check your
answer:

<img src="4.png" width=600>

## Problem 2 [4-node, BFS]

Paste+run the following:

```python
g = test_graph()
g.edge(1, 2)
g.edge(4, 3)
g.edge(1, 3)
g.edge(2, 4)
g.bfs(1, 3)
```

## Problem 3 [7-node, DFS+BFS]

Paste+run the following (same graph structure as last time, but you'll
visit the nodes in a different order):

```python
g = test_graph()
for i in range(5):
    g.edge(i, i+1)
    g.edge(i, 6)
    g.edge(6, i)
g.dfs(0, 4)
```

Then change `dfs` to `bfs` and try again.

## Problem 4 [6-node, BFS]

```python
g = test_graph()
for i in range(0, 4, 2):
    g.edge(i, i+2)
    g.edge(i+1, i+3)
    g.edge(i, i+1)
g.edge(4, 5)
g.bfs(2, 1)
```
