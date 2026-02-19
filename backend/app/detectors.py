from collections import defaultdict
from datetime import timedelta
import statistics


# -------------------------------
# CONFIGURATION
# -------------------------------

MIN_RING_SIZE = 3
MAX_RING_SIZE = 5
FAN_THRESHOLD = 10
TIME_WINDOW_HOURS = 72
MIN_CHAIN_LENGTH = 3


# -------------------------------
# MAIN ENGINE
# -------------------------------

def money_mule_detection(G, node_stats):

    results = []

    # ---------------------------------
    # Precompute graph stats
    # ---------------------------------

    graph_out = defaultdict(list)
    graph_in = defaultdict(list)
    edge_data = {}

    for u, v, data in G.edges(data=True):
        graph_out[u].append(v)
        graph_in[v].append(u)
        edge_data[(u, v)] = data

    all_amounts = [d["amount"] for _, _, d in G.edges(data=True)]
    median_amount = statistics.median(all_amounts) if all_amounts else 0

    # ---------------------------------
    # 1️⃣ CIRCULAR FUND ROUTING
    # Strict 3–5 bounded expansion
    # ---------------------------------

    visited_cycles = set()

    for start in graph_out:

        for n2 in graph_out[start]:
            if n2 == start:
                continue

            for n3 in graph_out.get(n2, []):
                if n3 in (start, n2):
                    continue

                # 3-cycle
                if start in graph_out.get(n3, []):
                    cycle = normalize_cycle([start, n2, n3])
                    validate_and_store_cycle(
                        cycle, edge_data, median_amount,
                        visited_cycles, results, node_stats
                    )

                for n4 in graph_out.get(n3, []):
                    if n4 in (start, n2, n3):
                        continue

                    # 4-cycle
                    if start in graph_out.get(n4, []):
                        cycle = normalize_cycle([start, n2, n3, n4])
                        validate_and_store_cycle(
                            cycle, edge_data, median_amount,
                            visited_cycles, results, node_stats
                        )

                    for n5 in graph_out.get(n4, []):
                        if n5 in (start, n2, n3, n4):
                            continue

                        # 5-cycle
                        if start in graph_out.get(n5, []):
                            cycle = normalize_cycle(
                                [start, n2, n3, n4, n5]
                            )
                            validate_and_store_cycle(
                                cycle, edge_data, median_amount,
                                visited_cycles, results, node_stats
                            )

    # ---------------------------------
    # 2️⃣ SMURFING DETECTION
    # ---------------------------------

    for account in graph_in:

        incoming = graph_in[account]
        outgoing = graph_out.get(account, [])

        # FAN-IN
        if len(incoming) >= FAN_THRESHOLD:
            if validate_time_window(account, graph_in, edge_data):
                results.append({
                    "pattern": "fan_in",
                    "account": account
                })

        # FAN-OUT
        if len(outgoing) >= FAN_THRESHOLD:
            if validate_time_window(account, graph_out, edge_data):
                results.append({
                    "pattern": "fan_out",
                    "account": account
                })

    # ---------------------------------
    # 3️⃣ SHELL CHAIN DETECTION
    # ---------------------------------

    for start in graph_out:

        for mid in graph_out[start]:

            if is_shell_account(mid, graph_in, graph_out):

                for end in graph_out.get(mid, []):
                    if is_shell_account(end, graph_in, graph_out):

                        results.append({
                            "pattern": "layered_shell",
                            "chain": [start, mid, end]
                        })

    return results


# -------------------------------
# HELPERS
# -------------------------------

def normalize_cycle(cycle):
    cycle = list(cycle)
    min_node = min(cycle)
    while cycle[0] != min_node:
        cycle = cycle[1:] + cycle[:1]
    return tuple(cycle)


def validate_and_store_cycle(
    cycle, edge_data, median_amount,
    visited_cycles, results, node_stats
):
    if cycle in visited_cycles:
        return

    total = 0
    timestamps = []

    for i in range(len(cycle)):
        u = cycle[i]
        v = cycle[(i+1) % len(cycle)]
        data = edge_data.get((u, v))
        if not data:
            return
        total += data["amount"]
        timestamps.append(data["timestamp"])

    if not timestamps:
        return

    if (max(timestamps) - min(timestamps)).total_seconds() > 72*3600:
        return

    if median_amount == 0:
        return

    if total / median_amount < 2:
        return

    visited_cycles.add(cycle)

    results.append({
        "pattern": "cycle",
        "members": list(cycle)
    })


def validate_time_window(account, graph_dir, edge_data):
    timestamps = []
    for neighbor in graph_dir[account]:
        data = edge_data.get((neighbor, account)) or edge_data.get((account, neighbor))
        if data:
            timestamps.append(data["timestamp"])
    if not timestamps:
        return False
    return (max(timestamps) - min(timestamps)).total_seconds() <= 72*3600


def is_shell_account(acc, graph_in, graph_out):
    total_tx = len(graph_in.get(acc, [])) + len(graph_out.get(acc, []))
    return 1 <= total_tx <= 3
