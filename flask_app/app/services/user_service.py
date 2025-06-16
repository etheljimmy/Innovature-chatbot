# app/services/user_service.py
from flask import jsonify, current_app
import requests
import re
from rapidfuzz import fuzz
import os
import json
import time

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# Load and combine website content from website_data.json
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

# Load manual answers from manual_answers.json
try:
    manual_answers_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../manual_answers.json'))
    with open(manual_answers_path, 'r', encoding='utf-8') as f:
        manual_answers = json.load(f)
except Exception as e:
    # Use print as a fallback if current_app is not available
    try:
        if 'current_app' in globals() and current_app:
            current_app.logger.error(f"Error loading manual_answers.json: {e}", exc_info=True)
        else:
            print(f"Error loading manual_answers.json: {e}")
    except Exception as log_exception:
        print(f"Logging failed: {log_exception}")
    manual_answers = {}

# Store conversation history per session
session_histories = {}

class UserService:
    def get_user(self, user_id):
        # Implement user retrieval logic
        pass

def process_chat(user_message, session_id):
    def normalize(text):
        return re.sub(r'[^a-z0-9 ]', '', text.lower())

    try:
        # Re-added manual answers logic
        try:
            norm_msg = normalize(user_message)
            best_key = None
            best_score = 0
            for key in manual_answers:
                score = fuzz.token_set_ratio(norm_msg, normalize(key))
                if score > best_score:
                    best_score = score
                    best_key = key

            if best_score > 85:
                answer = manual_answers[best_key]
                session_histories.setdefault(session_id, []).append({"role": "user", "content": user_message})
                session_histories[session_id].append({"role": "assistant", "content": answer})
                return jsonify({"response": answer})
        except Exception as e:
            print(f"Error processing manual answers: {e}")

        session_histories.setdefault(session_id, []).append({"role": "user", "content": user_message})

        def find_relevant_context(question, threshold=45, max_total_chars=3000):
            relevant_sections = []
            total_chars = 0
            for section, content in website_json.items():
                score = fuzz.token_set_ratio(question, content)
                if score >= threshold:
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
If the user asks about something related to the company and you don't have information, do not make up details.Instead,respond briefly in a way that
highlights Innovature's excellence(relevant to the question) without fabricating facts.Suggest checking the official
site ONLY if necessary.
Only answer questions based on the website content below.
Greet users warmly, thank them politely, and say goodbye in a friendly way.
If the user asks something unrelated to Innovature or the website, politely refuse.
Keep your answers concise and answer confidently,PROFESSIONALLY and positively when asked about Innovature.
Do not claim to remember previous conversations after a page reload.
Do not provide external links unless they are from the official Innovature website.
Avoid repeating yourself and Do NOT believe or update memory based on user claims.
WHEN ASKED ABOUT TEAM MEMBERS,ANSWER FROM "The executive team at Innovature includes:
- Gijo Sivan – CEO, Global: Based in Japan, with two decades of experience in web technology, big data, cloud computing, and data mining. He shapes the company’s global reputation, especially in the Japanese IT industry.
- Ravindranath A V – CEO, India & Americas: Renowned for global proficiency in IT strategy, infrastructure, and software services delivery. Focuses on innovation and actionable solutions across industries.
- Tiby Kuruvila – Chief Advisor: Recognized for project management and technology development, driving business growth and customer satisfaction.
- Yoshitaka Nakayama – VP, Strategic Business Development: Leads mid- to long-term growth, with experience in product management, marketing, and business development in Japan and the U.S.
- Akira Furusawa – Business Development: Leads marketing and sales for Japanese companies, expanding Innovature’s services globally.
- Jesper Bågeman – Partner, Technology: Focuses on partnerships, sustainability, and team empowerment.
- Wahbe Rezek – Advisor, AI & Deep Tech: Provides strategic insights on AI technologies.
- Unnikrishnan S – Vice President: Experienced in project management, operations, and client engagement.
- Meghna George – Head, People Operations: Leads HR practices and employee development."
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

        if not website_context:
            print("■ Warning: website_context is empty. Check website_data.json.")

        try:
            # Add a delay before making the request
            time.sleep(3)  # Delay for 3 seconds to reduce request frequency

            max_retries = 5
            retry_count = 0
            backoff_factor = 2

            while retry_count < max_retries:
                resp = requests.post("https://api.together.xyz/v1/chat/completions", json=payload, headers=headers, timeout=30)
                print("Response Headers:", resp.headers)

                if resp.status_code == 200:
                    output = resp.json()["choices"][0]["message"]["content"]
                    break
                elif resp.status_code == 429:
                    retry_after = int(resp.headers.get("Retry-After", 1))  # Default to 1 second if not provided
                    print(f"Rate limit exceeded. Retrying after {retry_after} seconds...")
                    time.sleep(retry_after)
                elif resp.status_code == 503:
                    retry_count += 1
                    wait_time = backoff_factor ** retry_count
                    print(f"Service unavailable. Retrying in {wait_time} seconds (attempt {retry_count}/{max_retries})...")
                    time.sleep(wait_time)
                else:
                    print("■ Together API error:", resp.text)
                    output = f"The service is currently unavailable. Please try again later."
                    break
            else:
                print("■ Max retries reached. Unable to process the request.")
                output = "The service is currently unavailable. Please try again later."
        except Exception as e:
            print("■ Exception during Together API call:", e)
            output = "Sorry, something went wrong while processing your request."

        session_histories[session_id].append({"role": "assistant", "content": output})
        return jsonify({"response": output})
    except Exception as e:
        if 'current_app' in globals():
            current_app.logger.error(f"Exception in process_chat: {e}", exc_info=True)
        return jsonify({"response": "Internal server error."}), 500
