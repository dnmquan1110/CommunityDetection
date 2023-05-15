---
title: "Lab 02: Building a Sentiment Analysis Benchmark"
author: ["Dang Nguyen Minh Quan"]
date: "2023-04-14"
subtitle: "CSC14114 Big Data Application 19KHMT"
lang: "en"
titlepage: true
titlepage-color: "0B1887"
titlepage-text-color: "FFFFFF"
titlepage-rule-color: "FFFFFF"
titlepage-rule-height: 2
book: true
classoption: oneside
code-block-font-size: \scriptsize
---

Task | Completed
------------------|----------------------------------------
Constructing Graph      | **Percent**: 100
Betweenness Calculation      | **Percent**: 100
Girvan-Newman       | **Percent**: 100
Community Detection    | **Percent**: 100
Girvan-Newman using NetworkX | Percent: 100
Compare results provided by NetworkX and my implementaion | **Percent**: 100


# Lab 03: Community Detection

This kernel has 3 file:
- **ImplementGraph.py**: implementation code for graph construction, edge betweenness score calculating, girvan-newman algorithm and community detection
- **NetworkX.py**: create NetworkX graph and community detection using edge betweenness centrality and girvan-newman algorithm from NetworkX
- **main.py**: run this file to run the kernel


## Task 1: Community Detection using Girvan-Newman algorithm (GM)

### Constructing Graph

In **ImplementGraph.py**, I create class **ImplementUndirectedGraph** for constructing graph. The graph has 3 variable: 
- **nodes** is set of nodes, and each node (called n temporarily) has set of other node which has a link to node n
- **edges**, including set of edges. each name edge is store in tuple format, the order of 2 node 
This class has some basic function need for graph: add_node, add_edge, number_of_edges, number_of_nodes,...
- **name2idx**: convert the name node type string to int

There is a **constructGraph()** function, which read a csv data to collect nodes, edges and create graph. I collect all _business_id_ review of each _user_id_. And compare the number of the same _business_id_ review of each pair _user_id_, if this value >= _threshold_, I add each pair user_id as 2 nodes and an edge between them in graph.
The _threshold_ in this kernel is 7.

### Betweenness Calculation

I calculate the betweenness score of each edge in **calculate_betweenness_score()** function. For each node in graph, I calculate this score by finding the shortest path from this node to others node using BFS in **shortest_path_by_BFS()** function.
After all, for each edge, sum all betweenness score calculated below to have the final score.

To write list edge and their betweenness score into file, you define the argument _result_filename_ as the output filename (default is None - no write  output file)

### Girvan-Newman 
The **Girvan_Newman()** function return the list of communities.

The idea was to find which edges in a network occur most frequently between other pairs of nodes by finding edges betweenness centrality.

The Girvan-Newman algorithm can be divided into 3 main steps:

1. Calculate the betweenness centrality of all edges.
2. Drop the edge in turn with the highest betweenness centrality until the graph has more components
3. Repeat steps 1,2 until there are no more edges left.

### Community detecion using Girvan-Newman algorithm
The function **CommunityDectection()** detect community of the graph, with the output include the best community and it's modularity score.

For each community as the output of Girvan-Newman algorithm, calculating their modularity score. The community has the highest modularity score is the best community while divide graph.

Define the argument _result_filename_ to write the best community to _result_filename_ file.

##  Task 2: Community Detection using Girvan-Newman algorithm in NetworkX
All thing using NetworkX are in **NetworkX.py**. **constructNetworkXGraph()** function return the graph which collect data from csv data file.

The **CommunityDetection()** function return a community which has the highest modularity score and it's modularity score.

Define the argument _result_filename_ to write the best community to _result_filename_ file.

## Compare the result provided by NetworkX and my implementation
I have compare 2 communities result , one is from my implementation, another is from NetworkX
Both 2 communities has the same number of group, and length of each group has the same size too. 
But 2 modularity has a very small difference, and some node are located differently.


I found out the reason for that slight difference. 
The reason is edge betweenness centrality. 
My edge betweenness centrality calculating is correct, but my result has an automatic round, lead to the difference sorted list edge. 
For example, my implementation calculate betweenness score centrality of 2 edge a and b is the same 1. 
So I will rank a before b. But, with NetworkX, it calculates a and b is 1 and 1.00000001, so it rank b before a.

By the way, my implementation is correct!!

### Run this kernel
To run this kernel, you must install **NetworkX** library, and run file **main.py**. It will print the highest community's modularity from both my implementation and NetworkX,
simultaneously write 2 output file of 2 community : _commnunity_detection.txt_ and c*ommunity_detection_nx.txt*.

## References
- Slides
