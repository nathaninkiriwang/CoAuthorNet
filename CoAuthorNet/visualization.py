import matplotlib.pyplot as plt
import networkx as nx

def plot_network(G, output_file='largest_component_network.png'):
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=50, font_size=8)
    plt.title("Authorship Network (Largest Component)")
    plt.savefig(output_file)
    plt.show()