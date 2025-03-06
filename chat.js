import { useState } from "react";
import axios from "axios";

const Chat = () => {
    const [input, setInput] = useState("");
    const [messages, setMessages] = useState([]);

    const sendMessage = async () => {
        if (!input) return;

        const userMessage = { role: "user", content: input };
        setMessages([...messages, userMessage]);

        try {
            const res = await axios.post("http://localhost:5000/chat", { message: input });
            const botMessage = { role: "assistant", content: res.data.reply };
            setMessages([...messages, userMessage, botMessage]);
        } catch (error) {
            console.error("Error sending message:", error);
        }

        setInput("");
    };

    return (
        <div className="w-full max-w-xl mx-auto p-4">
            <div className="bg-gray-100 p-4 h-96 overflow-y-auto rounded-lg">
                {messages.map((msg, i) => (
                    <div key={i} className={`p-2 ${msg.role === "user" ? "text-right" : "text-left"}`}>
                        <strong>{msg.role === "user" ? "You" : "Bot"}:</strong> {msg.content}
                    </div>
                ))}
            </div>
            <div className="flex mt-4">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    className="flex-grow p-2 border rounded-l-lg"
                />
                <button onClick={sendMessage} className="bg-blue-500 text-white p-2 rounded-r-lg">
                    Send
                </button>
            </div>
        </div>
    );
};

export default Chat;
