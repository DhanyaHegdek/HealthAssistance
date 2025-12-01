import React from "react";
import StreamingChat from "./components/StreamingChat.jsx";

export default function App() {
  return (
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-4 text-center">Mental Health Assistant 💚</h1>
      <StreamingChat />
    </div>
  );
}
