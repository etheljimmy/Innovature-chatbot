import React, { useState, useEffect, useRef } from 'react';
import './Chatbot.css';
import { sendMessageToBot } from '../services/chatbotService';
const Chatbot = () => {
  const chatEndRef = useRef(null);//scroll to bottom after each msg
  //Cookiehelpers
  function getCookie(name) {
    const cookieArr = document.cookie.split('; ');
    for (const cookie of cookieArr) {
      const [key, value] = cookie.split('=');
      if (key === name) return value;
    }
    return null;
  }
  function setCookie(name, value, days = 7) {
    const expires = new Date(Date.now() + days * 864e5).toUTCString();
    document.cookie = `${name}=${value}; expires=${expires}; path=/`;
  }
  function generateSessionId() {//uniqueid
    return 'session-' + Math.random().toString(36).substring(2, 15);
  }
  //cookiecheck
  const [sessionId, setSessionId] = useState('');
  useEffect(() => {
    let sid = getCookie('chat_session_id');
    if (!sid) {
      sid = generateSessionId();
      setCookie('chat_session_id', sid, 7);
    }
    setSessionId(sid);
  }, []);
  //checkhistory,if yes load
  const [chatHistory, setChatHistory] = useState(() => {
    const saved = sessionStorage.getItem('chatHistory');
    return saved ? JSON.parse(saved) : [];
  });
  const [typing, setTyping] = useState(false);//typingbot
  const [input, setInput] = useState('');
  useEffect(() => {//historysavee
    sessionStorage.setItem('chatHistory', JSON.stringify(chatHistory));
  }, [chatHistory]);
  useEffect(() => {//scroll to bottom auto
    if (chatEndRef.current) {
      chatEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [chatHistory, typing]);
  const handleSubmit = async (e) => {//stops page refresh when clicked
    e.preventDefault();
    const message = input.trim();
    if (!message) return;
    //newchat
    const newHistory = [...chatHistory, { sender: 'user', text: message }];
    setChatHistory(newHistory);
    setInput('');
    setTyping(true);
    try {//send to backend
      const data = await sendMessageToBot(message, newHistory.map(msg => ({
        role: msg.sender === 'user' ? 'user' : 'assistant',
        content: msg.text
      })), sessionId); //sessionId
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
