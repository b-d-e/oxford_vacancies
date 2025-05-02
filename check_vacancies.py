#!/usr/bin/env python3
import os
import json
import requests
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime
import pathlib

# Configuration
VACANCIES_URL = "https://collegevacancies.web.ox.ac.uk/"
# Read keywords from environment variable
keywords_str = os.environ.get("VACANCY_KEYWORDS", "Balliol")
KEYWORDS = [k.strip() for k in keywords_str.split(",")]
DATA_FILE_PATH = "tracked_vacancies.json"  # File will be at the top level
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

def load_tracked_vacancies():
    """Load previously tracked vacancies from a JSON file"""
    try:
        with open(DATA_FILE_PATH, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"tracked_vacancies": []}

def save_tracked_vacancies(data):
    """Save tracked vacancies to a JSON file"""
    with open(DATA_FILE_PATH, "w") as f:
        json.dump(data, f, indent=2)

def send_slack_notification(vacancies):
    """Send a notification to Slack about new matching vacancies"""
    if not SLACK_WEBHOOK_URL:
        print("SLACK_WEBHOOK_URL environment variable not set. Skipping notification.")
        return
    
    if not vacancies:
        return
    
    message_blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "🔔 New Oxford College Vacancies Matching Your Keywords",
                "emoji": True
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Found {len(vacancies)} new vacancies matching your keywords:"
            }
        },
        {"type": "divider"}
    ]
    
    for vacancy in vacancies:
        message_blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"*<{vacancy['url']}|{vacancy['title']}>*\n{vacancy['description']}"
            }
        })
        message_blocks.append({"type": "divider"})
    
    message = {
        "blocks": message_blocks
    }
    
    response = requests.post(SLACK_WEBHOOK_URL, json=message)
    if response.status_code != 200:
        print(f"Failed to send Slack notification: {response.status_code} {response.text}")

def check_vacancies():
    """Check for new vacancies matching keywords"""
    # Load previously tracked vacancies
    data = load_tracked_vacancies()
    tracked_ids = {vacancy["id"] for vacancy in data["tracked_vacancies"]}
    
    # Fetch the vacancies page
    response = requests.get(VACANCIES_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Find all vacancy articles
    vacancy_articles = soup.find_all("article", class_="listing-item")
    
    # List to store new matching vacancies
    new_matching_vacancies = []
    
    for article in vacancy_articles:
        # Extract vacancy details
        link_element = article.find("a", class_="listing-item-link")
        title_element = article.find("h3")
        description_element = article.find("div", class_="teaser-text")
        
        if not all([link_element, title_element]):
            continue
        
        title = title_element.text.strip()
        url = link_element.get("href")
        description = description_element.text.strip() if description_element else ""
        
        # Create a unique ID for the vacancy
        vacancy_id = f"{url}#{title}"
        
        # Check if the vacancy contains any of the keywords
        text_to_check = (title + " " + description).lower()
        matching_keywords = [keyword for keyword in KEYWORDS if keyword.lower() in text_to_check]
        
        if matching_keywords and vacancy_id not in tracked_ids:
            # Add this vacancy to the list of new matching vacancies
            vacancy_info = {
                "id": vacancy_id,
                "title": title,
                "url": url if url.startswith("http") else f"https://collegevacancies.web.ox.ac.uk{url}",
                "description": description,
                "keywords": matching_keywords,
                "found_date": datetime.now().isoformat()
            }
            
            new_matching_vacancies.append(vacancy_info)
            data["tracked_vacancies"].append(vacancy_info)
    
    # Update the tracked vacancies file
    save_tracked_vacancies(data)
    
    # Send Slack notification for new matching vacancies
    if new_matching_vacancies:
        send_slack_notification(new_matching_vacancies)
        print(f"::set-output name=found_new::true")
        print(f"Found {len(new_matching_vacancies)} new vacancies matching keywords")
    else:
        print(f"::set-output name=found_new::false")
        print("No new vacancies matching keywords found")

if __name__ == "__main__":
    check_vacancies()
