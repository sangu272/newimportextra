import re
import requests
from pyrogram import filters
from BADMUSIC import app
from config import LOG_GROUP_ID

INSTAGRAM_API = "https://insta-dl.hazex.workers.dev/?url="  # Primary API URL


@app.on_message(filters.command(["ig", "instagram", "reel"]))
async def download_instagram_video(client, message):
    if len(message.command) < 2:
        await message.reply_text("Please provide the Instagram reel URL after the command.")
        return

    # Extract and validate the Instagram URL
    url = message.text.split()[1]
    if not re.match(r"^(https?://)?(www\.)?(instagram\.com|instagr\.am)/(p|reel|tv|stories)/.*$", url):
        await message.reply_text("The provided URL is not a valid Instagram URL.")
        return

    a = await message.reply_text("Processing your request...")

    try:
        # Make API request
        response = requests.get(f"{INSTAGRAM_API}{url}", timeout=10)
        if response.status_code != 200:
            await a.edit("The API is not responding or returned an error. Please try again later.")
            return

        # Parse the API response
        result = response.json()
        if result.get("error"):
            await a.edit(f"API Error: {result.get('message', 'Unknown error occurred.')}")
            return

        # Extract video details
        data = result.get("result")
        if not data or not data.get("url"):
            await a.edit("Failed to fetch the video details. The API might not support this URL.")
            return

        video_url = data["url"]
        duration = data.get("duration", "Unknown")
        quality = data.get("quality", "Unknown")
        file_type = data.get("extension", "Unknown")
        size = data.get("formattedSize", "Unknown")

        # Prepare caption
        caption = (
            f"**Duration:** {duration}\n"
            f"**Quality:** {quality}\n"
            f"**Type:** {file_type}\n"
            f"**Size:** {size}"
        )

        await a.delete()
        await message.reply_video(video_url, caption=caption)

    except requests.exceptions.Timeout:
        await a.edit("The API request timed out. Please try again later.")

    except requests.exceptions.RequestException as e:
        await a.edit(f"Request failed: {str(e)}")
        await app.send_message(LOG_GROUP_ID, f"Request Exception: {str(e)}")

    except Exception as e:
        await a.edit("An unexpected error occurred.")
        await app.send_message(LOG_GROUP_ID, f"Unexpected Error: {str(e)}")


__MODULE__ = "IG-Reel"
__HELP__ = """
Instagram Reel Downloader:

• `/ig [URL]`: Download Instagram reels.
• `/instagram [URL]`: Download Instagram reels.
• `/reel [URL]`: Download Instagram reels.
"""
