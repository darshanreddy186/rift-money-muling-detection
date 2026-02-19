export default function DownloadButton({ data }: any) {

  const download = () => {
    const blob = new Blob(
      [JSON.stringify(data, null, 2)],
      { type: "application/json" }
    );
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "financial_forensics_output.json";
    a.click();
  };

  return (
    <button onClick={download} style={{ marginTop: 20 }}>
      Download JSON Report
    </button>
  );
}
