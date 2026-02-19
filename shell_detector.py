def detect_shells(G, node_stats):
    rings = []
    ring_counter = 2000

    for node in list(G.nodes()):
        if node_stats[node].get("transactions", 0) > 4:  # stricter
            continue
        if G.out_degree(node) != 1 or G.in_degree(node) < 1:
            continue

        # follow unique successor chain
        chain = [node]
        curr = node
        seen = {node}

        while True:
            succ = list(G.successors(curr))
            if len(succ) != 1:
                break
            next_n = succ[0]
            if next_n in seen:
                break  # avoid self-loop or tiny cycle
            if node_stats[next_n].get("transactions", 0) > 4:
                break

            chain.append(next_n)
            seen.add(next_n)
            curr = next_n

            if len(chain) >= 4:  # stricter minimum
                # optional: check amounts are similar along chain
                amounts = []
                for i in range(len(chain)-1):
                    if not G.has_edge(chain[i], chain[i+1]):
                        break
                    am = G[chain[i]][chain[i+1]].get("amount", 0)
                    amounts.append(am)
                if len(amounts) == len(chain)-1 and min(amounts) > 0:
                    ratio = min(amounts) / max(amounts)
                    if ratio < 0.75:  # too much loss → not layering
                        break

                rings.append({
                    "ring_id": f"RING_L_{ring_counter}",
                    "member_accounts": chain[:],
                    "pattern_type": "layered_shell",
                    "risk_score": 78.0
                })
                ring_counter += 1
                break  # one chain per starting low-degree node

    return rings