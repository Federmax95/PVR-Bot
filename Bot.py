import os
import subprocess
import asyncio
from telethon import TelegramClient, events

# Configure bot credentials
API_ID = ""
API_HASH = ""
BOT_TOKEN = ""

bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
OUTPUT_DIR = "recordings"
os.makedirs(OUTPUT_DIR, exist_ok=True)


@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    """Responds to the /start command"""
    await event.reply("Hello! Send me the HLS live stream link and the duration (in seconds) separated by a space.\nExample: `http://yourstream.com/stream.m3u8 30`")


@bot.on(events.NewMessage)
async def record_hls(event):
    """Handles messages to record the HLS live stream"""
    try:
        message = event.message.message.strip()
        if not message:
            return
        parts = message.split()
        if len(parts) != 2:
            await event.reply("Incorrect format. Use: `<URL> <duration in seconds>`")
            return
        url, duration = parts
        if not url.startswith("http") or not duration.isdigit():
            await event.reply("Invalid URL or non-numeric duration.")
            return
        duration = int(duration)
        output_file = os.path.join(
            OUTPUT_DIR, f"recording_{event.sender_id}.mp4")
        command = [
            "ffmpeg",
            "-y",
            "-reconnect", "1",
            "-reconnect_streamed", "1",
            "-reconnect_delay_max", "5",
            "-i", url,
            "-t", str(duration),
            "-bufsize", "2M",
            "-vf", "scale=640:-1",
            "-c:v", "libx264",
            "-preset", "slow",
            "-crf", "28",
            "-b:v", "500k",
            "-c:a", "aac",
            "-b:a", "128k",
            "-strict", "experimental",
            "-max_muxing_queue_size", "1024",
            "-f", "mp4",
            output_file
        ]
        await event.reply("📡 Recording started...")
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=None,
            stderr=None
        )
        await process.wait()
        if process.returncode == 0:
            await event.reply("✅ Recording complete. Sending the file...")
            await bot.send_file(event.chat_id, output_file, caption="Here is your recorded file!")
        else:
            error_message = stderr.decode()
            await event.reply(f"❌ Recording error:\n```{error_message}\n```")
        if os.path.exists(output_file):
            os.remove(output_file)
    except Exception as e:
        await event.reply(f"❌ Error: {str(e)}")
print("Bot started...")
bot.run_until_disconnected()
