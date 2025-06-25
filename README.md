---

# Innovature Chatbot - README

# Project Overview
This project is a full-stack AI-powered chatbot for the Innovature company.
The Innovature Chatbot is designed to intelligently answer user questions about
the Innovature website, services, teams, and job openings.
It uses a Flask backend and a React frontend to provide users with helpful,
context-based responses based on website content and manual answers.
The chatbot is integrated with the Together.ai API using the LLaMA-3 model,
and includes context filtering via cosine similarity.

------------------------------------------------------------------------
# Key Features
------------------------------------------------------------------------
- Remembers session-specific chat history using cookies  
- Uses TF-IDF + cosine similarity to find relevant web content  
- Manual Q&A support  
- Integration with Together.ai’s LLaMA-3 model  
- Input and send button are disabled while the bot is thinking  
- Displays typing indicator  

------------------------------------------------------------------------
# Technical Implementation
------------------------------------------------------------------------
**Backend (Flask)**  
- Loads structured website content AND manual data.
- Matches user messages with manual_answers.json using cosine similarity first  
- Falls back to website context and sends prompts to Together.ai  
- Logs errors and responses in flask_app.log 

**Frontend (React + Vite)**  
- Chat interface styled using CSS  
- Handles message sending, session ID tracking with cookies  
- Maintains chat history using `sessionStorage`  
- Displays message bubbles  

------------------------------------------------------------------------
# Browser Compatibility
------------------------------------------------------------------------
This chatbot is compatible with major browsers:  
- Chrome  
- Microsoft Edge  

------------------------------------------------------------------------
# Project Structure(imp files)
------------------------------------------------------------------------
### Flask App

flask_app/  
├── run.py  
├── services/user_service.py  

### React Frontend

react/  
└── src/  
    ├── App.jsx  
    ├── index.css  
    ├── main.jsx  
    ├── components/  
    │   ├── Chatbot.jsx  
    │   ├── HomePage.jsx  
    │   ├── Chatbot.css  
    │   └── HomePage.css  
    └── services/  
        └── chatbotService.js  

------------------------------------------------------------------------
# Flask Setup & Installation
------------------------------------------------------------------------
# Install required backend packages:  

pip install flask python-dotenv requests scikit-learn
# OR
pip install -r requirements.txt

# Create and activate virtual environment:

python -m venv venv
source venv/bin/activate        # macOS/Linux  
venv\Scripts\activate           # Windows

(Create a .env file in flask_app/ with:
TOGETHER_API_KEY=your_api_key_here)


---

# React Setup & Installation
---

Install React with Vite and dependencies:

npm create vite@latest
cd react
npm install


---

# How to Run the Application


---
Start the Backend (Flask):
cd flask_app
python run.py

Start the Frontend (React) in a new terminal:
cd react
npm run build
npm run dev

This starts the chatbot app on:
http://localhost:5173

Make sure the backend is also running at the same time.
