from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File

import pandas as pd
import time

from app.graph_builder import build_graph
from app.detectors.cycle_detector import detect_cycles
from app.detectors.smurf_detector import detect_smurf_rings
from app.detectors.shell_detector import detect_shells
from app.scoring import calculate_suspicion
from app.output_formatter import format_output

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    start_time = time.time()

    # -----------------------------
    # Load CSV
    # -----------------------------
    df = pd.read_csv(file.file)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # -----------------------------
    # Build Graph
    # -----------------------------
    G, node_stats = build_graph(df)

    # -----------------------------
    # Run All Detectors
    # -----------------------------
    fraud_rings = []

    # 1️⃣ Cycle detection
    cycle_rings = detect_cycles(G, df, node_stats)
    fraud_rings.extend(cycle_rings)

    # 2️⃣ Smurf detection
    smurf_rings = detect_smurf_rings(df)
    fraud_rings.extend(smurf_rings)

    # 3️⃣ Shell detection
    shell_rings = detect_shells(G, node_stats)
    fraud_rings.extend(shell_rings)

    # -----------------------------
    # Suspicion Scoring
    # -----------------------------
    suspicious_accounts = calculate_suspicion(
        G,
        node_stats,
        fraud_rings
    )

    processing_time = round(time.time() - start_time, 2)

    # -----------------------------
    # Final Output
    # -----------------------------
    return format_output(
        suspicious_accounts,
        fraud_rings,
        node_stats,
        processing_time,
        G
    )