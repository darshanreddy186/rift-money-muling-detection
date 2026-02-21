import { analyzeCSV } from "../api";

export default function FileUpload({ setData }: any) {

  const handleUpload = async (e: any) => {
    const file = e.target.files[0];
    const result = await analyzeCSV(file);
    setData(result);
  };

  return <input type="file" accept=".csv" onChange={handleUpload} />;
}
