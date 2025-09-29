export default function SourceChip({ href, label }: { href: string; label: string }) {
  return (
    <a href={href} target="_blank" rel="noreferrer"
       className="muted mono"
       style={{ padding: "4px 8px", border: "1px solid #2a2f36", borderRadius: 8 }}>
      {label}
    </a>
  );
}
