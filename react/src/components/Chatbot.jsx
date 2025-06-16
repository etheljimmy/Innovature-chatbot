import React, { useState, useRef, useEffect } from 'react';

const chatboxStyles = {
  fontFamily: 'Times New Roman, sans-serif',
  width: '350px',
  height: '580px',
  background: '#e9f0f7',
  borderRadius: '15px',
  boxShadow: '0 4px 24px rgba(0,0,0,0.12)',
  padding: '0',
  overflow: 'hidden',
  border: 'none',
  display: 'flex',
  flexDirection: 'column',
};
const headerStyles = {
  background: '#102049',
  color: 'white',
  padding: '18px',
  fontWeight: 'bold',
  fontSize: '1.5rem',
  textAlign: 'left',
  letterSpacing: '1px',
};
const chatAreaStyles = {
  background: '#f6f8fa',
  padding: '16px',
  flex: 1,
  maxHeight: '350px',
  overflowY: 'auto',
  display: 'flex',
  flexDirection: 'column',
  gap: '12px',
};
const userBubble = {
  alignSelf: 'flex-end',
  background: '#102049',
  color: 'white',
  borderRadius: '20px 20px 0 20px',
  padding: '12px 18px',
  maxWidth: '80%',
  fontWeight: '500',
  marginBottom: '2px',
};
const botBubble = {
  alignSelf: 'flex-start',
  background: '#cbe3f7',
  color: '#102049',
  borderRadius: '20px 20px 20px 0',
  padding: '12px 18px',
  maxWidth: '80%',
  fontWeight: '200',
  marginBottom: '2px',
};
const inputAreaStyles = {
  display: 'flex',
  borderTop: '1px solid #dbeafe',
  background: '#f6f8fa',
  padding: '12px',
  alignItems: 'center',
};
const inputStyles = {
  flex: 1,
  padding: '10px',
  borderRadius: '8px',
  border: '1px solid #b6c6e3',
  fontSize: '0.9rem',
  outline: 'none',
};
const buttonStyles = {
  marginLeft: '10px',
  padding: '10px 18px',
  background: '#102049',
  color: 'white',
  border: 'none',
  borderRadius: '8px',
  fontWeight: 'bold',
  cursor: 'pointer',
  fontSize: '1rem',
};

const Chatbot = () => {
  const [chatHistory, setChatHistory] = useState([]);
  const [input, setInput] = useState('');
  const [typing, setTyping] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [chatHistory, typing]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    const message = input.trim();
    if (!message) return;
    const newHistory = [...chatHistory, { sender: 'user', text: message }];
    setChatHistory(newHistory);
    setInput('');
    setTyping(true);
    try {
      const response = await fetch(`${import.meta.env.VITE_API_URL}/chat`, {
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
      setTyping(false);
      setChatHistory(h => [...h, { sender: 'bot', text: 'Bot: Error contacting server.' }]);
    }
  };

  return (
    <div style={chatboxStyles}>
      <div style={headerStyles}>Innovature Chatbox!</div>
      <div style={chatAreaStyles}>
        {chatHistory.map((msg, idx) => (
          <div key={idx} style={msg.sender === 'user' ? userBubble : botBubble}>
            {msg.text}
          </div>
        ))}
        {typing && <div style={botBubble}>Bot is typing...</div>}
        <div ref={chatEndRef} />
      </div>
      <form style={inputAreaStyles} onSubmit={handleSubmit}>
        <input
          style={inputStyles}
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Type your message..."
        />
        <button style={buttonStyles} type="submit">Send</button>
      </form>
    </div>
  );
};

export default Chatbot;