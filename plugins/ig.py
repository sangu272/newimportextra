import re
import requests
from pyrogram import filters
from BADMUSIC import app
from config import LOG_GROUP_ID


@app.on_message(filters.command(["ig", "instagram", "reel"]))
async def download_instagram_video(client, message):
    # Check if the user provided a URL
    if len(message.command) < 2:
        await message.reply_text(
            "Pʟᴇᴀsᴇ ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ Iɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟ URL ᴀғᴛᴇʀ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ"
        )
        return

    # Extract the URL from the message
    url = message.text.split()[1]

    # Validate the URL format for Instagram using regex
    if not re.match(
        re.compile(r"^(https?://)?(www\.)?(instagram\.com|instagr\.am)/.*$"), url
    ):
        return await message.reply_text(
            "Tʜᴇ ᴘʀᴏᴠɪᴅᴇᴅ URL ɪs ɴᴏᴛ ᴀ ᴠᴀʟɪᴅ Iɴsᴛᴀɢʀᴀᴍ URL😅😅"
        )
    
    # Notify user that the video is being processed
    a = await message.reply_text("ᴘʀᴏᴄᴇssɪɴɢ...")

    # API URL for Instagram video download
    api_url = f"https://insta-dl.hazex.workers.dev/?url={url}"

    try:
        # Send a GET request to the API
        response = requests.get(api_url)
        # Try to parse the JSON response
        result = response.json()

        # If the result has an error, notify the user
        if result["error"]:
            await a.edit("Fᴀɪʟᴇᴅ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ʀᴇᴇʟ")
            return

        # If no error, extract the video data
        data = result["result"]
        video_url = data["url"]
        duration = data["duration"]
        quality = data["quality"]
        file_type = data["extension"]
        size = data["formattedSize"]

        # Format the caption with video information
        caption = f"**Dᴜʀᴀᴛɪᴏɴ :** {duration}\n**Qᴜᴀʟɪᴛʏ :** {quality}\n**Tʏᴘᴇ :** {file_type}\n**Sɪᴢᴇ :** {size}"

        # Remove processing message and send the video
        await a.delete()
        await message.reply_video(video_url, caption=caption)

    except Exception as e:
        # If there's any error in the process, log it and notify the user
        error_message = f"Eʀʀᴏʀ :\n{e}"
        await a.delete()
        await message.reply_text("Fᴀɪʟᴇᴅ ᴛᴏ ᴅᴏᴡɴʟᴏᴀᴅ ʀᴇᴇʟ")
        
        # Log the error in the log group
        await app.send_message(LOG_GROUP_ID, error_message) 


__MODULE__ = "ɪɢ-ʀᴇᴇʟ"
__HELP__ = """
**ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟ ᴅᴏᴡɴʟᴏᴀᴅᴇʀ:**

• `/ig [URL]`: ᴅᴏᴡɴʟᴏᴀᴅ ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟs. Pʀᴏᴠɪᴅᴇ ᴛʜᴇ ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟ URL ᴀғᴛᴇʀ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ.
• `/instagram [URL]`: ᴅᴏᴡɴʟᴏᴀᴅ ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟs. Pʀᴏᴠɪᴅᴇ ᴛʜᴇ ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟ URL ᴀғᴛᴇʀ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ.
• `/reel [URL]`: ᴅᴏᴡɴʟᴏᴀᴅ ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟs. Pʀᴏᴠɪᴅᴇ ᴛʜᴇ ɪɴsᴛᴀɢʀᴀᴍ ʀᴇᴇʟ URL ᴀғᴛᴇʀ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ.
"""
