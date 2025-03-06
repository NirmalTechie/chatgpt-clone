import { useState } from "react";
import { sendMessageToChatGPT } from "./api";

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleSend = async () => {
    if (!input.trim()) return;

    const newMessage = { role: "user", content: input };
    setMessages([...messages, newMessage]);

    setInput(""); // Clear input

    const botResponse = await sendMessageToChatGPT(input);
    setMessages([...messages, newMessage, { role: "assistant", content: botResponse }]);
  };

  return (
    <div className="h-screen flex flex-col items-center justify-center bg-gray-100">
      <div className="w-full max-w-2xl bg-white shadow-lg rounded-lg p-6">
        <h1 className="text-xl font-bold mb-4 text-center">ChatGPT Clone</h1>
        
        <div className="h-96 overflow-y-auto border p-3 rounded-lg">
          {messages.map((msg, index) => (
            <div key={index} className={`p-2 my-1 ${msg.role === "user" ? "text-right" : "text-left"}`}>
              <span className={`inline-block px-3 py-1 rounded-lg ${msg.role === "user" ? "bg-blue-500 text-white" : "bg-gray-200 text-black"}`}>
                {msg.content}
              </span>
            </div>
          ))}
        </div>

        <div className="flex mt-4">
          <input
            type="text"
            className="flex-1 border rounded-l-lg p-2 outline-none"
            placeholder="Type a message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
          <button className="bg-blue-500 text-white px-4 py-2 rounded-r-lg" onClick={handleSend}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
