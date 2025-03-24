import React, { useState } from "react";
import "./ChatBox.css";

const ChatBox = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState("");
    const [loading, setLoading] = useState(false);
    const [goal, setGoal] = useState("");
    const [progress, setProgress] = useState(0);
    const [journal, setJournal] = useState("");

    const formatText = (text) => {
        let formattedText = text.replace(/\\(.?)\\*/g, "<strong>$1</strong>");
        formattedText = formattedText.replace(/\(.?)\*/g, "<em>$1</em>");
        return formattedText;
    };

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

            if (!response.ok) {
                console.error("Error with response:", response);
                setMessages([...newMessages, { bot: "Oops, something went wrong. Please try again later." }]);
                setLoading(false);
                return;
            }

            const data = await response.json();
            console.log("Bot response:", data.response);

            setMessages([...newMessages, { bot: formatText(data.response) }]);
        } catch (error) {
            console.error("Error:", error);
            setMessages([...newMessages, { bot: "Network error. Please check your connection and try again." }]);
        }
        setLoading(false);
    };

    const handleSetGoal = () => {
        if (goal) {
            sendMessage();
        }
    };

    const handleJournalEntry = () => {
        if (journal) {
            sendMessage();
        }
    };

    const handleProgressUpdate = (progressValue) => {
        setProgress(progressValue);
        sendMessage();
    };

    return (
        <div className="chat-container futuristic-background">
            <h1 className="chatbot-title">Twaine: Your Goal Assistant</h1>
            <div className="chat-box">
                {messages.map((msg, index) => (
                    <div
                        key={index}
                        className={msg.user ? "chat-bubble user" : "chat-bubble bot"}
                        dangerouslySetInnerHTML={{ __html: msg.user || msg.bot }}
                    />
                ))}
                {loading && <div className="typing-indicator">Twaine is working hard at it...</div>}
            </div>

            <div className="input-container">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="What goal can I help you with today?"
                />
                <button onClick={sendMessage} className="send-button">Send</button>
            </div>

            {/* Goal Setting */}
            <div className="goal-container">
                <h2>Set Your Goal</h2>
                <input
                    type="text"
                    value={goal}
                    onChange={(e) => setGoal(e.target.value)}
                    placeholder="Type your goal here"
                />
                <button onClick={handleSetGoal} className="send-button">Set Goal</button>
            </div>

            {/* Progress Tracker */}
            <div className="progress-container">
                <h2>Update Progress</h2>
                <input
                    type="number"
                    value={progress}
                    onChange={(e) => setProgress(e.target.value)}
                    placeholder="Enter your progress in %"
                />
                <button onClick={() => handleProgressUpdate(progress)} className="send-button">Update Progress</button>
            </div>

            {/* Journal Entry */}
            <div className="journal-container">
                <h2>Journal Entry</h2>
                <textarea
                    value={journal}
                    onChange={(e) => setJournal(e.target.value)}
                    placeholder="Reflect on your journey here"
                />
                <button onClick={handleJournalEntry} className="send-button">Submit Journal</button>
            </div>
        </div>
    );
};

export default ChatBox;