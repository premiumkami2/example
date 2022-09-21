
from pyrogram import Client
from pyrogram import filters
from pyrogram import idle
from pyrogram import errors

from pyrogram.types import InlineKeyboardButton as button
from pyrogram.types import InlineKeyboardMarkup as markup
from pyrogram.types import ForceReply as reply

api_id, api_hash = 13360888, "f9f13233c4bff84f6ee3423f58f796a8"
with Client("session_me",api_id,api_hash) as cli:
        cli.send_message("me","Log in session pyrogram")

            

