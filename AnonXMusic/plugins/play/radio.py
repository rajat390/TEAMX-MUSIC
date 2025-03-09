import asyncio
import os
import logging
import subprocess
from config import RADIO_STREAM_URL
from pyrogram import Client, filters
from pyrogram.raw import functions, types
from pytgcalls.types.raw import VideoStream
from pytgcalls.types.raw import AudioStream
from AnonXMusic import app 

# Replace with your API credentials and radio stream URL

async def stream_radio(chat_id):
    try:
        call = await app.get_call(chat_id)  # Get an existing call or start a new one.
        if call is None:
            await app.invoke(
                functions.phone.CreateGroupCall(
                    peer=await app.resolve_peer(chat_id),
                    random_id=app.rnd_id(),
                    title="Radio Stream",
                    rtmp_stream=True,
                    video=True,
                    file_reference=b""
                )
            )

            call = await app.get_call(chat_id)

        if call:

            # Using ffmpeg to stream the radio stream to a pipe.
            process = subprocess.Popen(
                ["ffmpeg", "-i", RADIO_STREAM_URL, "-acodec", "pcm_s16le", "-ar", "48000", "-ac", "1", "-f", "s16le", "-"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.DEVNULL
            )

            await app.stream_call(chat_id, AudioPiped(process.stdout))
            try:
    LOGGER.info(f"Started streaming radio to chat {chat_id}")
             # Keep the stream running indefinitely.
             await asyncio.Event().wait() #This is important to keep the stream running.
else:
             LOGGER.error(f"Failed to start/find voice chat in chat {chat_id}")
 
     except Exception as e:
         LOGGER.error(f"An error occurred: {e}")
 
            
@app.on_message(filters.command("startradio"))
async def start_radio_command(client, message):
    try:
        chat_id = message.chat.id
        await stream_radio(chat_id)

    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")

@app.on_message(filters.command("stopradio"))
async def stop_radio_command(client, message):
    try:
        chat_id = message.chat.id
        await app.stop_call(chat_id)
        await message.reply_text("Radio stream stopped.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {e}")

