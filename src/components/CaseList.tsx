export default function CaseList({ cases, onSelect }: any) {

  return (
    <div style={{ marginTop: 20 }}>
      <h3>Detected Cases</h3>

      {cases.length === 0 && <p>No suspicious cases detected</p>}

      {cases.map((c: any) => (
        <div
          key={c.case_id}
          style={{
            border: "1px solid #ccc",
            padding: 10,
            marginTop: 10,
            cursor: "pointer"
          }}
          onClick={() => onSelect(c)}
        >
          <strong>{c.case_id}</strong>
          <p>{c.pattern_type}</p>
          <p>Risk: {c.risk_score}</p>
        </div>
      ))}
    </div>
  );
}
