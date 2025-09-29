import { NextRequest } from "next/server";
export const runtime = "edge";

export async function POST(req: NextRequest) {
  const API_BASE = (process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8080").replace(/\/+$/,"");
  const body = await req.text();
  const resp = await fetch(`${API_BASE}/plan`, {
    method: "POST",
    headers: { "Accept": "text/event-stream", "Content-Type": "application/json" },
    body
  });
  return new Response(resp.body, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      "Connection": "keep-alive"
    }
  });
}
