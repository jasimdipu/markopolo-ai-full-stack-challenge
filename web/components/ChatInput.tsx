"use client";

import { useState } from "react";

export default function ChatInput({ onSend }: { onSend: (text: string) => void }) {
  const [val, setVal] = useState("");
  return (
    <form
      onSubmit={(e) => { e.preventDefault(); const t = val.trim(); if (t) { onSend(t); setVal(""); } }}
      className="row"
    >
      <input
        value={val}
        onChange={(e) => setVal(e.target.value)}
        placeholder="Follow-up…"
        style={{ flex: 1, padding: "10px 12px", borderRadius: 10, border: "1px solid #2a2f36", background: "#0f1012" }}
      />
      <button type="submit" style={{ padding: "10px 12px", borderRadius: 10, border: "1px solid #2a2f36", background: "#15171a" }}>
        Send
      </button>
    </form>
  );
}
