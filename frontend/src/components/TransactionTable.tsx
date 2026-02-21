export default function TransactionTable({ transactions }: any) {

  return (
    <div style={{ marginTop: 20 }}>
      <h3>Transactions</h3>

      <table border={1} cellPadding={5}>
        <thead>
          <tr>
            <th>ID</th>
            <th>Sender</th>
            <th>Receiver</th>
            <th>Amount</th>
            <th>Timestamp</th>
          </tr>
        </thead>

        <tbody>
          {transactions.map((t: any) => (
            <tr key={t.transaction_id}>
              <td>{t.transaction_id}</td>
              <td>{t.sender_id}</td>
              <td>{t.receiver_id}</td>
              <td>{t.amount}</td>
              <td>{t.timestamp}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
