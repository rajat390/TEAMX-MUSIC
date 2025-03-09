import asyncio
import os
import logging
import subprocess
from config import RADIO_STREAM_URL
from pyrogram import Client, filters
from pyrogram.raw import functions, types
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
from AnonXMusic import app

# Konfigurasi Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)

async def stream_radio(chat_id):
    try:
        call = await app.get_call(chat_id)
        if call is None:
            try:
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
            except Exception as create_call_error:
                LOGGER.error(f"Failed to create group call: {create_call_error}")
                return

        if call:
            process = subprocess.Popen(
                ["ffmpeg", "-i", RADIO_STREAM_URL, "-acodec", "pcm_s16le", "-ar", "48000", "-ac", "1", "-f", "s16le", "-"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.DEVNULL
            )

            try:
                await app.stream_call(chat_id, AudioPiped(process.stdout))
                LOGGER.info(f"Started streaming radio to chat {chat_id}")
                await asyncio.Event().wait()  # Keep the stream running.
            except Exception as stream_error:
                LOGGER.error(f"Failed to stream: {stream_error}")
            finally:
                process.terminate() #terminate ffmpeg process.
                LOGGER.info("ffmpeg process terminated")

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
        
