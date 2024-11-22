import re
import requests
from pyrogram import filters
from BADMUSIC import app
from config import LOG_GROUP_ID


@app.on_message(filters.command(["ig", "instagram", "reel"]))
async def download_instagram_video(client, message):
    if len(message.command) < 2:
        await message.reply_text("Please provide the Instagram reel URL after the command.")
        return

    url = message.text.split()[1]

    if not re.match(r"^(https?://)?(www\.)?(instagram\.com|instagr\.am)/(p|reel|tv|stories)/.*$", url):
        await message.reply_text("The provided URL is not a valid Instagram URL.")
        return

    a = await message.reply_text("Processing your request...")

    api_url = f"https://insta-dl.hazex.workers.dev/?url={url}"

    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code != 200:
            await a.edit("Failed to connect to the API. Please try again later.")
            return

        result = response.json()
        if result.get("error"):
            await a.edit(f"API Error: {result.get('message', 'Unknown error occurred.')}")
            return

        data = result["result"]
        video_url = data["url"]
        duration = data.get("duration", "Unknown")
        quality = data.get("quality", "Unknown")
        file_type = data.get("extension", "Unknown")
        size = data.get("formattedSize", "Unknown")

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
