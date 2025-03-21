# Trello Downloader

This project is designed to download JSON files with actions and attachments from Trello boards, bypassing the 1000-action limit.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/garpastyls/Trello_downloader.git
   cd Trello_downloader
   ```

2. **Create a virtual environment (recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate  # For Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. **Edit the `config.py` file in the project's root directory** and add the following:
   ```python
   API_KEY = "your_trello_api_key"
   API_TOKEN = "your_trello_api_token"
   DELAY = 0.5  # Delay between requests
   BOARD_IDS = []  # Specify the required board IDs after retrieving them
   ```

2. **Obtain your Trello API key and token:**
   1. Go to [Trello Power-Ups Admin](https://trello.com/power-ups/admin)
   2. Click "Enhancements"
   3. Click "Create New" and enter organization details
   4. Click "Generate new API key" and save it in `config.py`
   5. Click "Manually generate a token" (review the page and click Allow). Save the token in `config.py`

3. **Retrieve board IDs:**
   ```bash
   python get_trello_boards_id.py
   ```
   This will display a list of your boards and their IDs in the console. Select the necessary IDs and manually add them to `BOARD_IDS` in `config.py`.

4. **Run the script to download data:**
   ```bash
   python download_trello_json_and_attachment.py
   ```

## Output
   - JSON file with actions (`/trello_downloader/trello_data/BOARD_IDS/json`)
   - Folder with attachments (`/trello_downloader/trello_data/BOARD_IDS/attachments/CARD_IDS`)
     
## Additional Information
- The script processes file names to remove invalid characters.
- Built-in delays help avoid exceeding Trello API rate limits.

## License
MIT License

