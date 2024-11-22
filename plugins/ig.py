from pyrogram import Client, filters
import requests
import re
from BADMUSIC import app


# Function to fetch thumbnail from Instagram Reels
def get_reels_thumbnail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Regex to find og:image meta tag
            match = re.search(r'"og:image" content="([^"]+)"', response.text)
            if match:
                return match.group(1)  # Return the thumbnail URL
        return None
    except Exception as e:
        return None

# Command to download Instagram Reels photo
@app.on_message(filters.command("reels") & filters.private)
def reels_photo_download(client, message):
    if len(message.command) < 2:
        message.reply_text("Please provide a valid Instagram Reels URL.\nUsage: `/reels <URL>`")
        return

    url = message.command[1]
    message.reply_text("Fetching the thumbnail, please wait...")

    # Fetch the thumbnail
    thumbnail_url = get_reels_thumbnail(url)
    if thumbnail_url:
        # Send the photo to the user
        client.send_photo(chat_id=message.chat.id, photo=thumbnail_url, caption="Here is your Reels thumbnail!")
    else:
        message.reply_text("Failed to fetch the thumbnail. Please check the URL and try again.")
        

__MODULE__ = "ɪɢ-ʀᴇᴇʟ"
__HELP__ = """
**ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ:**

• `/ig [URL]`: ᴅᴏᴡɴʟᴏᴀᴅ ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟs. Pʀᴏᴠɪᴅᴇ ᴛʜᴇ ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟ URL ᴀғᴛᴇʀ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ.
• `/instagram [URL]`: ᴅᴏᴡɴʟᴏᴀᴅ ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟs. Pʀᴏᴠɪᴅᴇ ᴛʜᴇ ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟ URL ᴀғᴛᴇʀ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ.
• `/reel [URL]`: ᴅᴏᴡɴʟᴏᴀᴅ ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟs. Pʀᴏᴠɪᴅᴇ ᴛʜᴇ ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟ URL ᴀғᴛᴇʀ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ.
"""
