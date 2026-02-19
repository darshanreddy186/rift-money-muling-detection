import networkx as nx
from collections import defaultdict
import statistics
from datetime import timedelta

MIN_RING_SIZE = 3
MAX_RING_SIZE = 5
MAX_TIME_WINDOW_HOURS = 72
MIN_RELATIVE_AMOUNT = 1.8      # was 2, slightly lowered
AMOUNT_PRESERVATION_TOL = 0.92  # at least 92% of amount should stay in cycle

def find_cycles_dfs(G, source, max_depth, visited_global, time_window_hours):
    """ Limited-depth DFS cycle finder from source, temporal constraint """
    def dfs(node, path, start_time):
        if len(path) > max_depth:
            return []

        cycles = []
        for neigh, data in G[node].items():
            if data.get('timestamp', None) is None:
                continue
            if (data['timestamp'] - start_time).total_seconds() / 3600 > time_window_hours:
                continue

            if neigh == path[0] and len(path) >= MIN_RING_SIZE:
                cycle = path + [neigh]
                cycles.append(tuple(cycle))
            elif neigh not in path:
                new_path = path + [neigh]
                cycles.extend(dfs(neigh, new_path, start_time))

        return cycles

    if source in visited_global:
        return []

    visited_global.add(source)
    start_time = min((d['timestamp'] for _, d in G[source].items()), default=None)
    if start_time is None:
        return []

    found = dfs(source, [source], start_time)

    # deduplicate rotationally
    unique = set()
    for c in found:
        c_rot = min(c[i:] + c[:i] for i in range(len(c)-1))
        unique.add(c_rot)

    return list(unique)


def detect_cycles(G, df, node_stats):
    rings = []
    ring_counter = 1

    all_amounts = [d['amount'] for u,v,d in G.edges(data=True) if 'amount' in d]
    median_amount = statistics.median(all_amounts) if all_amounts else 1.0

    visited = set()

    for node in list(G.nodes()):
        if node in visited:
            continue
        if G.out_degree(node) < 1 or G.in_degree(node) < 1:
            continue

        cycles = find_cycles_dfs(G, node, MAX_RING_SIZE, visited, MAX_TIME_WINDOW_HOURS)

        for cycle_tuple in cycles:
            cycle = list(cycle_tuple[:-1])  # remove duplicate closing node
            if len(cycle) < MIN_RING_SIZE or len(cycle) > MAX_RING_SIZE:
                continue

            # amount preservation check
            total_out = 0.0
            total_in  = 0.0
            timestamps = []

            valid = True
            for i in range(len(cycle)):
                a = cycle[i]
                b = cycle[(i+1) % len(cycle)]
                if not G.has_edge(a, b):
                    valid = False
                    break
                d = G[a][b]
                total_out += d.get('amount', 0)
                total_in  += d.get('amount', 0)  # in simple cycle should balance
                timestamps.append(d.get('timestamp'))

            if not valid or not timestamps:
                continue

            if (max(timestamps) - min(timestamps)) / timedelta(hours=1) > MAX_TIME_WINDOW_HOURS:
                continue

            if total_out == 0:
                continue

            relative = total_out / median_amount
            if relative < MIN_RELATIVE_AMOUNT:
                continue

            # stricter: amount should roughly preserve
            if min(total_out, total_in) / max(total_out, total_in + 1e-9) < AMOUNT_PRESERVATION_TOL:
                continue

            risk = min(100.0, 45 + relative * 8)

            ring_id = f"RING_C_{ring_counter:03d}"
            members = sorted(set(cycle))

            rings.append({
                "ring_id": ring_id,
                "member_accounts": members,
                "pattern_type": "cycle",
                "risk_score": round(risk, 2)
            })

            for acc in members:
                node_stats[acc].setdefault("patterns", set()).add(f"cycle_length_{len(members)}")
                node_stats[acc].setdefault("ring_ids", set()).add(ring_id)

            ring_counter += 1

            # mark all in cycle visited (avoid redundant work)
            visited.update(members)

    return rings