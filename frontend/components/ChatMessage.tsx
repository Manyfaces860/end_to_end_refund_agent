"use client";

import { Message } from "@/types";
import { Bot, User } from "lucide-react";
import clsx from "clsx";

interface ChatMessageProps {
  message: Message;
  isLatest?: boolean;
}

function formatTimestamp(date: Date): string {
  return date.toLocaleTimeString("en-IN", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
  });
}

export default function ChatMessage({ message, isLatest }: ChatMessageProps) {
  const isUser = message.role === "user";

  return (
    <div
      className={clsx(
        "flex gap-3 animate-slide-up",
        isUser ? "flex-row-reverse" : "flex-row"
      )}
    >
      {/* Avatar */}
      <div
        className={clsx(
          "w-8 h-8 rounded-xl flex items-center justify-center flex-shrink-0 mt-0.5",
          isUser ? "bg-accent text-ivory" : "bg-ink text-ivory"
        )}
      >
        {isUser ? <User size={14} strokeWidth={2} /> : <Bot size={14} strokeWidth={2} />}
      </div>

      {/* Bubble */}
      <div className={clsx("flex flex-col gap-1 max-w-[75%]", isUser ? "items-end" : "items-start")}>
        <div className={clsx("flex items-center gap-2", isUser ? "flex-row-reverse" : "flex-row")}>
          <span className="text-[11px] font-medium text-dim">
            {isUser ? "You" : "Support Agent"}
          </span>
          {isLatest && (
            <span className="text-[10px] font-mono text-ash">{formatTimestamp(message.timestamp)}</span>
          )}
        </div>

        <div
          className={clsx(
            "px-4 py-3 rounded-2xl text-sm leading-relaxed",
            isUser
              ? "bg-ink text-ivory rounded-tr-sm"
              : "bg-ivory border border-mist text-ink rounded-tl-sm shadow-sm"
          )}
        >
          {/* Render newlines properly */}
          {message.content.split("\n").map((line, i, arr) => (
            <span key={i}>
              {line}
              {i < arr.length - 1 && <br />}
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}

export function TypingIndicator() {
  return (
    <div className="flex gap-3 animate-fade-in">
      <div className="w-8 h-8 rounded-xl bg-ink flex items-center justify-center flex-shrink-0">
        <Bot size={14} strokeWidth={2} className="text-ivory" />
      </div>
      <div className="flex flex-col gap-1 items-start">
        <span className="text-[11px] font-medium text-dim">Support Agent</span>
        <div className="px-4 py-3 rounded-2xl rounded-tl-sm bg-ivory border border-mist shadow-sm">
          <div className="flex items-center gap-1.5 h-4">
            <div className="typing-dot" />
            <div className="typing-dot" />
            <div className="typing-dot" />
          </div>
        </div>
      </div>
    </div>
  );
}
