"use client";

import { useState, useCallback, useRef, useEffect } from "react";
import { Session, Message, SessionStatus } from "@/types";
import SessionSidebar from "@/components/SessionSidebar";
import ChatPanel from "@/components/ChatPanel";
import { sendMessage, extractResponseText, isSessionResolved } from "@/lib/api";
import { Menu } from "lucide-react";

let localIdCounter = 0;
function genLocalId() {
  return `local-${Date.now()}-${++localIdCounter}`;
}
function genMsgId() {
  return `msg-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
}
function makeTitle(query: string): string {
  return query.length > 36 ? query.slice(0, 36).trimEnd() + "…" : query;
}

export default function SupportPage() {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [activeSessionId, setActiveSessionId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false); // for mobile

  // Keep a ref to the latest sessions for callbacks
  const sessionsRef = useRef(sessions);
  useEffect(() => { sessionsRef.current = sessions; }, [sessions]);

  const activeSession = sessions.find((s) => s.id === activeSessionId) ?? null;

  const createSession = useCallback(() => {
    const newSession: Session = {
      id: genLocalId(),
      sessionId: null,
      title: "New Session",
      status: "pending",
      messages: [],
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    setSessions((prev) => [newSession, ...prev]);
    setActiveSessionId(newSession.id);
    setSidebarOpen(false);
  }, []);

  const handleSendMessage = useCallback(
    async (sessionLocalId: string, query: string) => {
      // Find the current session
      const currentSession = sessionsRef.current.find(
        (s) => s.id === sessionLocalId
      );
      if (!currentSession || currentSession.status === "approved") return;

      // Append user message immediately
      const userMsg: Message = {
        id: genMsgId(),
        role: "user",
        content: query,
        timestamp: new Date(),
      };

      setSessions((prev) =>
        prev.map((s) => {
          if (s.id !== sessionLocalId) return s;
          const updated = {
            ...s,
            messages: [...s.messages, userMsg],
            // Set title from first message
            title: s.messages.length === 0 ? makeTitle(query) : s.title,
            updatedAt: new Date(),
          };
          return updated;
        })
      );

      setIsLoading(true);

      try {
        // Get the latest session id at call time
        const latestSession = sessionsRef.current.find(
          (s) => s.id === sessionLocalId
        );
        const serverSessionId = latestSession?.sessionId ?? null;

        const data = await sendMessage(query, serverSessionId);
        console.log(query, serverSessionId)

        const agentContent = extractResponseText(data);
        const newServerSessionId = data.session_key ?? null;
        const resolved = isSessionResolved(data);
        const status: SessionStatus = data.refund!.toString() as SessionStatus;


        const agentMsg: Message = {
          id: genMsgId(),
          role: "agent",
          content: agentContent,
          timestamp: new Date(),
        };

        setSessions((prev) =>
          prev.map((s) => {
            if (s.id !== sessionLocalId) return s;
            return {
              ...s,
              sessionId: s.sessionId || newServerSessionId,
              messages: [...s.messages, agentMsg],
              status: status,
              resolvedKey: resolved ? data.refund?.toString() : s.resolvedKey,
              updatedAt: new Date(),
            };
          })
        );
      } catch (err) {
        const errorMsg: Message = {
          id: genMsgId(),
          role: "agent",
          content:
            err instanceof Error
              ? `⚠️ Error: ${err.message}`
              : "⚠️ Something went wrong. Please try again.",
          timestamp: new Date(),
        };
        setSessions((prev) =>
          prev.map((s) =>
            s.id === sessionLocalId
              ? { ...s, messages: [...s.messages, errorMsg], updatedAt: new Date() }
              : s
          )
        );
      } finally {
        setIsLoading(false);
      }
    },
    []
  );

  return (
    <div className="flex h-screen overflow-hidden bg-paper">
      {/* Mobile sidebar overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 z-20 bg-ink/40 backdrop-blur-sm md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <div
        className={`
          fixed md:relative z-30 md:z-auto
          h-full w-72 flex-shrink-0
          transition-transform duration-300 ease-in-out
          ${sidebarOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"}
        `}
      >
        <SessionSidebar
          sessions={sessions}
          activeSessionId={activeSessionId}
          onSelectSession={(id) => {
            setActiveSessionId(id);
            setSidebarOpen(false);
          }}
          onCreateSession={createSession}
        />
      </div>

      {/* Divider */}
      <div className="hidden md:block w-px bg-mist flex-shrink-0" />

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col min-w-0 relative">
        {/* Mobile header bar */}
        <div className="md:hidden flex items-center gap-3 px-4 py-3 border-b border-mist bg-paper flex-shrink-0">
          <button
            onClick={() => setSidebarOpen(true)}
            className="w-9 h-9 rounded-xl bg-mist flex items-center justify-center text-ink"
          >
            <Menu size={18} />
          </button>
          <span className="font-display text-lg text-ink">
            {activeSession?.title ?? "Support Agent"}
          </span>
        </div>

        <ChatPanel
          session={activeSession}
          isLoading={isLoading && activeSession !== null}
          onSendMessage={handleSendMessage}
          onCreateSession={createSession}
        />
      </div>
    </div>
  );
}
