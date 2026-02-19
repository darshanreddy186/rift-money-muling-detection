from collections import defaultdict
import pandas as pd
from datetime import timedelta

WINDOW = timedelta(hours=72)
MIN_UNIQUE_FAN = 8          # lowered slightly, but still meaningful
MIN_TX_PER_HUB = 12
HUB_LIFESPAN_DAYS_THRESH = 45

def detect_smurf_rings(df: pd.DataFrame):
    if len(df) == 0:
        return []

    df = df.sort_values("timestamp").copy()
    df["ts"] = df["timestamp"]

    senders = df["sender_id"].value_counts()
    receivers = df["receiver_id"].value_counts()

    potential_hubs = set(
        senders[senders >= MIN_TX_PER_HUB].index
    ) | set(
        receivers[receivers >= MIN_TX_PER_HUB].index
    )

    if not potential_hubs:
        return []

    tx_by_account = defaultdict(list)
    for _, row in df.iterrows():
        tx_by_account[row["sender_id"]].append(row)
        tx_by_account[row["receiver_id"]].append(row)

    rings = []
    ring_counter = 1

    for hub in potential_hubs:
        incoming = [r for r in tx_by_account[hub] if r["receiver_id"] == hub]
        outgoing = [r for r in tx_by_account[hub] if r["sender_id"] == hub]

        if len(incoming) < MIN_UNIQUE_FAN or len(outgoing) < MIN_UNIQUE_FAN:
            continue

        inc_df = pd.DataFrame(incoming).sort_values("ts")
        out_df = pd.DataFrame(outgoing).sort_values("ts")

        # sliding window unique senders → receivers
        def max_unique_in_window(dff, key_col):
            if len(dff) < MIN_UNIQUE_FAN:
                return 0, (0,0)
            dff = dff.reset_index(drop=True)
            left = 0
            cnt = defaultdict(int)
            uniq = 0
            max_u = 0
            best = (0,0)

            for right in range(len(dff)):
                k = dff.at[right, key_col]
                cnt[k] += 1
                if cnt[k] == 1:
                    uniq += 1

                while dff.at[right, "ts"] - dff.at[left, "ts"] > WINDOW and left <= right:
                    kl = dff.at[left, key_col]
                    cnt[kl] -= 1
                    if cnt[kl] == 0:
                        uniq -= 1
                    left += 1

                if uniq > max_u:
                    max_u = uniq
                    best = (left, right)

            return max_u, best

        uniq_in, (l_in, r_in) = max_unique_in_window(inc_df, "sender_id")
        if uniq_in < MIN_UNIQUE_FAN:
            continue

        end_ts = inc_df.iloc[r_in]["ts"]

        out_after = out_df[out_df["ts"] >= end_ts - timedelta(hours=6)]  # allow small lag
        if len(out_after) < MIN_UNIQUE_FAN:
            continue

        uniq_out, (l_out, r_out) = max_unique_in_window(out_after, "receiver_id")
        if uniq_out < MIN_UNIQUE_FAN:
            continue

        # simple lifespan filter
        lifespan = (df["ts"].max() - df["ts"].min()).days if len(df) > 0 else 0
        if lifespan > HUB_LIFESPAN_DAYS_THRESH * 1.5:  # long-lived → probably normal
            continue

        # collect members
        in_senders = set(inc_df.iloc[l_in:r_in+1]["sender_id"])
        out_receivers = set(out_after.iloc[l_out:r_out+1]["receiver_id"])

        members = {hub} | in_senders | out_receivers

        score = min(100, 55 + (uniq_in + uniq_out) * 1.1)

        rings.append({
            "ring_id": f"RING_S_{ring_counter:03d}",
            "member_accounts": sorted(members),
            "pattern_type": "fan_in_fan_out",
            "risk_score": round(score, 2)
        })
        ring_counter += 1

    return rings