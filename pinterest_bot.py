import os
import requests
import json
import time
from datetime import datetime

class PinguinPinterestBot:
    def __init__(self, access_token, board_id):
        self.access_token = access_token
        self.board_id = board_id
        self.api_url = "https://api.pinterest.com/v5"
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def create_pin(self, title, description, link, image_url):
        endpoint = f"{self.api_url}/pins"
        
        payload = {
            "board_id": self.board_id,
            "title": title,
            "description": description,
            "link": link,
            "media_source": {
                "source_type": "image_url",
                "url": image_url
            }
        }

        try:
            response = requests.post(endpoint, headers=self.headers, data=json.dumps(payload))
            response.raise_for_status()
            pin_data = response.json()
            print(f"[{datetime.now()}] ✅ Successfully created Pin: '{title}'")
            print(f"Pin ID: {pin_data.get('id')}")
            return pin_data
        except requests.exceptions.RequestException as e:
            print(f"[{datetime.now()}] ❌ Error creating Pin '{title}': {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Details: {e.response.text}")
            return None

if __name__ == "__main__":
    # ==========================================================
    # --- Pinguin-Umzuege Pinterest Configuration ---
    # 1. Get these from your Pinterest Developer Dashboard
    # https://developers.pinterest.com/
    # ==========================================================
    
    PINTEREST_ACCESS_TOKEN = "YOUR_ACCESS_TOKEN_HERE" 
    PINTEREST_BOARD_ID = "YOUR_BOARD_ID_HERE"
    
    # Initialize our bot
    bot = PinguinPinterestBot(PINTEREST_ACCESS_TOKEN, PINTEREST_BOARD_ID)
    
    # ==========================================================
    # --- Example Pin Data ---
    # In the future, we can load this from a spreadsheet, a blog 
    # RSS feed, or have AI automatically generate them!
    # ==========================================================
    
    sample_pins = [
        {
            "title": "5 Tipps für einen stressfreien Umzug in Berlin",
            "description": "Ein Umzug in Berlin kann anstrengend sein – muss er aber nicht! Mit diesen 5 einfachen Tipps von Pinguin Umzüge gelingt Ihr Wohnungswechsel garantiert entspannt. Holt euch jetzt euer unverbindliches Angebot! 🐧📦 #UmzugBerlin #PinguinUmzuege #Umzugstipps",
            "link": "https://www.pinguin-umzuege.de/leistungen/",
            "image_url": "https://images.unsplash.com/photo-1600585154340-be6161a56a0c?q=80&w=1000&auto=format&fit=crop" # Placeholder moving image
        },
        {
            "title": "Was kostet ein Fernumzug von Berlin?",
            "description": "Ziehen Sie von Berlin in eine andere Stadt wie Hamburg oder München? Erfahren Sie hier, worauf Sie bei den Kosten achten müssen und wie Pinguin Umzüge Ihnen hilft, sicher ans Ziel zu kommen. Wir gewähren 50€ Rabatt bei Online-Anfragen! 🚚💨 #Fernumzug #Umzug #Umzugsunternehmen",
            "link": "https://www.pinguin-umzuege.de/",
            "image_url": "https://images.unsplash.com/photo-1588636531940-064e6fc21a71?q=80&w=1000&auto=format&fit=crop" # Placeholder truck image
        }
    ]
    
    # Execute the automation
    print("Starting Pinguin Pinterest Automation...")
    for pin in sample_pins:
        bot.create_pin(
            title=pin["title"],
            description=pin["description"],
            link=pin["link"],
            image_url=pin["image_url"]
        )
        print("-" * 50)
        # Sleep slightly to avoid hitting API rate limits instantly
        time.sleep(2)
