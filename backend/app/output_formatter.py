def format_output(suspicious_accounts, fraud_rings, node_stats, processing_time, G):

    edges = []
    for u, v in G.edges():
        edges.append({
            "source": u,
            "target": v,
            "amount": G[u][v]["amount"],
    "timestamp": str(G[u][v]["timestamp"])
        })

    return {
        "suspicious_accounts": suspicious_accounts,
        "fraud_rings": fraud_rings,
        "graph": {
            "edges": edges
        },
        "summary": {
            "total_accounts_analyzed": len(node_stats),
            "suspicious_accounts_flagged": len(suspicious_accounts),
            "fraud_rings_detected": len(fraud_rings),
            "processing_time_seconds": processing_time
        }
    }
