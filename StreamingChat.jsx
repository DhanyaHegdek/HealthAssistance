import React, { useState } from "react";

const API = import.meta.env.VITE_API_BASE || "http://127.0.0.1:8000";
const WS = API.replace(/^http/, "ws");


export default function StreamingChat() {
  const [messages, setMessages] = useState([
    { sender: "bot", text: "Hi — how are you feeling today? 💬" }
  ]);
  const [input, setInput] = useState("");

  function addMessage(msg) {
    setMessages((prev) => [...prev, msg]);
  }

  function speak(text) {
    const speech = new SpeechSynthesisUtterance(text);
    speechSynthesis.speak(speech);
  }

  function voiceInput() {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) return alert("Your browser does not support voice input.");

    const rec = new SR();
    rec.lang = "en-US";
    rec.onresult = (e) => setInput(e.results[0][0].transcript);
    rec.start();
  }

  function send() {
    if (!input.trim()) return;

    const ws = new WebSocket(`${WS}/ws/chat`);

    addMessage({ sender: "user", text: input });

    const payload = JSON.stringify({
      user_id: "demo",
      message: input
    });

    let buffer = "";

    ws.onopen = () => ws.send(payload);

    ws.onmessage = (e) => {
      // Try JSON (crisis mode)
      try {
        const data = JSON.parse(e.data);
        if (data.type === "crisis") {
            addMessage({ sender: "bot", text: data.reply });
            ws.close();
            return;
        }
      } catch (_) {}

      buffer += e.data;
      setMessages((prev) => {
        const last = prev[prev.length - 1];
        if (last.sender === "bot_stream") {
          const updated = [...prev];
          updated[updated.length - 1] = { sender: "bot_stream", text: buffer };
          return updated;
        }
        return [...prev, { sender: "bot_stream", text: buffer }];
      });
    };

    ws.onclose = () => {
      speak(buffer);
      setMessages((prev) =>
        prev.map((m) =>
          m.sender === "bot_stream"
            ? { sender: "bot", text: m.text }
            : m
        )
      );
    };

    setInput("");
  }

  return (
    <div className="bg-white shadow p-4 rounded-lg h-[70vh] flex flex-col">

      {/* Messages */}
      <div className="flex-1 overflow-y-auto space-y-3">
        {messages.map((m, idx) => (
          <div key={idx} className={m.sender === "user" ? "text-right" : "text-left"}>
            <span
              className={
                m.sender === "user"
                  ? "bg-green-200 px-3 py-2 rounded-xl inline-block"
                  : "bg-gray-200 px-3 py-2 rounded-xl inline-block"
              }
            >
              {m.text}
            </span>
          </div>
        ))}
      </div>

      {/* Input bar */}
      <div className="mt-3 flex gap-2">
        <button
          onClick={voiceInput}
          className="px-3 py-2 bg-blue-600 text-white rounded-lg"
        >
          🎙️
        </button>

        <input
          className="flex-1 border px-3 py-2 rounded-lg"
          placeholder="Talk to me…"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
        />

        <button
          onClick={send}
          className="px-4 py-2 bg-green-600 text-white rounded-lg"
        >
          Send
        </button>
      </div>
    </div>
  );
}
