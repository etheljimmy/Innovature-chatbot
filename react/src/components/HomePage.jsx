import React, { useState } from 'react';
import Chatbot from './Chatbot';
import './HomePage.css'; // 

const HomePage = () => {
  const [showChatbot, setShowChatbot] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);
  const [typing, setTyping] = useState(false);

  const toggleChatbot = () => {
    setShowChatbot(!showChatbot);
  };

  return (
    <>
      <div className="home-wrapper">
        <div className="home-container">
          <header className="main-header">
            <h1>Empowering Innovations with Artificial Intelligence</h1>
            <p>Unlocking Tomorrow</p>
            <button className="header-button">Learn More →</button>
          </header>

          <main className="main-content">
            <h2>Revolutionizing Tomorrow</h2>
            <h3>The Power of Digital Transformation</h3>
            <p>
              Innovature, a global software company since 2005, empowers businesses across industries with digital solutions—spanning Cloud, Data, AI, and Consulting—to scale faster, operate safer, and grow smarter across borders.<br />
              Rooted in deep domain expertise and a unique <b>“insource quality, outsource execution”</b> model, we help enterprises unlock long-term value through purposeful digital transformation.
            </p>
          </main>
        </div>
      </div>

      {/*Button*/}
      <button onClick={toggleChatbot} className="chat-toggle-btn">
        Chat
      </button>

      {/*floating */}
      {showChatbot && (
        <div className="chatbot-container">
          <Chatbot
            chatHistory={chatHistory}
            setChatHistory={setChatHistory}
            typing={typing}
            setTyping={setTyping}
          />
        </div>
      )}
    </>
  );
};

export default HomePage;
