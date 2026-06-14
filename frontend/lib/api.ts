import { ApiResponse } from "@/types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function sendMessage(
  query: string,
  sessionId: string | null
): Promise<ApiResponse> {
  const payload: Record<string, string> = { query };
  if (sessionId) {
    payload.session_key = sessionId;
  }

  const res = await fetch(`${API_BASE_URL}/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const errorText = await res.text().catch(() => "Unknown error");
    throw new Error(`API error ${res.status}: ${errorText}`);
  }

  return res.json() as Promise<ApiResponse>;
}

/** Extract the best text content from the API response */
export function extractResponseText(data: ApiResponse): string {
  return (
    data.message ??
    JSON.stringify(data, null, 2)
  );
}

/** Check if the session should be closed based on the API response */
export function isSessionResolved(data: ApiResponse): boolean {
  if (!data.refund) return false;
  const v = data.refund.toString().toLowerCase();
  return v === "approved" || v === "denied" || v === "escalate";
}
