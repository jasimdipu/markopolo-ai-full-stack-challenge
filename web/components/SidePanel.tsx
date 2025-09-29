export default function SidePanel({ frames }: { frames: any[] }) {
  const messages = frames.filter(f => f.step === "messages")?.[0]?.payload?.templates ?? [];
  const schedule = frames.filter(f => f.step === "schedule")?.[0]?.payload ?? null;

  return (
    <div className="card col" style={{ padding: 12, position: "sticky", top: 16 }}>
      <strong>Summary</strong>
      <div className="hr" />
      <div>
        <div className="muted" style={{ marginBottom: 6 }}>Templates</div>
        <ul style={{ margin: 0, paddingLeft: 18 }}>
          {messages.map((m: any, i: number) => (
            <li key={i} className="mono" style={{ fontSize: 12 }}>{m.channel}:{m.variant}</li>
          ))}
          {messages.length === 0 && <div className="muted">No templates yet</div>}
        </ul>
      </div>
      <div className="hr" />
      <div>
        <div className="muted" style={{ marginBottom: 6 }}>Schedule</div>
        <pre className="mono" style={{ whiteSpace: "pre-wrap", margin: 0 }}>
          {schedule ? JSON.stringify(schedule, null, 2) : "—"}
        </pre>
      </div>
    </div>
  );
}
