"use client";

import { useRouter } from "next/navigation";
import { useEffect, useRef, useState } from "react";

export default function SearchBar({ initialQuery = "", autoFocus = false }: { initialQuery?: string; autoFocus?: boolean }) {
  const [q, setQ] = useState(initialQuery);
  const r = useRouter();
  const ref = useRef<HTMLInputElement>(null);
  useEffect(() => { if (autoFocus) ref.current?.focus(); }, [autoFocus]);

  return (
    <form
      onSubmit={(e) => { e.preventDefault(); if (q.trim()) r.push(`/q?q=${encodeURIComponent(q.trim())}`); }}
      className="row"
    >
      <input
        ref={ref}
        value={q}
        onChange={(e) => setQ(e.target.value)}
        placeholder="Ask anything…"
        aria-label="Search"
        style={{ flex: 1, padding: "12px 14px", borderRadius: 12, border: "1px solid #2a2f36", background: "#0f1012", color: "inherit" }}
      />
      <button type="submit" style={{ padding: "12px 16px", borderRadius: 10, border: "1px solid #2a2f36", background: "#15171a" }}>
        Search
      </button>
    </form>
  );
}
