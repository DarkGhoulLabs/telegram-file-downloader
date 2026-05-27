# Telegram File Downloader

A simple Python-based Telegram media downloader built using [Telethon](https://github.com/LonamiWebs/Telethon?utm_source=chatgpt.com).
This tool allows you to download media files from Telegram chats, Saved Messages, groups, or channels with multiple download modes and live progress tracking. 

---

## Features

* Download **all media files** from a chat
* Download files within a **specific date range**
* Choose and download **specific files manually**
* Real-time download progress bars using tqdm
* Supports:

  * Saved Messages
  * Private chats
  * Groups
  * Channels
* Custom download directory support

---

## Tech Stack

* Python
* [Telethon](https://github.com/LonamiWebs/Telethon?utm_source=chatgpt.com)
* [tqdm](https://github.com/tqdm/tqdm?utm_source=chatgpt.com)

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/telegram-file-downloader.git
cd telegram-file-downloader
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install telethon tqdm
```

---

## Telegram API Setup

To use this project, you need Telegram API credentials.

### Steps:

1. Visit: [my.telegram.org](https://my.telegram.org?utm_source=chatgpt.com)
2. Log in with your Telegram account
3. Open **API Development Tools**
4. Create an application
5. Copy:

   * `api_id`
   * `api_hash`

Replace them in the script:

```python
api_id = YOUR_API_ID
api_hash = "YOUR_API_HASH"
```

---

## Usage

Run the script:

```bash
python main.py
```

You will be asked for:

* Chat username / ID
* Download folder
* Download mode

---

## Available Modes

### 1. Download All Files

Downloads every media file from the entire chat history.

### 2. Download by Date Range

Download files between selected start and end dates.

Example:

```text
Start date: 2025-01-01
End date: 2025-02-01
```

### 3. Choose Specific Files

* Scans recent media messages
* Displays message IDs and filenames
* Lets you choose which files to download

Example:

```text
12345, 67890, 54321
```

---

## Example Output

```text
====== Telegram File Downloader ======

Enter chat username/ID: me

Choose mode:
1) Download All Files
2) Download files in a Date Range
3) Choose SPECIFIC files

Your choice: 1
```

---

## Project Structure

```text
telegram-file-downloader/
│
├── main.py
├── requirements.txt
└── README.md
```

---

## Future Improvements

* GUI version
* Resume interrupted downloads
* File type filtering
* Multi-threaded downloading
* Duplicate file detection
* Export download logs

---

## Known Issues

* Large chats may take time to scan
* Telegram rate limits can slow downloads
* Requires first-time Telegram login authentication

---

## License

This project is open-source and available under the MIT License.

---

## Author

Priyanshu Parmar

* [GitHub](https://github.com/DarkGhoulLabs)
* [LinkedIn](https://www.linkedin.com/in/priyanshu-parmar-8b80b62b4)
