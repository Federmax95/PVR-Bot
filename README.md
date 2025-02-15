# Telegram HLS Recording Bot

This is a Telegram bot built with Telethon that allows users to record live HLS streams using FFmpeg. Users can send a stream URL and a duration, and the bot will record the stream and send back the recorded file.

## Features
- Accepts HLS stream links and recording duration from users
- Uses FFmpeg to record the stream
- Sends the recorded file to the user via Telegram
- Deletes the recorded file after sending

## Requirements
- Python 3.8+
- FFmpeg installed and accessible via command line
- A Telegram bot token from [BotFather](https://t.me/BotFather)
- A Telegram API ID and API Hash from [my.telegram.org](https://my.telegram.org)

## Installation
1. Clone this repository:
   ```sh
   git clone https://github.com/Federmax95/PVR-Bot.git
   cd PVR-Bot
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Create and configure your Telegram bot by setting up API credentials in `Bot_finale.py`:
   ```python
   API_ID = "YOUR_API_ID"
   API_HASH = "YOUR_API_HASH"
   BOT_TOKEN = "YOUR_BOT_TOKEN"
   ```
4. Ensure FFmpeg is installed and available in your system's PATH.

## Usage
1. Run the bot:
   ```sh
   python Bot_finale.py
   ```
2. Start the bot on Telegram and send a message in the format:
   ```
   http://example.com/stream.m3u8 30
   ```
   (where `30` is the duration in seconds)
3. The bot will record the stream and send you the recorded file.

## FFmpeg Command Details
The bot executes the following FFmpeg command to record the stream:
```sh
ffmpeg -y -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -i <URL> -t <DURATION> -bufsize 2M -vf "scale=640:-1" -c:v libx264 -preset slow -crf 28 -b:v 500k -c:a aac -b:a 128k -strict experimental -max_muxing_queue_size 1024 -f mp4 <OUTPUT_FILE>
```

## Notes
- The bot creates a `recordings` directory to store temporary files.
- Recorded files are deleted after being sent to the user.
- Ensure FFmpeg is installed and correctly configured on your system.

## License
This project is licensed under the MIT License.

## Contributing
Pull requests are welcome! If you have suggestions or find issues, feel free to open an issue or submit a PR.

