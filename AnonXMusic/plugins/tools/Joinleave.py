from pyrogram import Client, filters
from pyrogram.errors import BadRequest
from AnonXMusic import app

@app.on_message(filters.new_chat_members)
async def delete_join(client, message):
    """Menghapus pesan bergabung."""
    try:
        await message.delete()
        print(f"Pesan bergabung dihapus di chat ID {message.chat.id}")
    except BadRequest as e:
        print(f"Error menghapus pesan bergabung: {e}")
    except Exception as e:
        print(f"Terjadi error tak terduga: {e}")

@app.on_message(filters.left_chat_member)
async def delete_leave(client, message):
    """Menghapus pesan keluar."""
    try:
        await message.delete()
        print(f"Pesan keluar dihapus di chat ID {message.chat.id}")
    except BadRequest as e:
        print(f"Error menghapus pesan keluar: {e}")
    except Exception as e:
        print(f"Terjadi error tak terduga: {e}")
        
