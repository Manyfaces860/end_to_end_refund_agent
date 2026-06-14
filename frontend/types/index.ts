export type MessageRole = "user" | "agent";

export interface Message {
  id: string;
  role: MessageRole;
  content: string;
  timestamp: Date;
}

export type SessionStatus = "approved" | "denied" | "escalate" | "pending";

export interface Session {
  id: string; // local UUID — always present
  sessionId: string | null; // server-assigned session_id — null until first API round-trip
  title: string;
  status: SessionStatus;
  messages: Message[];
  createdAt: Date;
  updatedAt: Date;
  resolvedKey?: string; // value of `refund` key if returned, e.g. "resolved"
}

export interface ApiResponse {
  message?: string;
  session_key?: string;
  refund?: string;
}
