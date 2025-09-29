"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import { streamSSEPost } from "../../lib/sse";
import { formatTime } from "../../lib/fmt";
import SearchBar from "../../components/SearchBar";
import MessageList from "../../components/MessageList";
import SidePanel from "../../components/SidePanel";
import LoadingSkeleton from "../../components/LoadingSkeleton";
import ErrorState from "../../components/ErrorState";

const API_BASE = (process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8080").replace(/\/+$/,"");

export default function QueryPage({ searchParams }: { searchParams: { q?: string } }) {
  const q = (searchParams.q || "").trim();
  const [frames, setFrames] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [startedAt] = useState(() => Date.now());
  const abortRef = useRef<AbortController | null>(null);

  const start = useMemo(() => async (goal: string) => {
    setFrames([]);
    setError(null);
    abortRef.current?.abort();
    const ac = new AbortController();
    abortRef.current = ac;

    try {
      await streamSSEPost(`${API_BASE}/plan`, { goal }, ac.signal, (evt) => {
        // support server sending {step, payload} or {frame: "..."} etc.
        const normalized = evt.step ? evt : (evt.frame ? evt.frame : evt);
        setFrames((prev) => [...prev, normalized]);
      });
    } catch (e: any) {
      setError(e?.message || "Failed to fetch");
    }
  }, []);

  useEffect(() => {
    if (q) start(q);
    return () => abortRef.current?.abort();
  }, [q, start]);

  return (
    <main className="row" style={{ alignItems: "flex-start" }}>
      <section style={{ flex: 1, minWidth: 0 }} className="col">
        <SearchBar initialQuery={q} />
        {!q ? <div className="muted">Type a question above.</div> : null}
        {error ? <ErrorState message={error} /> : null}
        {!error && frames.length === 0 && q ? <LoadingSkeleton /> : null}
        <MessageList frames={frames} />
        <div className="muted mono" style={{ marginTop: 8 }}>
          {frames.length} frames • {formatTime(Date.now() - startedAt)}
        </div>
      </section>
      <aside style={{ width: 300 }}>
        <SidePanel frames={frames} />
      </aside>
    </main>
  );
}
