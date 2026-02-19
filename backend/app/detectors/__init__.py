from .cycle_detector import detect_cycles
from .smurf_detector import detect_smurf_rings
from .shell_detector import detect_shells


def detect_patterns(G, df, node_stats):
    rings = []

    # Cycle detection
    cycle_rings = detect_cycles(G, df, node_stats)
    rings.extend(cycle_rings)

    # Smurf detection
    smurf_rings = detect_smurf_rings(df)
    rings.extend(smurf_rings)

    # Shell detection
    shell_rings = detect_shells(G, node_stats)
    rings.extend(shell_rings)

    return rings
