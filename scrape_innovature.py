import os
import requests
from bs4 import BeautifulSoup
import json
pages = {
    "homepage": "https://innovature.ai/",
    "blogs": "https://innovature.ai/blogs/",
    "lifeatinnovature": "https://innovature.ai/lifeatinnovature/",
    "about": "https://innovature.ai/about-us/",
    "our_team": "https://innovature.ai/our-team/",
    "ai_services": "https://innovature.ai/artificial-intelligence-services-and-solutions/",
    "cloud_services": "https://innovature.ai/cloud-services/",
    "case_study": "https://innovature.ai/case-study/",
    "contact": "https://innovature.ai/contact/",
    "rfp": "https://innovature.ai/rfp/",
    "careers": "https://innovature.ai/careers/",
    "newsroom": "https://innovature.ai/newsroom/",
    "industries": "https://innovature.ai/industries/",
    "industries_education": "https://innovature.ai/industries/education/",
    "industries_advertising_media": "https://innovature.ai/industries/advertising-media/",
    "industries_retail": "https://innovature.ai/industries/retail-app-development/",
    "industries_telecommunication": "https://innovature.ai/industries/telecommunication/",
    "industries_healthcare": "https://innovature.ai/industries/healthcare/",
    "industries_utilities": "https://innovature.ai/industries/utilities/",
    "industries_finance": "https://innovature.ai/industries/finance/",
    "industries_ecommerce": "https://innovature.ai/industries/e-commerce/"
}

manual_keys = ["executive_team_manual", "global_contacts_manual"]
preserved_manual = {}

# Preserve manual sections
if os.path.exists("website_data.json"):
    with open("website_data.json", "r", encoding="utf-8") as f:
        existing_data = json.load(f)
        for key in manual_keys:
            if key in existing_data:
                preserved_manual[key] = existing_data[key]


os.makedirs("scraped_pages", exist_ok=True)

#Scrape andsave 
for name, url in pages.items():
    try:
        print(f"Scraping {url}")
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        with open(f"scraped_pages/{name}.txt", "w", encoding="utf-8") as f:
            f.write(text)
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")

#Convert txt jSON
json_data = {}
for filename in os.listdir("scraped_pages"):
    if filename.endswith(".txt"):
        key = filename.replace(".txt", "")
        with open(f"scraped_pages/{filename}", "r", encoding="utf-8") as f:
            json_data[key] = f.read()

#existing manual
existing_path = "website_data.json"
if os.path.exists(existing_path):
    with open(existing_path, "r", encoding="utf-8") as f:
        existing_data = json.load(f)
    existing_data.update(json_data)
    json_data = existing_data

#SaveJSON
with open("website_data.json", "w", encoding="utf-8") as f:
    json.dump(json_data, f, indent=2, ensure_ascii=False)

print(" Scraping complete. Data saved to website_data.json (manual content preserved).")
