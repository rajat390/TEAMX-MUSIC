from pyrogram import filters
from AnonXMusic import YouTube, app
from AnonXMusic.utils.channelplay import get_channeplayCB
from AnonXMusic.utils.decorators.language import languageCB
from AnonXMusic.utils.stream.stream import stream
from config import BANNED_USERS
import logging

# Konfigurasi logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

@app.on_callback_query(filters.command("LiveStream") & filters.group & ~BANNED_USERS)
@languageCB
async def play_live_stream(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    vidid, user_id, mode, cplay, fplay = callback_request.split("|")
    
    # Validasi pengguna
    if CallbackQuery.from_user.id != int(user_id):
        try:
            await CallbackQuery.answer(_["playcb_1"], show_alert=True)
        except Exception as e:
            logging.error(f"Error answering callback query: {e}")
        return
    
    # Mendapatkan detail channel play
    try:
        chat_id, channel = await get_channeplayCB(_, cplay, CallbackQuery)
    except Exception as e:
        logging.error(f"Error getting channel play: {e}")
        return
    
    video = True if mode == "v" else None
    user_name = CallbackQuery.from_user.first_name
    
    try:
        await CallbackQuery.message.delete()
        await CallbackQuery.answer()
    except Exception as e:
        logging.error(f"Error deleting message or answering callback: {e}")
    
    # Memberi tahu pengguna bahwa permintaan sedang diproses
    message_text = _["play_2"].format(channel) if channel else _["play_1"]
    mystic = await CallbackQuery.message.reply_text(message_text)
    
    # Mendapatkan detail video YouTube
    try:
        details, track_id = await YouTube.track(vidid, True)
    except Exception as e:
        logging.error(f"Error getting YouTube track details: {e}")
        await mystic.edit_text(_["play_3"])
        return
    
    ffplay = True if fplay == "f" else None
    
    # Memeriksa apakah video adalah live stream
    if not details["duration_min"]:
        try:
            await stream(
                _,
                mystic,
                user_id,
                details,
                chat_id,
                user_name,
                CallbackQuery.message.chat.id,
                video,
                streamtype="live",
                forceplay=ffplay,
            )
        except Exception as e:
            ex_type = type(e).__name__
            err = e if ex_type == "AssistantErr" else _["general_2"].format(ex_type)
            logging.error(f"Error streaming live video: {e}")
            await mystic.edit_text(err)
            return
    else:
        await mystic.edit_text("» ɴᴏᴛ ᴀ ʟɪᴠᴇ sᴛʀᴇᴀᴍ.")
    
    try:
        await mystic.delete()
    except Exception as e:
        logging.error(f"Error deleting mystic message: {e}")
        
