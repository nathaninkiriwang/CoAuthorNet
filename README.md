# CoAuthorNet

**CoAuthorNet** is a Python package for analyzing and visualizing university authorship networks. It facilitates the retrieval of publication data for university staff, builds co-authorship networks, calculates network metrics, and visualizes the largest connected component of the network. CoAuthorNet is ideal for researchers interested in studying collaboration patterns within academic institutions.

## Features

- Fetch publication data for university staff from Google Scholar
- Create bipartite author-publication and co-authorship networks
- Calculate network metrics (average degree, clustering coefficient, shortest path length, etc.)
- Visualize the largest connected component of the co-authorship network

## Installation

To install CoAuthorNet, use `pip`:

```bash
pip install CoAuthorNet
```

## Requirements

CoAuthorNet requires the following dependencies:

- `pandas`
- `networkx`
- `numpy`
- `matplotlib`
- `tqdm`
- `scholarly`

These are automatically installed with the package.

## Usage

Here’s a quick example to get started with CoAuthorNet.

1. **Prepare a CSV file** with a column named `Staff Name`, containing the names of staff members. Example CSV (`author_school.csv`):

   ```csv
   Staff Name,School,Faculty
   Alice Smith,School of Chemistry,Faculty of Science
   Bob Jones,School of Physics,Faculty of Science
   ```

2. **Run the code** below to create and analyze the co-authorship network:

   ```python
    import CoAuthorNet as yn
    import pandas as pd

    staff_data = pd.read_csv("./author_school.csv")
    staff_publications_data = yn.fetch_publications(staff_data)


    G, author_dict, paper_dict = yn.create_bipartite_network(staff_publications_data)
    author_network = yn.create_authorship_network(G, author_dict)


    author_network_gc = yn.get_largest_component(author_network)
    yn.save_graph(author_network_gc, "largest_component.graphml")
    metrics = yn.calculate_metrics(author_network_gc)
    print(metrics)
   ```

## Function Reference

- **`fetch_publications(staff_data, output_csv='staff_publications_data.csv')`**
  - Fetches publication data for each staff member and saves it to a CSV file.

- **`create_bipartite_network(df)`**
  - Creates a bipartite network of authors and publications from the data.

- **`create_authorship_network(G, author_dict)`**
  - Converts the bipartite network into a co-authorship network.

- **`get_largest_component(graph)`**
  - Extracts the largest connected component of a graph.

- **`calculate_metrics(G)`**
  - Calculates various network metrics like average degree, clustering coefficient, etc.

- **`save_graph(G)`**
    - Saves largest component as a `.graphml` file.


- **`plot_network(G, output_file='largest_component_network.png')`**
  - Plots and saves the largest connected component of the co-authorship network.
 
## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


## Contributing

Contributions are welcome! Feel free to submit a pull request or report issues.
