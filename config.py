import re
import os
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters
import sys
from decouple import config

load_dotenv()

# Configuration using getenv and decouple config
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")

# Get your token from @BotFather on Telegram.
BOT_TOKEN = getenv("BOT_TOKEN")

SESSION = config("SESSION")

BOT_USERNAME = getenv("BOT_USERNAME", "xteam_clonebot")

# Get your mongo url from cloud.mongodb.com
MONGO_DB_URI = getenv("MONGO_DB_URI")

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 240))

# Chat id of a group for logging bot's activities
LOGGER_ID = int(getenv("LOGGER_ID"))

# Get this value from @FallenxBot on Telegram by /id
OWNER_ID = int(getenv("OWNER_ID"))

## Fill these variables if you're deploying on heroku.
# Your heroku app name
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
# Get it from http://dashboard.heroku.com/account
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

UPSTREAM_REPO = config("UPSTREAM_REPO", default=getenv("UPSTREAM_REPO", "https://github.com/xteam-cloner/TEAMX-MUSIC"))
UPSTREAM_BRANCH = config("UPSTREAM_BRANCH", default=getenv("UPSTREAM_BRANCH", "master"))
GIT_TOKEN = config("GIT_TOKEN", default=getenv("GIT_TOKEN", None))
SUPPORT_CHANNEL = config("SUPPORT_CHANNEL", default=getenv("SUPPORT_CHANNEL", "https://t.me/xteam_cloner"))
SUPPORT_CHAT = config("SUPPORT_CHAT", default=getenv("SUPPORT_CHAT", "https://t.me/xteam_cloner"))
PRIVATE_BOT_MODE = config("PRIVATE_BOT_MODE", default=getenv("PRIVATE_BOT_MODE", "False")).lower() in ("true", "1", "t")
AUTO_LEAVING_ASSISTANT = config("AUTO_LEAVING_ASSISTANT", default=getenv("AUTO_LEAVING_ASSISTANT", "False")).lower() in ("true", "1", "t")
SPOTIFY_CLIENT_ID = config("SPOTIFY_CLIENT_ID", default=getenv("SPOTIFY_CLIENT_ID", "e9d00bfcd9a246dabd5c36256ba2302c"))
SPOTIFY_CLIENT_SECRET = config("SPOTIFY_CLIENT_SECRET", default=getenv("SPOTIFY_CLIENT_SECRET", "0f2b27d79dcf4808bcd4f16e5d7a1478"))
PLAYLIST_FETCH_LIMIT = int(config("PLAYLIST_FETCH_LIMIT", default=getenv("PLAYLIST_FETCH_LIMIT", "25")))
TG_AUDIO_FILESIZE_LIMIT = int(config("TG_AUDIO_FILESIZE_LIMIT", default=getenv("TG_AUDIO_FILESIZE_LIMIT", "104857600")))
TG_VIDEO_FILESIZE_LIMIT = int(config("TG_VIDEO_FILESIZE_LIMIT", default=getenv("TG_VIDEO_FILESIZE_LIMIT", "1073741824")))

# Get your pyrogram v2 session from @StringFatherBot on Telegram
STRING1 = getenv("STRING_SESSION", None)
STRING2 = getenv("STRING_SESSION2", None)
STRING3 = getenv("STRING_SESSION3", None)
STRING4 = getenv("STRING_SESSION4", None)
STRING5 = getenv("STRING_SESSION5", None)


RADIO_STREAM_URL = config("RADIO_STREAM_URL", default=getenv("RADIO_STREAM_URL", "https://n0e.radiojar.com/8s5u5tpdtwzuv?rj-ttl=5&rj-tok=AAABjW7yROAA0TUU8cXhXIAi6g"))
START_IMG_URL = config("START_IMG_URL", default=getenv("START_IMG_URL", "https://files.catbox.moe/ib6qvk.mp4"))
PING_IMG_URL = config("PING_IMG_URL", default=getenv("PING_IMG_URL", "https://files.catbox.moe/ib6qvk.mp4"))
PLAYLIST_IMG_URL = "https://telegra.ph/file/8d7b534e34e13316a7dd2.jpg"
STATS_IMG_URL = "https://te.legra.ph/file/e906c2def5afe8a9b9120.jpg"
TELEGRAM_AUDIO_URL = "https://te.legra.ph/file/6298d377ad3eb46711644.jpg"
TELEGRAM_VIDEO_URL = "https://te.legra.ph/file/6298d377ad3eb46711644.jpg"
STREAM_IMG_URL = "https://te.legra.ph/file/bd995b032b6bd263e2cc9.jpg"
SOUNCLOUD_IMG_URL = "https://te.legra.ph/file/bb0ff85f2dd44070ea519.jpg"
YOUTUBE_IMG_URL = "https://te.legra.ph/file/6298d377ad3eb46711644.jpg"
SPOTIFY_ARTIST_IMG_URL = "https://te.legra.ph/file/37d163a2f75e0d3b403d6.jpg"
SPOTIFY_ALBUM_IMG_URL = "https://te.legra.ph/file/b35fd1dfca73b950b1b05.jpg"
SPOTIFY_PLAYLIST_IMG_URL = "https://te.legra.ph/file/95b3ca7993bbfaf993dcb.jpg"
REDIS_URI = config("REDIS_URI", default=None) or config("REDIS_URL", default=None)
REDIS_PASSWORD = config("REDIS_PASSWORD", default=None)
ADDONS = config("ADDONS", default=False, cast=bool)
VCBOT = config("VCBOT", default=False, cast=bool)
REDISPASSWORD = config("REDISPASSWORD", default=None)
REDISHOST = config("REDISHOST", default=None)
REDISPORT = config("REDISPORT", default=None)
REDISUSER = config("REDISUSER", default=None)
DATABASE_URL = config("DATABASE_URL", default=None)

# Ensure required environment variables are loaded
if not STRING1:
    raise ValueError("STRING_SESSION environment variable is missing")

# Helper functions
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60**i for i, x in enumerate(reversed(stringt.split(":"))))

DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))

if SUPPORT_CHANNEL and not re.match(r"(?:http|https)://", SUPPORT_CHANNEL):
    raise SystemExit("[ERROR] - Your SUPPORT_CHANNEL URL is incorrect. Please ensure it starts with https://")

if SUPPORT_CHAT and not re.match(r"(?:http|https)://", SUPPORT_CHAT):
    raise SystemExit("[ERROR] - Your SUPPORT_CHAT URL is incorrect. Please ensure it starts with https://")

# Global variables
BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}
