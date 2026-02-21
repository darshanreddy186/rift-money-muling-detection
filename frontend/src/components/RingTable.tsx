export default function RingTable({ rings }: { rings: any[] }) {
  return (
    <div className="overflow-x-auto rounded-2xl">

      <table className="w-full text-left border-collapse">

        <thead>
          <tr className="text-gray-400 text-sm uppercase tracking-wider border-b border-white/10">
            <th className="py-4">Ring ID</th>
            <th>Pattern</th>
            <th>Members</th>
            <th>Risk Score</th>
          </tr>
        </thead>

        <tbody>
          {rings.map((ring, index) => (
            <tr
              key={index}
              className="border-b border-white/5 hover:bg-white/5 transition duration-300"
            >
              <td className="py-4 font-semibold text-indigo-300">
                {ring.ring_id}
              </td>

              <td className="text-gray-300">
                {ring.pattern_type}
              </td>

              <td className="text-gray-300">
                {ring.member_accounts.length}
              </td>

              <td>
                <span className="px-4 py-1 rounded-full bg-gradient-to-r from-red-500/20 to-pink-500/20 text-red-400 text-sm font-medium">
                  {ring.risk_score}
                </span>
              </td>
            </tr>
          ))}
        </tbody>

      </table>
    </div>
  );
}
