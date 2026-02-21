import axios from "axios";

export const analyzeCSV = async (file: File) => {
  const formData = new FormData();
  formData.append("file", file);

  const res = await axios.post("http://localhost:8000/analyze", formData);
  return res.data;
};
