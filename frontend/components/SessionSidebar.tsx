"use client";

import { Session } from "@/types";
import { Plus, MessageCircle, CheckCircle2, Clock } from "lucide-react";
import clsx from "clsx";

interface SessionSidebarProps {
  sessions: Session[];
  activeSessionId: string | null;
  onSelectSession: (id: string) => void;
  onCreateSession: () => void;
}

function formatTime(date: Date): string {
  const now = new Date();
  const diff = now.getTime() - date.getTime();
  if (diff < 60000) return "just now";
  if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`;
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}h ago`;
  return date.toLocaleDateString("en-IN", { day: "numeric", month: "short" });
}

export default function SessionSidebar({
  sessions,
  activeSessionId,
  onSelectSession,
  onCreateSession,
}: SessionSidebarProps) {
  return (
    <aside className="flex flex-col h-full bg-paper border-r border-mist w-full">
      {/* Header */}
      <div className="px-5 pt-6 pb-4 border-b border-mist">
        <div className="flex items-center justify-between mb-1">
          <span className="font-display text-xl text-ink tracking-tight">Support</span>
          <span className="text-xs font-mono text-dim bg-mist px-2 py-0.5 rounded-full">
            {sessions.length} {sessions.length === 1 ? "session" : "sessions"}
          </span>
        </div>
        <p className="text-xs text-dim">Customer support conversations</p>
      </div>

      {/* New Session Button */}
      <div className="px-4 pt-4 pb-2">
        <button
          onClick={onCreateSession}
          className="w-full flex items-center justify-center gap-2 bg-accent text-ivory text-sm font-medium px-4 py-2.5 rounded-xl hover:bg-accent-light transition-all duration-200 shadow-sm hover:shadow-md active:scale-[0.98]"
        >
          <Plus size={15} strokeWidth={2.5} />
          New Session
        </button>
      </div>

      {/* Session List */}
      <div className="flex-1 overflow-y-auto px-3 pb-4 space-y-1.5 mt-2">
        {sessions.length === 0 && (
          <div className="flex flex-col items-center justify-center pt-12 gap-3 text-center px-4">
            <div className="w-12 h-12 rounded-2xl bg-mist flex items-center justify-center">
              <MessageCircle size={20} className="text-ash" />
            </div>
            <p className="text-sm text-dim leading-relaxed">
              No sessions yet. Create one to get started.
            </p>
          </div>
        )}
        {sessions.map((session) => {
          const isActive = session.id === activeSessionId;
          const lastMsg = session.messages[session.messages.length - 1];
          const isResolved = session?.status === "approved" || session?.status === "denied" || session?.status === 'escalate';

          return (
            <button
              key={session.id}
              onClick={() => onSelectSession(session.id)}
              className={clsx(
                "w-full text-left px-3.5 py-3 rounded-xl transition-all duration-200 group animate-slide-in-left",
                isActive
                  ? "bg-ink text-ivory shadow-sm"
                  : "hover:bg-session-bg text-ink"
              )}
            >
              <div className="flex items-start justify-between gap-2">
                <div className="flex items-center gap-2 min-w-0">
                  <div className={clsx(
                    "w-2 h-2 rounded-full flex-shrink-0 mt-0.5",
                    isResolved ? "bg-resolved" :
                    isActive ? "bg-accent-light" : "bg-accent"
                  )} />
                  <span className={clsx(
                    "text-sm font-medium truncate",
                    isActive ? "text-ivory" : "text-ink"
                  )}>
                    {session.title}
                  </span>
                </div>
                <div className="flex items-center gap-1 flex-shrink-0">
                  {isResolved ? (
                    <CheckCircle2 size={13} className={clsx(isActive ? "text-teal-light" : "text-resolved")} />
                  ) : (
                    <Clock size={13} className={clsx(isActive ? "text-ash" : "text-dim")} />
                  )}
                </div>
              </div>

              {lastMsg && (
                <p className={clsx(
                  "text-xs mt-1.5 truncate pl-4",
                  isActive ? "text-ash" : "text-dim"
                )}>
                  {lastMsg.role === "user" ? "You: " : "Agent: "}
                  {lastMsg.content}
                </p>
              )}

              <div className="flex items-center justify-between pl-4 mt-1.5">
                <span className={clsx(
                  "text-[10px] font-mono",
                  isActive ? "text-ash" : "text-dim"
                )}>
                  {formatTime(session.updatedAt)}
                </span>
                {isResolved && (
                  <span className={clsx(
                    "text-[10px] font-medium px-1.5 py-0.5 rounded-full",
                    isActive
                      ? "bg-teal-light/20 text-teal-light"
                      : "bg-resolved-bg text-resolved"
                  )}>
                    Resolved
                  </span>
                )}
                {!isResolved && session.sessionId && (
                  <span className={clsx(
                    "text-[10px] font-mono truncate max-w-[80px]",
                    isActive ? "text-ash" : "text-dim"
                  )}>
                    #{session.sessionId.slice(0, 8)}
                  </span>
                )}
              </div>
            </button>
          );
        })}
      </div>
    </aside>
  );
}
