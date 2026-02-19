import numpy as np
import networkx as nx

def calculate_suspicion(G, node_stats, fraud_rings):

    try:
        pagerank = nx.pagerank(G, max_iter=50)
        betweenness = nx.betweenness_centrality(G)
    except:
        pagerank = {}
        betweenness = {}

    suspicious = []

    for node, data in node_stats.items():

        score = 0

        if any("cycle" in p for p in data["patterns"]):
            score += 40

        if "smurfing" in data["patterns"]:
            score += 30

        if "shell_network" in data["patterns"]:
            score += 20

        score += pagerank.get(node, 0) * 20
        score += betweenness.get(node, 0) * 20

        if data["transactions"] >= 20:
            score += 10

        # FALSE POSITIVE CONTROL
        avg = np.mean(data["amounts"]) if data["amounts"] else 0
        std = np.std(data["amounts"]) if data["amounts"] else 0

        if data["transactions"] > 100 and std < avg * 0.1:
            score *= 0.3

        if score > 5:
            suspicious.append({
                "account_id": node,
                "suspicion_score": round(min(score, 100), 2),
                "detected_patterns": sorted(list(data["patterns"])),
                "ring_id": sorted(list(data["ring_ids"]))[0] if data["ring_ids"] else ""
            })

    suspicious.sort(key=lambda x: x["suspicion_score"], reverse=True)

    return suspicious
