export default function LoadingSkeleton() {
  return (
    <div className="card" style={{ padding: 14 }}>
      <div className="muted">Streaming…</div>
      <div style={{ height: 8 }} />
      <div style={{ height: 8, background: "#1a1d22", borderRadius: 6 }} />
      <div style={{ height: 8, background: "#1a1d22", borderRadius: 6, marginTop: 6, width: "80%" }} />
      <div style={{ height: 8, background: "#1a1d22", borderRadius: 6, marginTop: 6, width: "60%" }} />
    </div>
  );
}
