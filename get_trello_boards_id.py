import requests
from config import API_KEY, API_TOKEN

# Getting a list of boards with their IDs
def get_boards():
    url = f"https://api.trello.com/1/members/me/boards?fields=id,name&key={API_KEY}&token={API_TOKEN}"
    response = requests.get(url)
    response.raise_for_status()
    boards = response.json()
    print("A list of your boards:")
    for board in boards:
        print(f"{board['name']}: {board['id']}")
    print("Select the desired IDs and add them to config.py")

if __name__ == "__main__":
    get_boards()