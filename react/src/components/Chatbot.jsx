import React, { useState } from 'react';

const Chatbot = () => {
  const [chatHistory, setChatHistory] = useState([]);
  const [input, setInput] = useState('');
  const [typing, setTyping] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const message = input.trim();
    if (!message) return;

    const newHistory = [...chatHistory, { sender: 'user', text: message }];
    setChatHistory(newHistory);
    setInput('');
    setTyping(true);

    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/chat`, { // Use environment variable for API URL
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message,
          history: newHistory.map(msg => ({
            role: msg.sender === 'user' ? 'user' : 'assistant',
            content: msg.text
          }))
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setTyping(false);
      setChatHistory(h => [...h, { sender: 'bot', text: data.response }]);
    } catch (error) {
      console.error('Error contacting server:', error); // Log error for debugging
      setTyping(false);
      setChatHistory(h => [...h, { sender: 'bot', text: 'Bot: Error contacting server.' }]);
    }
  };

  return (
    <div>
      <div>
        {chatHistory.map((msg, index) => (
          <div key={index} className={msg.sender}>
            {msg.text}
          </div>
        ))}
        {typing && <div className="typing-indicator">Bot is typing...</div>}
      </div>
      <form onSubmit={handleSubmit}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
};

export default Chatbot;