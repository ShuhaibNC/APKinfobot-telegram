from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import time
import os
from func import *
from .commands import get_image_data, getfullreport, del_path
from io import BytesIO

#callback handle
@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery ):
    if query.data == 'ic_launcher':
        ic_out_name = str(query.from_user.id) + ".jpg"
        image_data = get_image_data()
        if image_data:
            n_image_data = BytesIO()
            n_image_data.write(image_data)
            n_image_data.name = ic_out_name
            await client.send_photo(
                chat_id=query.message.chat.id, photo=n_image_data
            )
            return
        else:
            await query.answer("No image data available!", show_alert=True)
            return
    elif query.data == 'full_report':
        out_name = str(query.from_user.id) + ".txt"
        full_report = getfullreport()
        print("Report file name: "+out_name)
        with open(out_name, "w", encoding="utf-8") as f:
            f.write(full_report)
        await client.send_document(
            chat_id=query.message.chat.id,
            document=out_name,
            caption="FULL REPORT 📄"
        )
        time.sleep(1)
        if os.path.exists(out_name):
             os.remove(out_name)