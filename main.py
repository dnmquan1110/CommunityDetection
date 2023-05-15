from ImplementGraph import ImplementUndirectedGraph
import ImplementGraph as IG
import NetworkX as NX

if __name__ == '__main__':
    G = ImplementUndirectedGraph()
    G.constructGraph('ub_sample_data.csv', 7)
    c1, m1 = IG.CommunityDectection(G, 'community_detection.txt')
    print(f'Highest modularity from implementation code: {m1}')
    print('\n')
    nx_G = NX.constructNetworkXGraph('ub_sample_data.csv', 7)
    c2, m2 = NX.CommunityDetection(nx_G, 'community_detection_nx.txt')
    print(f'Highest modularity from NetworkX: {m2}')
