import cytoscape from "cytoscape";
import { useEffect, useRef } from "react";

export default function CaseGraph({ caseData }: any) {

  const container = useRef<HTMLDivElement>(null);

  useEffect(() => {

    const elements: any[] = [];

    const nodeSet = new Set<string>();

    caseData.transactions.forEach((t: any) => {
      nodeSet.add(t.sender_id);
      nodeSet.add(t.receiver_id);
    });

    nodeSet.forEach(id => {
      elements.push({ data: { id } });
    });

    caseData.transactions.forEach((t: any, index: number) => {
      elements.push({
        data: {
          id: `edge-${index}`,
          source: t.sender_id,
          target: t.receiver_id
        }
      });
    });

    const cy = cytoscape({
      container: container.current,
      elements,
      style: [
        {
          selector: "node",
          style: {
            "background-color": "#ef4444",
            "label": "data(id)",
            "color": "#fff",
            "text-valign": "center"
          }
        },
        {
          selector: "edge",
          style: {
            "line-color": "#999",
            "target-arrow-color": "#999",
            "target-arrow-shape": "triangle"
          }
        }
      ],
      layout: { name: "cose" }
    });

    return () => cy.destroy();

  }, [caseData]);

  return <div ref={container} style={{ height: 400 }} />;
}
