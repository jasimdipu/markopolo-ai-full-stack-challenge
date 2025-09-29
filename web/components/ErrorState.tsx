export default function ErrorState({ message }: { message: string }) {
  return (
    <div className="card" style={{ padding: 14, borderColor: "#432222" }}>
      <strong style={{ color: "#ff6b6b" }}>Error</strong>
      <div className="hr" />
      <div className="mono">{message}</div>
    </div>
  );
}
