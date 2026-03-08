import os
import requests
import json
from dotenv import load_dotenv

# Load your token from the .env file
load_dotenv()
ACCESS_TOKEN = os.environ.get("PINTEREST_ACCESS_TOKEN")

def list_my_boards():
    if not ACCESS_TOKEN or ACCESS_TOKEN == "YOUR_FULL_TOKEN_HERE":
        print("\n❌ Error: No Access Token found in .env file!")
        print("Please add your token to the .env file first.")
        return

    print("\n🐧 Fetching your Pinterest boards...")
    
    url = "https://api.pinterest.com/v5/boards"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])
            
            if not items:
                print("No boards found. Is your account connected correctly?")
                return

            print("\n✅ Found these boards:")
            print("-" * 50)
            for board in items:
                print(f"📌 Name: {board['name']}")
                print(f"🆔 ID:   {board['id']}")
                print("-" * 50)
            
            print("\nCopy the 'ID' for the board you want to use and paste it into your .env file!")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Something went wrong: {e}")

if __name__ == "__main__":
    list_my_boards()
