import ResultCard from "./ResultCard";

export default function MessageList({ frames }: { frames: any[] }) {
  return (
    <div className="col">
      {frames.map((f, i) => (
        <ResultCard key={i} frame={f} />
      ))}
    </div>
  );
}
