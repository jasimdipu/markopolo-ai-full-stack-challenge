import SearchBar from "@/components/SearchBar";

export default function Home() {
  return (
    <main className="col" style={{ marginTop: 48, alignItems: "center" }}>
      <h1 style={{ fontSize: 28, fontWeight: 700, marginBottom: 8 }}>Ask anything</h1>
      <p className="muted" style={{ marginBottom: 18 }}>Perplexity-style streaming results</p>
      <div style={{ width: "min(760px, 100%)" }}>
        <SearchBar autoFocus />
      </div>
    </main>
  );
}
