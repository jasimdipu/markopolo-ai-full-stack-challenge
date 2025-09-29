import SourceChip from "./SourceChip";

export default function ResultCard({ frame }: { frame: any }) {
  const step = frame.step ?? "frame";
  const payload = frame.payload ?? frame.artifact ?? frame;

  return (
    <article className="card" style={{ padding: 14 }}>
      <div className="row" style={{ justifyContent: "space-between" }}>
        <div className="muted mono" style={{ textTransform: "uppercase" }}>{step}</div>
        <div className="row" style={{ gap: 6 }}>
          {(payload?.sources ?? []).slice(0, 4).map((s: any, idx: number) => (
            <SourceChip key={idx} href={s.url} label={s.domain || s.url} />
          ))}
        </div>
      </div>
      <div className="hr" />
      <pre className="mono" style={{ whiteSpace: "pre-wrap", margin: 0, overflowX: "auto" }}>
        {typeof payload === "string" ? payload : JSON.stringify(payload, null, 2)}
      </pre>
    </article>
  );
}
