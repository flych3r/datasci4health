import json

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import community


plt.style.use("seaborn-dark")


if __name__ == "__main__":
    my_inflamome = pd.read_excel(
        "../data/external/protein-network.XLS",
        sheet_name="My-Inflamome",
        names=["source", "int", "target"],
        dtype=str,
    )

    my_inflamome[my_inflamome.isna().any(axis=1)]
    my_inflamome.fillna("None", inplace=True)

    MyInflamome = nx.from_pandas_edgelist(my_inflamome)
    polar = nx.circular_layout(MyInflamome)

    print("calculando trafego e grau dos nós")
    traffic = nx.betweenness_centrality(MyInflamome, normalized=True)
    node_degree = dict(MyInflamome.degree())

    high_traffic_proteins = pd.DataFrame.from_dict(
        traffic, orient="index", columns=["traffic"]
    )
    high_traffic_proteins.sort_values(by="traffic", ascending=False, inplace=True)

    high_degree_proteins = pd.DataFrame.from_dict(
        node_degree, orient="index", columns=["degree"]
    )
    high_degree_proteins.sort_values(by="degree", ascending=False, inplace=True)

    high_traffic_proteins.to_csv("../data/processed/high_traffic.csv")
    high_degree_proteins.to_csv("../data/processed/high_degree.csv")

    print("trafego e Grau")
    print(high_traffic_proteins.head(10))
    print(high_degree_proteins.head(10))

    plt.figure(figsize=(16, 9))
    plt.scatter(x=high_degree_proteins["degree"], y=high_traffic_proteins["traffic"])
    plt.xlabel("degree")
    plt.ylabel("traffic")
    plt.title("Correlação entre grau e trafego do nó")
    plt.show()

    communities_generator = community.greedy_modularity_communities(MyInflamome)
    print('Numero de comunidades:', len(communities_generator))

    communities = {f'Modulo {i}': list(c) for i, c in enumerate(communities_generator, start=1)}
    with open('../data/processed/communities.json', 'w') as f:
        json.dump(communities, f, indent=4)

    plt.figure(figsize=(16, 16))
    nx.draw(MyInflamome, pos=polar, with_labels=False, node_size=100)
    plt.title("MyInflamome")
    plt.savefig("../graphics/MyInflamome.pdf")
    plt.show()

    fig, axs = plt.subplots(
        nrows=5, ncols=5, figsize=(16, 16), subplot_kw={"xticks": [], "yticks": []}
    )

    for i, (ax, module) in enumerate(zip(axs.flat, communities_generator), start=1):
        view = nx.subgraph_view(MyInflamome, filter_node=lambda x: x in module)
        ax.set_title(f"Modulo {i}")
        nx.draw(view, pos=polar, with_labels=False, node_size=100, ax=ax)

    plt.tight_layout()
    plt.savefig("../graphics/MyInflamome-modules.pdf")
    plt.show()
