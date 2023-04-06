import json
import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(jsonld_data):
    try:
        jsonld = json.loads(jsonld_data)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON-LD data: {e}")
        return None

    if '@graph' not in jsonld:
        print("Error: '@graph' key not found in JSON-LD data.")
        return None

    graph = nx.DiGraph()

    for node in jsonld['@graph']:
        if not isinstance(node, dict) or '@id' not in node:
            print("Error: Invalid node in JSON-LD data.")
            continue

        node_id = node['@id']
        graph.add_node(node_id, **node)

        if 'includes' in node:
            for dependency in node['includes']:
                graph.add_edge(node_id, dependency)

    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=1500, node_color="skyblue", font_size=10, font_weight='bold')
    edge_labels = nx.get_edge_attributes(graph, 'label')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8)

    plt.savefig('graph.png')
    plt.show()

    return 'graph.png'
