import pandas as pd
from collections import deque
from collections import OrderedDict
from copy import deepcopy
from tqdm import tqdm
import numpy as np

class ImplementUndirectedGraph:
    def __init__(self):
        self.nodes = {}
        self.edges = set()
        self.name2idx = OrderedDict()

    def add_node(self, node):
        if node not in self.nodes:
            self.nodes[node] = {}
            self.name2idx[node] = len(self.name2idx)

    def add_edge(self, node1, node2):
        self.add_node(node1)
        self.add_node(node2)

        if node1 not in self.nodes[node2]:
            self.nodes[node1][node2] = 0
        if node2 not in self.nodes[node1]:
            self.nodes[node2][node1] = 0

        self.nodes[node1][node2] = 1
        self.nodes[node2][node1] = 1
        self.edges.add(tuple(sorted([node1, node2])))

    def number_of_edges(self):
        return len(self.edges)

    def number_of_nodes(self):
        return len(self.nodes)

    def constructGraph(self, filename: str, threshold: int):
        df = pd.read_csv(filename)
        user_id = df.user_id.unique()
        user_review = {}
        for u in tqdm(user_id, desc= 'Get list business review of each user'):
            user_review[u] = set(df[df.user_id == u].business_id.unique())
        for i in tqdm(range(len(user_id)), desc=f'Constructing implementation graph with each user and other users who have {threshold} same business review'):
            for j in range(i + 1, len(user_id)):
                if len(user_review[user_id[i]] & user_review[user_id[j]]) >= threshold:
                    self.add_edge(user_id[i], user_id[j])
        print(f'Finish constructing implementation graph, the graph has {self.number_of_nodes()} nodes and {self.number_of_edges()} edges')

    def adjacency_matrix(self):
        matrix = [[0 for i in range(len(self.nodes))] for j in range(len(self.nodes))]
        for u in self.nodes:
            for v in self.nodes[u]:
                matrix[self.name2idx[u]][self.name2idx[v]] = 1
                matrix[self.name2idx[v]][self.name2idx[u]] = 1
        return matrix

    def remove_edge(self, edge: tuple):
        self.nodes[edge[0]].pop(edge[1])
        self.nodes[edge[1]].pop(edge[0])
        self.edges.remove(tuple(sorted([edge[0], edge[1]])))

    def shortest_path_by_BFS(self, root):
        pre_node = {v: [] for v in self.nodes}
        number_shortest_path = {v: 0 for v in self.nodes}
        number_shortest_path[root] = 1
        bfs = []
        depth = {root: 0}
        Q = deque([root])
        while Q:
            node1 = Q.popleft()
            bfs.append(node1)
            for node2 in self.nodes[node1]:
                if node2 not in depth:
                    depth[node2] = depth[node1] + 1
                    Q.append(node2)
                if depth[node2] == depth[node1] + 1:
                    number_shortest_path[node2] += number_shortest_path[node1]
                    pre_node[node2].append(node1)
        return bfs, pre_node, number_shortest_path

    def edge_betweenness(self, betweenness_score, bfs, pre_node, number_shortest_path):
        credit = dict.fromkeys(self.nodes, 1)
        while bfs:
            node = bfs.pop()
            for p_node in pre_node[node]:
                c = credit[node] * number_shortest_path[p_node] / number_shortest_path[node]
                betweenness_score[tuple(sorted([node, p_node]))] += c
                credit[p_node] += c
        return betweenness_score

    def calculate_betweenness_score(self, result_filename: None):
        betweenness_score = dict.fromkeys(self.edges, 0)
        for node in self.nodes:
            bfs, pre_node, number_shortest_path = self.shortest_path_by_BFS(node)
            betweenness_score = self.edge_betweenness(betweenness_score, bfs, pre_node, number_shortest_path)
        betweenness_score = {key: val/2 for (key, val) in betweenness_score.items()}
        betweenness_score = dict(sorted(betweenness_score.items(), key=lambda i: (i[1], i[0])))
        betweenness_score = dict(sorted(betweenness_score.items(), key=lambda i: i[1], reverse=True))
        if result_filename is not None:
            f = open(result_filename, "w")
            for key, value in betweenness_score.items():
                f.write(str(key) + ', ' + str(value) + '\n')
            f.close()
        return betweenness_score


def calculate_modularity(G: ImplementUndirectedGraph, adjacency_matrix_G, community, resolution = 1):
    m = np.sum(adjacency_matrix_G) / 2
    k = np.sum(adjacency_matrix_G, axis=0)
    Q = 0
    for i in range(len(community)):
        c_i = [G.name2idx[node] for node in community[i]]
        A_i = np.sum(np.array(adjacency_matrix_G)[np.ix_(c_i, c_i)])
        Q += (A_i - resolution * (k[c_i].sum())**2 / (2 * m))
    Q /= (2 * m)
    return Q


def get_connected_components(G: ImplementUndirectedGraph):
    not_visited = list(G.nodes.keys())
    components = []
    while not_visited:
        c = []
        queue = [not_visited.pop()]
        c.append(queue[0])
        while queue:
            for edge in G.edges:
                if queue[0] in edge:
                    tmp = edge[0] if edge[0] != queue[0] else edge[1]
                    if tmp in not_visited:
                        queue.append(tmp)
                        not_visited.remove(tmp)
                        c.append(tmp)
            queue.pop(0)
        components.append(c)
    return components

def sort_communities(communities):
    communities = [sorted(c) for c in communities]
    return sorted(communities)

def Girvan_Newman(G: ImplementUndirectedGraph):
    G_copy = deepcopy(G)
    communities = []
    betweenness_score = G_copy.calculate_betweenness_score(None)
    while G_copy.number_of_edges() != 0:
        new_component_len = origin_component_len = len(get_connected_components(G_copy))
        while (new_component_len == origin_component_len):
            remove_edge = next(iter(betweenness_score))
            betweenness_score.pop(remove_edge)
            G_copy.remove_edge(remove_edge)
            new_community = get_connected_components(G_copy)
            new_component_len = len(new_community)
        betweenness_score = G_copy.calculate_betweenness_score(None)
        communities.append(new_community)
    return communities

def CommunityDectection(G: ImplementUndirectedGraph, result_filename = None):
    print(f'Divide the graph into communities using Girvan-Newman algorith: ', end='')
    communities = Girvan_Newman(G)
    print(f'Done!')
    max_modularity = -1
    adjacency_matrix = G.adjacency_matrix()

    for c in tqdm(communities, desc = 'Calculating the modularity score of each community'):
        modularity = calculate_modularity(G, adjacency_matrix, c)
        if (modularity > max_modularity):
            max_modularity = modularity
            best_community = c

    best_community = [sorted(b) for b in best_community]
    best_community.sort(key=lambda item: (len(item), item))
    if result_filename is not None:
        f = open(result_filename, 'w')
        for c in best_community:
            c = [str(f"\'{i}\'") for i in c]
            tmp = ', '.join(c)
            f.write(f'{tmp} \n')
        f.close()
    return best_community, max_modularity