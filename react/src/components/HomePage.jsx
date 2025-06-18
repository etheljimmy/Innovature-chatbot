import React, { useState } from 'react';
import Chatbot from './Chatbot';

const HomePage = () => {
  const [showChatbot, setShowChatbot] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);
  const [typing, setTyping] = useState(false);

  const toggleChatbot = () => {
    setShowChatbot(!showChatbot);
  };

  return (
    <>
      {/* ✅ Main Page Content */}
      <div style={{ fontFamily: 'Montserrat, Arial, sans-serif', background: '#f4f9ff', minHeight: '100vh', margin: 0 }}>
        <div style={{ maxWidth: '100%', margin: '0 auto', padding: '0 0 40px 0' }}>
          <header style={{
            background: 'linear-gradient(90deg, #102049 60%, #007bff 100%)',
            borderRadius: '0 0 32px 32px',
            boxShadow: '0 2px 16px rgba(0,0,0,0.07)',
            padding: '64px 0 48px 0',
            marginBottom: '40px',
            textAlign: 'center'
          }}>
            <h1 style={{
              fontSize: '3.5rem',
              fontWeight: 800,
              color: 'white',
              margin: 0,
              letterSpacing: '1px'
            }}>Empowering Innovations with Artificial Intelligence</h1>
            <p style={{
              color: '#e0e7ef',
              fontSize: '1.5rem',
              margin: '24px 0 0 0',
              fontWeight: 500
            }}>Unlocking Tomorrow</p>
            <button style={{
              marginTop: '32px',
              padding: '16px 36px',
              fontSize: '1.2rem',
              fontWeight: 600,
              background: '#fff',
              color: '#102049',
              border: 'none',
              borderRadius: '32px',
              cursor: 'pointer',
              boxShadow: '0 2px 8px rgba(0,0,0,0.10)'
            }}>Learn More →</button>
          </header>

          <main style={{ textAlign: 'center', color: '#222', fontSize: '1.25rem', marginTop: '48px' }}>
            <h2 style={{
              color: '#d7263d',
              fontWeight: 700,
              fontSize: '1.5rem',
              marginBottom: '16px'
            }}>Revolutionizing Tomorrow</h2>
            <h3 style={{
              fontWeight: 700,
              fontSize: '2.2rem',
              margin: '0 0 16px 0'
            }}>The Power of Digital Transformation</h3>
            <p style={{
              maxWidth: '900px',
              margin: '0 auto 32px auto',
              color: '#444',
              fontSize: '1.1rem'
            }}>
              Innovature, a global software company since 2005, empowers businesses across industries with digital solutions—spanning Cloud, Data, AI, and Consulting—to scale faster, operate safer, and grow smarter across borders.<br />
              Rooted in deep domain expertise and a unique <b>“insource quality, outsource execution”</b> model, we help enterprises unlock long-term value through purposeful digital transformation.
            </p>
          </main>
        </div>
      </div>

      {/* ✅ Floating Chat Button */}
      <button
        onClick={toggleChatbot}
        style={{
          position: 'fixed',
          bottom: '20px',
          right: '20px',
          padding: '12px 28px',
          backgroundColor: '#007bff',
          color: '#fff',
          border: 'none',
          borderRadius: '50px',
          cursor: 'pointer',
          fontWeight: 600,
          fontSize: '1.1rem',
          boxShadow: '0 2px 8px rgba(0,0,0,0.12)',
          zIndex: 1001
        }}
      >
        Chat
      </button>

      {/* ✅ Floating Chatbot Rendered OUTSIDE Main Layout */}
      {showChatbot && (
        <div style={{ position: 'fixed', bottom: '80px', right: '20px', zIndex: 1000 }}>
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
