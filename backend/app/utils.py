def generate_output(accounts, cycles, smurf, shells, total, time, graph):

    rings = cycles + smurf + shells

    fraud_rings = []

    for r in rings:
        fraud_rings.append({
            "ring_id": r["ring_id"],
            "member_accounts": r["members"],
            "pattern_type": r["pattern_type"],
            "risk_score": 95.0
        })

    edges = []
    for u, v in graph.edges():
        edges.append({"source": u, "target": v})

    return {
        "suspicious_accounts": accounts,
        "fraud_rings": fraud_rings,
        "graph": {
            "edges": edges
        },
        "summary": {
            "total_accounts_analyzed": total,
            "suspicious_accounts_flagged": len(accounts),
            "fraud_rings_detected": len(fraud_rings),
            "processing_time_seconds": time
        }
    }
