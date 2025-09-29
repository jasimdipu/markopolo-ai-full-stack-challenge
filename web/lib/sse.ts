export async function streamSSE(
  url: string,
  signal: AbortSignal,
  onEvent: (data: any) => void
) {
  const resp = await fetch(url, { method: "GET", signal, headers: { Accept: "text/event-stream" } });
  if (!resp.ok || !resp.body) throw new Error(`HTTP ${resp.status}`);

  const reader = resp.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });

    const chunks = buffer.split("\n\n");
    for (const chunk of chunks.slice(0, -1)) {
      const line = chunk.split("\n").find((l) => l.startsWith("data:"));
      if (!line) continue;
      const jsonStr = line.slice(5).trim();
      try { onEvent(JSON.parse(jsonStr)); } catch { /* ignore */ }
    }
    buffer = chunks[chunks.length - 1];
  }
}
