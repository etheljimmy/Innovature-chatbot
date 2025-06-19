import React, { useState, useEffect, useRef } from 'react';
import './Chatbot.css';
import { sendMessageToBot } from '../services/chatbotService';

const Chatbot = () => {
  const chatEndRef = useRef(null);

  const [chatHistory, setChatHistory] = useState(() => {
    const saved = sessionStorage.getItem('chatHistory');
    return saved ? JSON.parse(saved) : [];
  });

  const [typing, setTyping] = useState(false);
  const [input, setInput] = useState('');

  useEffect(() => {
    sessionStorage.setItem('chatHistory', JSON.stringify(chatHistory));
  }, [chatHistory]);

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
      const data = await sendMessageToBot(message, newHistory.map(msg => ({
        role: msg.sender === 'user' ? 'user' : 'assistant',
        content: msg.text
      })));
      setChatHistory(h => [...h, { sender: 'bot', text: data.response }]);
    } catch (error) {
      setChatHistory(h => [...h, { sender: 'bot', text: 'Bot error: could not contact server.' }]);
    } finally {
      setTyping(false);
    }
  };

  return (
    <div className="chatbox">
      <div className="chatHeader">Innovature Chatbot</div>
      <div className="chatArea">
        {chatHistory.map((msg, i) => (
          <div key={i} className={msg.sender === 'user' ? 'userBubble' : 'botBubble'}>
            {msg.text}
          </div>
        ))}
        {typing && <div className="botBubble">Bot is typing...</div>}
        <div ref={chatEndRef} />
      </div>
      <form className="inputArea" onSubmit={handleSubmit}>
        <input
          className="inputBox"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Type a message..."
        />
        <button className="sendButton" type="submit">Send</button>
      </form>
    </div>
  );
};

export default Chatbot;
