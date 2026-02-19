import cytoscape from "cytoscape";
import { useEffect, useRef, useState } from "react";

/* ================================
   TYPES
================================ */

interface SuspiciousAccount {
  account_id: string;
  suspicion_score: number;
  detected_patterns: string[];
  ring_id: string;
}

interface FraudRing {
  ring_id: string;
  member_accounts: string[];
  pattern_type: string;
  risk_score: number;
}

interface GraphEdge {
  source: string;
  target: string;
}

interface GraphData {
  suspicious_accounts: SuspiciousAccount[];
  fraud_rings: FraudRing[];
  graph: {
    edges: GraphEdge[];
  };
}

/* ================================
   COMPONENT
================================ */

export default function GraphView({ data }: { data: GraphData }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const tooltipRef = useRef<HTMLDivElement>(null);
  const cyRef = useRef<cytoscape.Core | null>(null);

  const [selectedRing, setSelectedRing] = useState<string | null>(null);
  const [selectedNode, setSelectedNode] =
    useState<SuspiciousAccount | null>(null);

  useEffect(() => {
    if (!data || !containerRef.current) return;

    const suspiciousMap = new Map<string, SuspiciousAccount>(
      data.suspicious_accounts.map((a) => [a.account_id, a])
    );

    let edgesToRender = data.graph.edges;

    // ===============================
    // RING FILTER
    // ===============================
    if (selectedRing) {
      const ring = data.fraud_rings.find(
        (r) => r.ring_id === selectedRing
      );
      if (ring) {
        edgesToRender = data.graph.edges.filter(
          (e) =>
            ring.member_accounts.includes(e.source) &&
            ring.member_accounts.includes(e.target)
        );
      }
    }

    const nodeSet = new Set<string>();
    edgesToRender.forEach((e) => {
      nodeSet.add(e.source);
      nodeSet.add(e.target);
    });

    const elements: any[] = [];

    nodeSet.forEach((id) => {
      const suspicious = suspiciousMap.get(id);
      elements.push({
        data: {
          id,
          score: suspicious ? suspicious.suspicion_score : 0,
          patterns: suspicious
            ? suspicious.detected_patterns.join(", ")
            : "None",
          ring_id: suspicious ? suspicious.ring_id : "N/A",
        },
      });
    });

    edgesToRender.forEach((e, i) => {
      elements.push({
        data: {
          id: `edge-${i}`,
          source: e.source,
          target: e.target,
        },
      });
    });

    // Destroy previous instance safely
    if (cyRef.current) {
      cyRef.current.destroy();
    }

    const cy = cytoscape({
      container: containerRef.current,
      elements,
      style: [
        {
          selector: "node",
          style: {
            "background-color": "#94a3b8",
            width: 12,
            height: 12,
          },
        },
        {
          selector: "node[score > 0]",
          style: {
            "background-color": "#ef4444",
            width: "mapData(score, 0, 100, 18, 36)",
            height: "mapData(score, 0, 100, 18, 36)",
            "border-width": 2,
            "border-color": "#111",
          },
        },
        {
          selector: "edge",
          style: {
            width: 1.5,
            "line-color": "#64748b",
            "curve-style": "bezier",
            "target-arrow-shape": "triangle",
            "target-arrow-color": "#64748b",
            "arrow-scale": 1.4,
          },
        },
      ],
      layout: {
        name: "cose",
        idealEdgeLength: 140,
        nodeRepulsion: 900000,
        gravity: 0.25,
        animate: true,
      },
    });

    cyRef.current = cy;

    cy.minZoom(0.2);
    cy.maxZoom(3);

    const tooltip = tooltipRef.current!;

    // ===============================
    // HOVER TOOLTIP
    // ===============================
    cy.on("mouseover", "node", (evt) => {
      const node = evt.target;

      tooltip.innerHTML = `
        <div style="font-weight:bold;margin-bottom:4px;">${node.id()}</div>
        <div>Score: ${node.data("score")}</div>
        <div>Patterns: ${node.data("patterns")}</div>
        <div>Ring: ${node.data("ring_id")}</div>
      `;

      tooltip.style.display = "block";
    });

    cy.on("mousemove", (evt) => {
      tooltip.style.left = evt.originalEvent.pageX + 15 + "px";
      tooltip.style.top = evt.originalEvent.pageY + 15 + "px";
    });

    cy.on("mouseout", "node", () => {
      tooltip.style.display = "none";
    });

    // ===============================
    // CLICK NODE (FIXED)
    // ===============================
    cy.on("tap", "node", (evt) => {
      const suspicious = suspiciousMap.get(evt.target.id());
      setSelectedNode(suspicious || null);
    });

    // Click background → clear selection
    cy.on("tap", (evt) => {
      if (evt.target === cy) {
        setSelectedNode(null);
      }
    });

    return () => {
      cy.destroy();
    };
  }, [data, selectedRing]);

  return (
    <>
      {/* Graph */}
      <div
        ref={containerRef}
        style={{
          height: 650,
          borderRadius: 16,
          background: "#0f172a",
        }}
      />

      {/* Tooltip */}
      <div
        ref={tooltipRef}
        style={{
          position: "absolute",
          display: "none",
          background: "#111827",
          color: "white",
          padding: "10px 14px",
          borderRadius: "8px",
          fontSize: "12px",
          pointerEvents: "none",
          zIndex: 9999,
          boxShadow: "0 8px 20px rgba(0,0,0,0.4)",
        }}
      />

      {/* Ring Focus Buttons */}
      <div style={{ marginTop: 20 }}>
        <h3 style={{ marginBottom: 10 }}>Ring Focus Mode</h3>

        <button
          onClick={() => setSelectedRing(null)}
          style={{
            marginRight: 10,
            padding: "6px 14px",
            background: "#374151",
            color: "white",
            borderRadius: 8,
            border: "none",
            cursor: "pointer",
          }}
        >
          Global View
        </button>

        {data.fraud_rings.map((r) => (
          <button
            key={r.ring_id}
            onClick={() => setSelectedRing(r.ring_id)}
            style={{
              marginRight: 10,
              padding: "6px 14px",
              background: "#2563eb",
              color: "white",
              borderRadius: 8,
              border: "none",
              cursor: "pointer",
            }}
          >
            {r.ring_id}
          </button>
        ))}
      </div>

      {/* Clicked Node Panel */}
      {selectedNode && (
        <div
          style={{
            marginTop: 25,
            padding: 18,
            borderRadius: 12,
            background: "#111827",
            color: "white",
          }}
        >
          <h3 style={{ marginBottom: 10 }}>Account Details</h3>
          <p><b>ID:</b> {selectedNode.account_id}</p>
          <p><b>Suspicion Score:</b> {selectedNode.suspicion_score}</p>
          <p>
            <b>Patterns:</b>{" "}
            {selectedNode.detected_patterns.join(", ")}
          </p>
          <p><b>Ring ID:</b> {selectedNode.ring_id}</p>
        </div>
      )}
    </>
  );
}
