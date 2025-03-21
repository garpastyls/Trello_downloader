import requests
import json
import os
import time
import re
from unidecode import unidecode
from config import API_KEY, API_TOKEN, DELAY, BOARD_IDS

HEADERS = {
    'Authorization': f'OAuth oauth_consumer_key="{API_KEY}", oauth_token="{API_TOKEN}"'
}

# Getting a json file containing more than 1000 actions from the trello board
def fetch_all_actions(board_id):
    actions = []
    limit = 1000
    before = None
    while True:
        url = f"https://api.trello.com/1/boards/{board_id}/actions?limit={limit}&key={API_KEY}&token={API_TOKEN}"
        if before:
            url += f"&before={before}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if not data:
                break
            actions.extend(data)
            before = data[-1]['id']
            time.sleep(0.5)
        else:
            print(f"Error {response.status_code} for {board_id}")
            break
    return actions

def save_actions_to_file(actions, board_id, folder):
    file_path = os.path.join(folder, f"board_{board_id}_actions.json")
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(actions, f, ensure_ascii=False, indent=4)
    print(f"Saved {len(actions)} actions in {file_path}")

# Getting attachments from the trello board
def get_cards_from_board(board_id):
    url = f"https://api.trello.com/1/boards/{board_id}/cards"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    time.sleep(DELAY)
    return response.json()

def get_attachments(card_id):
    url = f"https://api.trello.com/1/cards/{card_id}/attachments"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    time.sleep(DELAY)
    return response.json()

def sanitize_filename(filename):
    return re.sub(r'[^a-zA-Z0-9_.-]', '_', filename)

def get_translit_name(name, max_length=100):
    translit_name = unidecode(name)
    translit_name = re.sub(r'[^a-zA-Z0-9_-]', '_', translit_name)
    return translit_name[:max_length]

def download_attachment(attachment, board_folder, card_id, card_name):
    file_name = sanitize_filename(unidecode(attachment['name']))
    download_url = attachment['url']
    card_folder_name = f"{card_id}_{get_translit_name(card_name)}"
    card_folder = os.path.join(board_folder, 'attachments', card_folder_name)
    os.makedirs(card_folder, exist_ok=True)
    file_path = os.path.join(card_folder, file_name)
    response = requests.get(download_url, headers=HEADERS, stream=True)
    response.raise_for_status()
    with open(file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print(f'Downloaded: {file_path}')
    time.sleep(DELAY)

def main():
    if not BOARD_IDS:
        print("BOARD_IDS are not specified in config.py. Run get_trello_boards_id.py to get the ID.")
        return
    
    for board_id in BOARD_IDS:
        board_folder = f"trello_data/{board_id}"
        os.makedirs(board_folder, exist_ok=True)
        actions = fetch_all_actions(board_id)
        save_actions_to_file(actions, board_id, board_folder)
        cards = get_cards_from_board(board_id)
        for card in cards:
            card_id = card['id']
            card_name = card['name']
            for attachment in get_attachments(card_id):
                download_attachment(attachment, board_folder, card_id, card_name)

if __name__ == "__main__":
    main()