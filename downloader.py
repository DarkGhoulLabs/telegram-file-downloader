# Project Dependencies:
#   telethon    : Telegram Client library used to access chat history and download files.
#   tqdm        : Provides progress bars for each file being downloaded

# Install all required packages:
# Install with : pip install -r requirements.txt

# Importing all the required libraries
import os
from datetime import datetime
from telethon import TelegramClient
from tqdm import tqdm

# Replace with your real credentials
api_id = #API_ID
api_hash = "#API_HASH"
session_name = "my_session"
client = TelegramClient(session_name, api_id, api_hash)


#Progress bar
_progress_bars = {}

def progress_tqdm(recieved: int, total: int, msg_id=None):
# Shows a tqdm progress bar per message ID
    if total is None or total == 0:
        total = 1
    if msg_id not in _progress_bars:
        _progress_bars[msg_id] = tqdm(
            total=total,
            unit="B",
            unit_scale=True,
            desc=f"msg {msg_id}",
            leave=True,
        )
    bar = _progress_bars[msg_id]
    bar.total = total
    bar.n = recieved
    bar.refresh()
    
    if recieved >= total:
        bar.close()
        del _progress_bars[msg_id]


def ask_date(prompt: str):
# Ask for date in YYYY-MM-DD format.
# Returns a datetime.date object or None if left empty
    txt = input(prompt).strip()
    if not txt:
        return None
    try:
        return datetime.strptime(txt, "%Y-%m-%d").date()
    except:
        print("Invalid format, expected YYYY-MM-DD, Try again.")
        return ask_date(prompt)
    

def ask_download_folder():
# Ask the user for a download folder.
# Default: ./Downloads
# Returns the absolute path
    txt = input("Enter download folder path (leave empty for './downloads'): ").strip()
    if not txt:
        txt = "Downloads"

    folder = os.path.abspath(os.path.expanduser(txt))
    os.makedirs(folder, exist_ok=True)
    print(f"Files will be downloaded to {folder}")
    return folder


async def download_all_files(target, download_dir):
# Mode 1 : download all files from the chat history
    print("\n------ Download all files mode ------")
    count = 0
    async for msg in client.iter_messages(target, limit=None):
        if not msg.media:
            continue
        try:
            path = await msg.sownload_media(
                file=download_dir,
                progress_callback=lambda r, t, mid=msg.id: progress_tqdm(
                    r, t, msg_id=mid
                ),
            )
            if path:
                count += 1
                print(f"[{count}] id={msg.id} -> {path}")
        except Exception as e:
            print(f"Error downloading message {msg.id}: {e}")
    print(f"\nDone. Downloaded {count} file(s) from the entire history.")


async def download_by_date_range(target, download_dir):
# Mode 2: Download files between two dates (inclusive).
    print("\n------ Date range mode ------")
    print("Leave empty to skip start/end limit.")
    start_date = ask_date("Start date (YYYY-MM-DD, optional): ")
    end_date = ask_date("End date (YYYY-MM-DD, optional): ")
    
    count = 0
    #reverse is true -> from oldest to newest; easier to read progress
    async for msg in client.iter_messages(target, limit=None, reverse=True):
        if not msg.media:
            continue
        
        msg_d = msg.date.date()  #this is for only taking the date part
        
        if start_date and msg_d < start_date:
            continue
        if end_date and msg_d > end_date:
            continue
        try:
            path = await msg.download_media(
                file=download_dir,
                progress_callback=lambda r, t, mid=msg.id: progress_tqdm(
                    r, t, msg_id=mid
                ),
            )
            if path:
                count += 1 
                print(f"[{count}] {msg_d} id={msg.id} -> {path}")
        except Exception as e:
            print(f"Error downloading message {msg.id} : {e}")
    print(f"\nDone. Downloade {count} file(s) between the given dates.")


async def choose_specific_files(target, download_dir, scan_limit=200):
#Mode 3: show upto 'scan_limit' recent media messages, then let you pick specific files to download.
    print("\n------ Specific files mode -------")
    print(f"Scanning upto {scan_limit} recent messages for media.....\n")
    
    media_messages = []
    idx = 1

    async for msg in client.iter_messages(target, limit=scan_limit):
        if not msg.media:
            continue
        fname = None
        if msg.file and msg.file.name:
            fname = msg.file.name
        msg_d = msg.date.strftime("%Y-%m-%d %H:%M")
        print(
            f"{idx:3d}. msg_id={msg.id:8d}  date={msg_d}  name={fname or '<no name>'}"
        )
        media_messages.append(msg)
        idx +=1
    if not media_messages:
        print("No media messages found in the scanned range.")
        return
    ids_input = input(
        "\nEnter the mes_id values you want to download "
        "(comma-seperated, e.g. 123, 456, 789):"
    ).strip()
    if not ids_input:
        print("No IDs entered, aborting specific-file download.")
        return
    try:
        ids_to_download = [int(x.strip()) for x in ids_input.split(",") if x.strip()]
    except ValueError:
        print("Invalid input: please enter integer message IDs seperated by commas.")
        return
    
    msgs = await client.get_messages(target, ids=ids_to_download)
    if not isinstance(msgs, list):
        msgs = [msgs]

    count = 0
    for m in msgs:
        if not m or not m.media:
            continue
        try:
            path = await m.download_media(
                file=download_dir,
                progress_callback=lambda r, t, mid=m.id: progress_tqdm(
                    r, t, msg_id=mid
                ),
            )
            if path:
                count += 1
                print(f"[{count}] id={m.id} -> {path}")
        except Exception as e:
            print("Error downloading message {m.id}: {e}")
    print(f"\nDone. Downloaded {count} file(s) from your selection.")


# Main Function
async def main():
    print("====== Telegram File Downloader ======")
    print("Tip: use 'me' for your Saved Messages.\n")
    
    target = input("Enter chat username/ID (or 'me' for Saved Messages): ").strip()
    
    download_dir = ask_download_folder()
    
    print("\nChoose mode:")
    print("  1) Download All Files")
    print("  2) Download files in a Date Range")
    print("  3) Choose SPECIFIC files from recent messages")
    choice = input("Your choice (1/2/3): ").strip()

    if choice == "1":
        await download_all_files(target, download_dir)
    elif choice == "2":    
        await download_by_date_range(target, download_dir)
    elif choice == "3":
        await choose_specific_files(target, download_dir)
    else:
        print("Invalid choice. Choose one of them '1/2/3'")


if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(main())