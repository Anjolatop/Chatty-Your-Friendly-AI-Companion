import React, { useState, useEffect } from "react";
import "./ChatBox.css"; 

const ChatBox = () => {
    const [messages, setMessages] = useState([]); 
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false); 
    const sendMessage = async () => {
        if (!input) return;

        const newMessages = [...messages, { user: input }];
        setMessages(newMessages);
        setInput("");
        setLoading(true);

        try {
            const response = await fetch("http://127.0.0.1:5000/api/get_response", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: input }),
            });
            const data = await response.json();

            setMessages([...newMessages, { bot: data.response }]);
        } catch (error) {
            console.error("Error:", error);
        }
        setLoading(false);
    };

    return (
        <div className="chat-container futuristic-background">
             <h1 className="chatbot-title">Twaine</h1>
            <div className="chat-box">
                {messages.map((msg, index) => (
                    <div key={index} className={msg.user ? "chat-bubble user" : "chat-bubble bot"}>
                        {msg.user || msg.bot}
                    </div>
                ))}
                {loading && <div className="typing-indicator">Bot is typing...</div>}
            </div>
            <div className="input-container">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Type your message..."
                />
                <button onClick={sendMessage} className="send-button">Send</button>
            </div>
        </div>
    );
};

export default ChatBox;
