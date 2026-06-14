"use client";

import { useRef, useEffect, useState, useCallback } from "react";
import { Session } from "@/types";
import ChatMessage, { TypingIndicator } from "./ChatMessage";
import {
  Send,
  ChevronDown,
  CheckCircle2,
  Hash,
  Inbox,
  MessageSquarePlus,
} from "lucide-react";
import clsx from "clsx";

interface ChatPanelProps {
  session: Session | null;
  isLoading: boolean;
  onSendMessage: (sessionLocalId: string, query: string) => Promise<void>;
  onCreateSession: () => void;
}

export default function ChatPanel({
  session,
  isLoading,
  onSendMessage,
  onCreateSession,
}: ChatPanelProps) {
  const [inputValue, setInputValue] = useState("");
  const [showScrollButton, setShowScrollButton] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const messagesContainerRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const scrollToBottom = useCallback((behavior: ScrollBehavior = "smooth") => {
    messagesEndRef.current?.scrollIntoView({ behavior, block: "end" });
  }, []);

  // Auto-scroll when new messages arrive
  useEffect(() => {
    if (session?.messages.length) {
      scrollToBottom("smooth");
    }
  }, [session?.messages.length, isLoading, scrollToBottom]);

  // Detect scroll position to show/hide scroll button
  useEffect(() => {
    const container = messagesContainerRef.current;
    if (!container) return;

    const handleScroll = () => {
      const { scrollTop, scrollHeight, clientHeight } = container;
      const distanceFromBottom = scrollHeight - scrollTop - clientHeight;
      setShowScrollButton(distanceFromBottom > 120);
    };

    container.addEventListener("scroll", handleScroll);
    return () => container.removeEventListener("scroll", handleScroll);
  }, []);

  // Auto-resize textarea
  useEffect(() => {
    const ta = textareaRef.current;
    if (!ta) return;
    ta.style.height = "auto";
    ta.style.height = `${Math.min(ta.scrollHeight, 140)}px`;
  }, [inputValue]);

  // Reset input when session changes
  useEffect(() => {
    setInputValue("");
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }
  }, [session?.id]);

  const handleSend = async () => {
    const query = inputValue.trim();
    if (!query || !session || isLoading || session.status === "approved") return;
    setInputValue("");
    await onSendMessage(session.id, query);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const isResolved = session?.status === "approved" || session?.status === "denied" || session?.status === 'escalate';
  const textToShowOnResolution = session?.resolvedKey?.toUpperCase();
  console.log(textToShowOnResolution, session?.status.toUpperCase(), isResolved)
  const canSend = !isLoading && !isResolved && session !== null;

  // Empty state — no session selected
  if (!session) {
    return (
      <div className="flex-1 flex flex-col items-center justify-center bg-ivory gap-5 text-center px-8">
        <div className="w-16 h-16 rounded-2xl bg-paper border border-mist flex items-center justify-center">
          <Inbox size={28} className="text-ash" />
        </div>
        <div>
          <p className="font-display text-2xl text-ink mb-2">No session open</p>
          <p className="text-sm text-dim max-w-xs leading-relaxed">
            Select a session from the left or start a new conversation.
          </p>
        </div>
        <button
          onClick={onCreateSession}
          className="flex items-center gap-2 bg-accent text-ivory text-sm font-medium px-5 py-2.5 rounded-xl hover:bg-accent-light transition-all duration-200 shadow-sm hover:shadow-md"
        >
          <MessageSquarePlus size={15} strokeWidth={2.5} />
          New Session
        </button>
      </div>
    );
  }

  return (
    <div className="flex-1 flex flex-col h-full bg-ivory overflow-hidden">
      {/* Chat Header */}
      <div className="flex items-center justify-between px-6 py-4 border-b border-mist bg-paper flex-shrink-0">
        <div className="flex items-center gap-3 min-w-0">
          <div className={clsx(
            "w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0",
            isResolved ? "bg-resolved-bg" : "bg-accent-muted"
          )}>
            {isResolved
              ? <CheckCircle2 size={18} className="text-resolved" />
              : <MessageSquarePlus size={18} className="text-accent" />
            }
          </div>
          <div className="min-w-0">
            <h2 className="font-semibold text-sm text-ink truncate">{session.title}</h2>
            <div className="flex items-center gap-1.5 mt-0.5">
              {session.sessionId ? (
                <>
                  <Hash size={11} className="text-dim" />
                  <span className="text-[11px] font-mono text-dim truncate max-w-[200px]">
                    {session.sessionId}
                  </span>
                </>
              ) : (
                <span className="text-[11px] text-dim italic">
                  Session ID pending first message…
                </span>
              )}
            </div>
          </div>
        </div>

        <div className="flex items-center gap-2 flex-shrink-0">
          {isResolved ? (
            <span className="flex items-center gap-1.5 text-xs font-medium text-resolved bg-resolved-bg px-3 py-1.5 rounded-full">
              <CheckCircle2 size={12} />
              {textToShowOnResolution}
            </span>
          ) : (
            <span className="flex items-center gap-1.5 text-xs font-medium text-accent bg-accent-muted px-3 py-1.5 rounded-full">
              <span className="w-1.5 h-1.5 rounded-full bg-accent animate-pulse inline-block" />
              Active
            </span>
          )}
        </div>
      </div>

      {/* Messages Area */}
      <div
        ref={messagesContainerRef}
        className="flex-1 overflow-y-auto px-6 py-5 space-y-4 relative"
      >
        {/* Empty session state */}
        {session.messages.length === 0 && !isLoading && (
          <div className="flex flex-col items-center justify-center h-full gap-4 text-center">
            <div className="w-14 h-14 rounded-2xl bg-paper border border-mist flex items-center justify-center">
              <MessageSquarePlus size={24} className="text-ash" />
            </div>
            <div>
              <p className="font-display text-xl text-ink mb-1">New Conversation</p>
              <p className="text-sm text-dim max-w-sm leading-relaxed">
                Send your first message to start. A session ID will be assigned by the server.
              </p>
            </div>
          </div>
        )}

        {/* Messages */}
        {session.messages.map((msg, i) => (
          <ChatMessage
            key={msg.id}
            message={msg}
            isLatest={i === session.messages.length - 1}
          />
        ))}

        {/* Typing indicator */}
        {isLoading && <TypingIndicator />}

        {/* Scroll anchor */}
        <div ref={messagesEndRef} className="h-1" />
      </div>

      {/* Scroll to bottom button */}
      {showScrollButton && (
        <div className="absolute bottom-[100px] right-8 z-10 pointer-events-none" style={{ position: "absolute" }}>
          <button
            onClick={() => scrollToBottom("smooth")}
            className="pointer-events-auto w-9 h-9 rounded-full bg-ink text-ivory flex items-center justify-center shadow-lg hover:bg-accent transition-colors duration-200 animate-fade-in"
          >
            <ChevronDown size={16} />
          </button>
        </div>
      )}

      {/* Input Area */}
      <div className="px-5 pb-5 pt-3 border-t border-mist bg-paper flex-shrink-0">
        {isResolved ? (
          <div className="flex items-center justify-center gap-2 py-3 px-4 rounded-xl bg-resolved-bg border border-resolved/20">
            <CheckCircle2 size={15} className="text-resolved" />
            <p className="text-sm text-resolved font-medium">
              This session has been resolved. No further messages can be sent.
            </p>
          </div>
        ) : (
          <div className={clsx(
            "flex items-end gap-3 rounded-2xl border px-4 py-3 transition-all duration-200",
            "bg-ivory border-mist focus-within:border-accent focus-within:shadow-sm"
          )}>
            <textarea
              ref={textareaRef}
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={!canSend}
              placeholder="Type your message… (Enter to send, Shift+Enter for newline)"
              rows={1}
              className={clsx(
                "flex-1 bg-transparent resize-none outline-none text-sm text-ink placeholder:text-ash",
                "leading-relaxed min-h-[24px] max-h-[140px] py-0.5",
                !canSend && "opacity-50 cursor-not-allowed"
              )}
            />
            <button
              onClick={handleSend}
              disabled={!canSend || !inputValue.trim()}
              className={clsx(
                "w-9 h-9 rounded-xl flex items-center justify-center flex-shrink-0 transition-all duration-200 mb-0.5",
                canSend && inputValue.trim()
                  ? "bg-accent text-ivory hover:bg-accent-light active:scale-95 shadow-sm"
                  : "bg-mist text-ash cursor-not-allowed"
              )}
            >
              <Send size={15} strokeWidth={2} />
            </button>
          </div>
        )}
        <p className="text-[10px] text-dim text-center mt-2">
          Responses are AI-generated. Always verify important information.
        </p>
      </div>
    </div>
  );
}
