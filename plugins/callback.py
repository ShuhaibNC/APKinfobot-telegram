import asyncio
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import time
import config
import Script
import os
from func import *
from .commands import get_image_data, getfullreport
from io import BytesIO

#callback handle
@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery ):
    if query.data == 'ic_launcher':
        image_data = get_image_data()
        if image_data:
            n_image_data = BytesIO()
            n_image_data.write(image_data)
            n_image_data.name = "photo.jpg"
            await client.send_photo(
                chat_id=query.message.chat.id, photo=n_image_data
            )
            return
        else:
            await query.answer("No image data available!", show_alert=True)
            return
    elif query.data == 'full_report':
        out_name = "apkreport.txt"
        full_report = getfullreport()
        with open(out_name, "w", encoding="utf-8") as f:
            f.write(full_report)
        await client.send_document(
            chat_id=query.message.chat.id,
            document=out_name,
            caption="FULL REPORT 📄"
        )
        if os.path.exists(out_name):
             os.remove(out_name)