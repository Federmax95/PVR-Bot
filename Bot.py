import os
import subprocess
import asyncio
from telethon import TelegramClient, events
API_ID = ""
API_HASH = ""
BOT_TOKEN = ""
bot = TelegramClient('bot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)
OUTPUT_DIR = "recordings"
os.makedirs(OUTPUT_DIR, exist_ok=True)


@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    await event.reply("Hi! Send me link of the live and the duration in seconds separated by a space.\nExample: `http://example.live/stream.m3u8 30`")


@bot.on(events.NewMessage)
async def record_hls(event):
    try:
        message = event.message.message.strip()
        if not message:
            return
        parts = message.split()
        if len(parts) != 2:
            await event.reply("Format error. Use: `<URL> <duration in second>`")
            return
        url, duration = parts
        if not url.startswith("http") or not duration.isdigit():
            await event.reply("URL not valid or duration not valid.")
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
            await event.reply("✅ Recording completed. Sending File...")
            await bot.send_file(event.chat_id, output_file, caption="Ecco il tuo file registrato!")
        else:
            error_message = stderr.decode()
            await event.reply(f"❌ Error during recording:\n```\n{error_message}\n```")
        if os.path.exists(output_file):
            os.remove(output_file)
    except Exception as e:
        await event.reply(f"❌ Error: {str(e)}")
print("Bot in execution")
bot.run_until_disconnected()
