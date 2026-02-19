import networkx as nx
import pandas as pd

def build_graph(df: pd.DataFrame):
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    G = nx.DiGraph()
    node_stats = {}

    for _, row in df.iterrows():
        sender = row["sender_id"]
        receiver = row["receiver_id"]

        G.add_edge(sender, receiver, amount=row["amount"], timestamp=row["timestamp"])

        for node in [sender, receiver]:
            if node not in node_stats:
                node_stats[node] = {
                    "transactions": 0,
                    "patterns": set(),
                    "ring_ids": set(),
                    "amounts": []
                }

        node_stats[sender]["transactions"] += 1
        node_stats[receiver]["transactions"] += 1
        node_stats[sender]["amounts"].append(row["amount"])

    return G, node_stats
