from pyrogram import Client, filters
from pyrogram.errors import BadRequest
from AnonXMusic import app

@app.on_message(filters.chat_type(["group", "supergroup"]) & filters.new_chat_members)
async def delete_join(client, message):
    """Deletes join messages."""
    try:
        await message.delete()
        print(f"Deleted join message in chat ID {message.chat.id}")
    except BadRequest as e:
        print(f"Error deleting join message: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

@app.on_message(filters.chat_type(["group", "supergroup"]) & filters.left_chat_member)
async def delete_leave(client, message):
    """Deletes leave messages."""
    try:
        await message.delete()
        print(f"Deleted leave message in chat ID {message.chat.id}")
    except BadRequest as e:
        print(f"Error deleting leave message: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

@app.on_message(filters.chat_type(["group", "supergroup"]) & (filters.new_chat_members | filters.left_chat_member))
async def delete_join_leave(client, message):
    """Deletes both join and leave messages."""
    try:
        await message.delete()
        print(f"Deleted join/leave message in chat ID {message.chat.id}")
    except BadRequest as e:
        print(f"Error deleting join/leave message: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
