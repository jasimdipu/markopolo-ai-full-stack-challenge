export async function streamSSEGet(
  url: string,
  signal: AbortSignal,
  onEvent: (data: any) => void
) {
  const resp = await fetch(url, { method: "GET", signal, headers: { Accept: "text/event-stream" } });
  if (!resp.ok || !resp.body) throw new Error(`HTTP ${resp.status}`);
  await readStream(resp.body, onEvent);
}

export async function streamSSEPost(
  url: string,
  body: Record<string, unknown>,
  signal: AbortSignal,
  onEvent: (data: any) => void
) {
  const resp = await fetch(url, {
    method: "POST",
    signal,
    headers: {
      "Accept": "text/event-stream",
      "Content-Type": "application/json"
    },
    body: JSON.stringify(body)
  });
  if (!resp.ok || !resp.body) throw new Error(`HTTP ${resp.status}`);
  await readStream(resp.body, onEvent);
}

async function readStream(stream: ReadableStream<Uint8Array>, onEvent: (data: any) => void) {
  const reader = stream.getReader();
  const decoder = new TextDecoder();
  let buffer = "";
  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
    buffer += decoder.decode(value, { stream: true });

    const chunks = buffer.split("\n\n");
    for (const chunk of chunks.slice(0, -1)) {
      // tolerate both "data: {...}" and raw JSON lines
      const line = chunk.split("\n").find(l => l.startsWith("data:")) ?? chunk;
      const jsonStr = line.startsWith("data:") ? line.slice(5).trim() : line.trim();
      if (!jsonStr) continue;
      try { onEvent(JSON.parse(jsonStr)); } catch { /* ignore non-JSON */ }
    }
    buffer = chunks[chunks.length - 1];
  }
}
