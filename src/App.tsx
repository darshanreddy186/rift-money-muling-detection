import { useState } from "react";
import FileUpload from "./components/FileUpload";
import GraphView from "./components/GraphView";
import RingTable from "./components/RingTable";

export default function App() {
  const [data, setData] = useState<any>(null);

  return (
    <div className="relative min-h-screen bg-[#0b0f19] text-white overflow-hidden">

      {/* ===== Floating Background Blobs ===== */}
      <div className="absolute top-[-150px] left-[-150px] w-[500px] h-[500px] bg-indigo-600/30 rounded-full blur-[120px]" />
      <div className="absolute bottom-[-200px] right-[-200px] w-[600px] h-[600px] bg-purple-600/30 rounded-full blur-[150px]" />

      {/* ================= HEADER ================= */}
      <header className="sticky top-0 z-50 backdrop-blur-xl bg-white/5 border-b border-white/10 px-10 py-6 flex justify-between items-center">
        <h1 className="text-2xl font-semibold tracking-wide">
          🕵️ Financial Forensics Engine
        </h1>
        <span className="text-sm text-gray-400">
          RIFT 2026 • Graph Intelligence Track
        </span>
      </header>

      {/* ================= HERO ================= */}
      <section className="text-center py-20 px-6">
        <h2 className="text-6xl font-extrabold bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">
          Intelligence-Driven Fraud Detection
        </h2>

        <p className="mt-6 text-gray-400 max-w-3xl mx-auto text-lg leading-relaxed">
          Advanced graph theory, temporal analytics and adaptive risk scoring
          to uncover smurfing networks, circular routing and shell chains
          across financial ecosystems.
        </p>

        <div className="mt-10 flex justify-center">
          <div className="backdrop-blur-xl bg-white/5 border border-white/10 p-10 rounded-3xl shadow-2xl w-full max-w-3xl">
            <FileUpload setData={setData} />
          </div>
        </div>
      </section>

      {/* ================= RESULTS ================= */}
      {data && (
        <>
          {/* ===== Stats Section ===== */}
          <section className="grid grid-cols-1 md:grid-cols-4 gap-8 px-16 mb-20">

            <StatCard
              title="Total Accounts"
              value={data.summary.total_accounts_analyzed}
            />

            <StatCard
              title="Suspicious Accounts"
              value={data.summary.suspicious_accounts_flagged}
              highlight
            />

            <StatCard
              title="Fraud Rings"
              value={data.summary.fraud_rings_detected}
              highlight
            />

            <StatCard
              title="Processing Time (s)"
              value={data.summary.processing_time_seconds}
            />
          </section>

          {/* ===== Graph ===== */}
          <section className="px-16 mb-24">
            <div className="backdrop-blur-xl bg-white/5 border border-white/10 rounded-3xl p-10 shadow-2xl">
              <h3 className="text-2xl font-semibold mb-8 text-indigo-300">
                Transaction Network Intelligence Map
              </h3>
              <GraphView data={data} />
            </div>
          </section>

          {/* ===== Ring Table ===== */}
          <section className="px-16 mb-20">
            <div className="backdrop-blur-xl bg-white/5 border border-white/10 rounded-3xl p-10 shadow-2xl">
              <h3 className="text-2xl font-semibold mb-8 text-purple-300">
                Fraud Ring Intelligence Summary
              </h3>
              <RingTable rings={data.fraud_rings} />
            </div>
          </section>

          {/* ===== Download ===== */}
          <section className="text-center mb-20">
            <a
              href={`data:text/json;charset=utf-8,${encodeURIComponent(
                JSON.stringify(data, null, 2)
              )}`}
              download="analysis_output.json"
              className="inline-block bg-gradient-to-r from-indigo-600 to-purple-600 hover:scale-105 transition-transform duration-300 px-10 py-4 rounded-2xl font-semibold shadow-xl"
            >
              ⬇ Download Intelligence Report
            </a>
          </section>
        </>
      )}

      {/* ================= FOOTER ================= */}
      <footer className="text-center py-10 border-t border-white/10 text-gray-400 text-sm backdrop-blur-xl bg-white/5">
        Built for RIFT 2026 Hackathon • Graph-Based Financial Crime Detection • © 2026
      </footer>
    </div>
  );
}


/* ================= STAT CARD ================= */

function StatCard({
  title,
  value,
  highlight = false
}: {
  title: string;
  value: number;
  highlight?: boolean;
}) {
  return (
    <div
      className={`p-8 rounded-3xl backdrop-blur-xl border border-white/10 shadow-xl transition duration-300 hover:scale-105
      ${highlight ? "bg-gradient-to-br from-indigo-600/20 to-purple-600/20" : "bg-white/5"}`}
    >
      <p className="text-gray-400 text-sm tracking-wide">{title}</p>
      <h2 className="text-4xl font-bold mt-3">{value}</h2>
    </div>
  );
}
