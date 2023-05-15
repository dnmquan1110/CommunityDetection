import networkx as nx
import pandas as pd
from tqdm import tqdm

def createNetworkXGraph():
    return nx.Graph()

def constructNetworkXGraph(filename: str, threshold: int):
    G = nx.Graph()
    df = pd.read_csv(filename)
    user_id = df.user_id.unique()
    user_review = {}
    for u in tqdm(user_id, desc='Get list business review of each user'):
        user_review[u] = set(df[df.user_id == u].business_id.unique())
    for i in tqdm(range(len(user_id)), desc=f'Constructing NetworkX graph with each user and other users who have {threshold} same business review'):
        for j in range(i + 1, len(user_id)):
            if len(user_review[user_id[i]] & user_review[user_id[j]]) >= threshold:
                G.add_edge(user_id[i], user_id[j])
    print(f'Finish constructing graph, the graph has {G.number_of_nodes()} nodes and {G.number_of_edges()} edges')
    return G

def CommunityDetection(G: nx.Graph(), result_filename = None):
    print(f'Divide the graph into communities using Girvan-Newman algorith: ', end='')
    communities = nx.community.girvan_newman(G)
    print(f'Done!')
    max_modularity = -1
    for c in tqdm(communities, desc = 'Calculating the modularity score of each community'):
        if c is not None:
            modularity = nx.community.modularity(G, c)
            if (modularity > max_modularity):
                max_modularity = modularity
                best_community = c
    best_community = list(best_community)
    best_community = [sorted(i) for i in best_community]
    best_community.sort(key=lambda item: (len(item), item))
    if result_filename is not None:
        f = open(result_filename, 'w')
        for c in best_community:
            c = [str(f"\'{i}\'") for i in c]
            tmp = ', '.join(c)
            f.write(f'{tmp} \n')
        f.close()
    return best_community, max_modularity