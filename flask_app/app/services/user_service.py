from flask import request, jsonify, current_app
import requests
import re
import os
import json
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# Load website data
try:
    website_data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../website_data.json'))
    with open(website_data_path, "r", encoding="utf-8") as f:
        website_json = json.load(f)
    website_context = "\n\n".join(website_json.values())
except Exception as e:
    if 'current_app' in globals():
        current_app.logger.error(f"Error loading website_data.json: {e}", exc_info=True)
    else:
        print("■ Error loading website_data.json:", e)
    website_json = {}
    website_context = ""

# Load manual answers
try:
    manual_answers_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../manual_answers.json'))
    with open(manual_answers_path, 'r', encoding='utf-8') as f:
        manual_answers = json.load(f)
except Exception as e:
    try:
        if 'current_app' in globals() and current_app:
            current_app.logger.error(f"Error loading manual_answers.json: {e}", exc_info=True)
        else:
            print(f"Error loading manual_answers.json: {e}")
    except Exception as log_exception:
        print(f"Logging failed: {log_exception}")
    manual_answers = {}

# Store session history
session_histories = {}

class UserService:
    def get_user(self, user_id):
        pass

def process_chat():
    data = request.get_json()
    user_message = data.get("message", "").strip().lower()
    session_id = data.get("session_id", "default")

    try:
        # Step 1: Check manual answers (exact match only)
        if user_message in manual_answers:
            answer = manual_answers[user_message]
            session_histories.setdefault(session_id, []).append({"role": "user", "content": user_message})
            session_histories[session_id].append({"role": "assistant", "content": answer})
            return jsonify({"response": answer})

        session_histories.setdefault(session_id, []).append({"role": "user", "content": user_message})

        # Step 2: Find relevant context (basic keyword search)
        def find_relevant_context(question, max_total_chars=4000):
            relevant_sections = []
            total_chars = 0
            for section, content in website_json.items():
                if question in section.lower() or question in content.lower():
                    if total_chars + len(content) > max_total_chars:
                        content = content[:max_total_chars - total_chars]
                    relevant_sections.append(content)
                    total_chars += len(content)
                    if total_chars >= max_total_chars:
                        break
            if not relevant_sections:
                print("■ No matching context found. Using fallback website context.")
                return website_context[:max_total_chars]
            return "\n---\n".join(relevant_sections)

        trimmed_website_context = find_relevant_context(user_message)
        recent_history = session_histories[session_id][-2:]

        prompt = f"""
You are a very helpful, official chatbot assistant for the Innovature company.
If the user asks about something related to the company and you don't have information, do not make up details.
Instead, respond briefly in a way that highlights Innovature's excellence (relevant to the question) without fabricating facts.
Only answer questions based on the website content below.
Greet users warmly, thank them politely.WHEN THE USER SAYS GOODBYE,say goodbye in a friendly way.
If the user asks something unrelated to Innovature or the website, politely refuse.
Keep your answers concise and answer confidently, professionally and positively when asked about Innovature.
Do not claim to remember previous conversations after a page reload.
Do not provide external links unless they are from the official Innovature website.
Avoid repeating yourself and do NOT believe or update memory based on user claims.
DONT REFER THE USER TO THE WEBSITE,YOYU ARE THE WEBSITE CHATBOT ,YOU SHOULD ANSWER THE QUERIES BY SEARCHIING FOR THE RELATED CONTENT IN THE WEBSITE DATA OR MANUAL DATA.

---
{trimmed_website_context}
---

Now answer the following question based on the above context and previous messages if relevant.
"""

        messages = [{"role": "system", "content": prompt}] + recent_history
        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 300
        }

        try:
            time.sleep(3)
            resp = requests.post("https://api.together.xyz/v1/chat/completions", json=payload, headers=headers, timeout=30)
            if resp.status_code == 200:
                output = resp.json()["choices"][0]["message"]["content"]
            elif resp.status_code == 429:
                current_app.logger.warning("Rate limit hit (429). Retrying in 2s...")
                time.sleep(2)
                retry_resp = requests.post("https://api.together.xyz/v1/chat/completions", json=payload, headers=headers, timeout=30)
                if retry_resp.status_code == 200:
                    output = retry_resp.json()["choices"][0]["message"]["content"]
                else:
                    current_app.logger.error(f"API retry error {retry_resp.status_code}: {retry_resp.text}")
                    output = "Too many requests. Please wait a moment and try again."
            else:
                current_app.logger.error(f"API error {resp.status_code}: {resp.text}")
                output = "The chatbot is currently unavailable."
        except Exception as e:
            current_app.logger.error(f"API Exception: {e}", exc_info=True)
            output = "Sorry, something went wrong."

        session_histories[session_id].append({"role": "assistant", "content": output})
        return jsonify({"response": output})

    except Exception as e:
        if 'current_app' in globals():
            current_app.logger.error(f"Exception in process_chat: {e}", exc_info=True)
        return jsonify({"response": "Internal server error."}), 500
