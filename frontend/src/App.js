import React, { useState, useRef, useEffect } from "react";
import "./App.css";
import ReactMarkdown from "react-markdown";

function App() {

  const [message, setMessage] = useState("");
  const [chat, setChat] = useState([]);
  const [darkMode, setDarkMode] = useState(false);
  const [typing, setTyping] = useState(false);

  const chatEndRef = useRef(null);

  const examplePrompts = [
    "What is Artificial Intelligence?",
    "Explain DevOps",
    "What is Machine Learning?"
  ];

  // Load chat history
  useEffect(() => {
    const savedChat = localStorage.getItem("chatHistory");
    if (savedChat) {
      setChat(JSON.parse(savedChat));
    }
  }, []);

  // Save chat history
  useEffect(() => {
    localStorage.setItem("chatHistory", JSON.stringify(chat));
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chat]);

  const sendMessage = async (customMessage) => {

    const text = customMessage || message;

    if (!text.trim()) return;

    const userMessage = { sender: "user", text };
    setChat(prev => [...prev, userMessage]);

    setMessage("");
    setTyping(true);

    try {
      const response = await fetch("https://ai-chatbot-devops.onrender.com/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ message: text })
      });

      const data = await response.json();

      const botMessage = { sender: "bot", text: data.reply };

      setChat(prev => [...prev, botMessage]);

    } catch (error) {
      const errorMessage = {
        sender: "bot",
        text: "Error connecting to AI service."
      };

      setChat(prev => [...prev, errorMessage]);
    }

    setTyping(false);
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  };

  const clearChat = () => {
    setChat([]);
    localStorage.removeItem("chatHistory");
  };

  return (
    <div className={`app ${darkMode ? "dark" : ""}`}>

      <div className="chat-container">

        <div className="header">
          Ai chatbot 🙈🙈

          <div className="header-buttons">
            <button onClick={() => setDarkMode(!darkMode)}>
              {darkMode ? "☀️" : "🌙"}
            </button>

            <button onClick={clearChat}>
              🧹
            </button>
          </div>
        </div>

        <div className="chat-box">

          {chat.map((msg, index) => (
            <div
              key={index}
              className={`message ${msg.sender === "user" ? "user" : "bot"}`}
            >
              {msg.sender === "bot" ? "🤖 " : "👤 "}
              <ReactMarkdown>
               {msg.text}
              </ReactMarkdown>
            </div>
          ))}

          {typing && (
            <div className="message bot">
              🤖 AI is typing...
            </div>
          )}

          <div ref={chatEndRef}></div>

        </div>

        {/* Example prompts */}

        <div className="examples">

          {examplePrompts.map((prompt, index) => (
            <button
              key={index}
              onClick={() => sendMessage(prompt)}
            >
              {prompt}
            </button>
          ))}

        </div>

        <div className="input-area">

          <input
            type="text"
            placeholder="Ask something..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={handleKeyPress}
          />

          <button onClick={() => sendMessage()}>
            Send
          </button>

        </div>

      </div>

    </div>
  );
}

export default App;