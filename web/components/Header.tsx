import Link from "next/link";

export default function Header() {
  return (
    <header className="container row" style={{ alignItems: "center", paddingTop: 10 }}>
      <Link href="/" className="row" style={{ gap: 8, alignItems: "center" }}>
        <div style={{ width: 28, height: 28, borderRadius: 8, background: "linear-gradient(120deg,#4f86ff,#8f6fff)" }} />
        <strong>Perplexity-style</strong>
      </Link>
      <nav style={{ marginLeft: "auto" }}>
        <Link className="muted" href="/q?q=what+is+vertex+ai">Demo</Link>
      </nav>
    </header>
  );
}
