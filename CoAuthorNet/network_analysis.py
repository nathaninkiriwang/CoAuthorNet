import pandas as pd
import networkx as nx
import numpy as np
from scholarly import scholarly
import os
from tqdm import tqdm
import json

def fetch_publications(staff_data, output_csv='staff_publications_data.csv', affiliation=None):
    if os.path.exists(output_csv):
        staff_publications_data = pd.read_csv(output_csv)
    else:
        staff_publications_data = pd.DataFrame(columns=['staff_name', 'publication', 'publication_year'])
    
    processed_staff = set(staff_publications_data['staff_name'])
    new_data = []

    # Add tqdm progress bar here
    for staff in tqdm(staff_data['Staff Name'], desc="Fetching publications"):
        if staff in processed_staff:
            continue

        try:
            search_query = scholarly.search_author(f"{staff}, {affiliation}")
            first_author_result = next(search_query)
            author = scholarly.fill(first_author_result)
            publication_titles = [pub['bib']['title'] for pub in author['publications']]
            publication_years = [pub['bib'].get('pub_year', 'Unknown') for pub in author['publications']]
            for title, year in zip(publication_titles, publication_years):
                new_data.append({'staff_name': staff, 'publication': title, 'publication_year': year})
        except StopIteration:
            print(f"No publications found for {staff}")
        except Exception as e:
            print(f"Error retrieving data for {staff}: {e}")

        if len(new_data) >= 10:
            new_df = pd.DataFrame(new_data)
            staff_publications_data = pd.concat([staff_publications_data, new_df], ignore_index=True)
            staff_publications_data.to_csv(output_csv, index=False)
            new_data = []

    if new_data:
        new_df = pd.DataFrame(new_data)
        staff_publications_data = pd.concat([staff_publications_data, new_df], ignore_index=True)
        staff_publications_data.to_csv(output_csv, index=False)

    return staff_publications_data

def create_bipartite_network(df):
    G = nx.Graph()
    authors = df['staff_name'].unique()
    author_id = {author: idx for idx, author in enumerate(authors)}
    paper_dict = {}
    paper_ind = len(authors)

    # tqdm progress bar for iterating over rows
    for _, row in tqdm(df.iterrows(), desc="Creating bipartite network", total=len(df)):
        author, paper = row['staff_name'], row['publication']
        if paper not in paper_dict:
            paper_dict[paper] = paper_ind
            G.add_node(paper_ind, bipartite=1)
            paper_ind += 1
        G.add_edge(author_id[author], paper_dict[paper])
    
    return G, author_id, paper_dict

def create_authorship_network(G, author_id):
    author_network = nx.Graph()
    author_network.add_nodes_from([(idx, {'label': name}) for name, idx in author_id.items()])

    # tqdm progress bar for iterating over paper nodes
    for _, paper_id in tqdm(G.edges(), desc="Creating authorship network", total=len(G.edges())):
        neighbors = list(G.neighbors(paper_id))
        for i in range(len(neighbors)):
            for j in range(i + 1, len(neighbors)):
                author_network.add_edge(neighbors[i], neighbors[j])
    return author_network

def get_largest_component(graph):
    largest_cc = max(nx.connected_components(graph), key=len)
    return graph.subgraph(largest_cc)

def save_graph(graph, file_path="largest_component.graphml"):
    """Save the graph to a .graphml file."""
    nx.write_graphml(graph, file_path)
    print(f"Graph saved as {file_path}")


def calculate_metrics(G, output_file="metrics.json"):
    degs = [G.degree()[node] for node in tqdm(G.nodes(), desc="Calculating Degrees")]
    metrics = {
        "Average Degree": np.mean(degs),
        "Degree Standard Deviation": np.std(degs),
        "Clustering Coefficient": nx.transitivity(G),
        "Average Shortest Path Length": nx.average_shortest_path_length(G),
        "Diameter": nx.diameter(G),
        "Number of Nodes": G.number_of_nodes(),
        "Number of Edges": G.number_of_edges(),
    }
    
    with open(output_file, "w") as f:
        json.dump(metrics, f, indent=4)
    
    return metrics