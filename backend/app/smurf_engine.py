from collections import defaultdict
from datetime import timedelta

WINDOW_HOURS = 72
MIN_UNIQUE = 10


def detect_smurf_rings(df):

    transactions_by_sender = defaultdict(list)
    transactions_by_receiver = defaultdict(list)
    degree_in = defaultdict(int)
    degree_out = defaultdict(int)
    first_seen = {}
    last_seen = {}

    for _, row in df.iterrows():
        sender = row["sender_id"]
        receiver = row["receiver_id"]

        tx = {
            "sender": sender,
            "receiver": receiver,
            "amount": float(row["amount"]),
            "timestamp": row["timestamp"]
        }

        transactions_by_sender[sender].append(tx)
        transactions_by_receiver[receiver].append(tx)

        degree_out[sender] += 1
        degree_in[receiver] += 1

        if sender not in first_seen:
            first_seen[sender] = row["timestamp"]
        if receiver not in first_seen:
            first_seen[receiver] = row["timestamp"]

        last_seen[sender] = row["timestamp"]
        last_seen[receiver] = row["timestamp"]

    window_delta = timedelta(hours=WINDOW_HOURS)
    rings = []
    processed_accounts = set()

    for aggregator, incoming_txs in transactions_by_receiver.items():

        if len(incoming_txs) < MIN_UNIQUE:
            continue

        incoming_txs = sorted(incoming_txs, key=lambda x: x["timestamp"])
        left = 0
        unique_senders = set()

        for right in range(len(incoming_txs)):
            unique_senders.add(incoming_txs[right]["sender"])

            while incoming_txs[right]["timestamp"] - incoming_txs[left]["timestamp"] > window_delta:
                unique_senders.discard(incoming_txs[left]["sender"])
                left += 1

            if len(unique_senders) >= MIN_UNIQUE:

                outgoing_txs = transactions_by_sender.get(aggregator, [])
                outgoing_txs = sorted(outgoing_txs, key=lambda x: x["timestamp"])

                left_out = 0
                unique_receivers = set()

                for r in range(len(outgoing_txs)):
                    unique_receivers.add(outgoing_txs[r]["receiver"])

                    while outgoing_txs[r]["timestamp"] - outgoing_txs[left_out]["timestamp"] > window_delta:
                        unique_receivers.discard(outgoing_txs[left_out]["receiver"])
                        left_out += 1

                    if len(unique_receivers) >= MIN_UNIQUE:

                        lifespan_days = (last_seen[aggregator] - first_seen[aggregator]).days
                        total_degree = degree_in[aggregator] + degree_out[aggregator]

                        suppress = False

                        if total_degree > 150:
                            suppress = True

                        if lifespan_days > 20:
                            suppress = True

                        if len(outgoing_txs) >= 50:
                            timestamps = sorted([tx["timestamp"] for tx in outgoing_txs])
                            time_span = (timestamps[-1] - timestamps[0]).total_seconds() / 3600
                            amounts = [tx["amount"] for tx in outgoing_txs]
                            if time_span < 5 and (max(amounts) - min(amounts)) > 20000:
                                suppress = True

                        if not suppress and aggregator not in processed_accounts:

                            ring_members = set()
                            ring_members.add(aggregator)
                            ring_members.update(unique_senders)
                            ring_members.update(unique_receivers)

                            rings.append(list(ring_members))
                            processed_accounts.add(aggregator)

                        break
                break

    return rings
