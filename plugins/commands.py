from pyrogram import *
from pyrogram.types import *
import Script
import time
from pyaxmlparser import APK
import math
import os
import subprocess
from func import *

_image_data = None  # Private variable
_report_ = None
# Function to set image_data
def set_image_data(data):
    global _image_data  # Use global to modify it
    _image_data = data

# Function to get image_data
def get_image_data():
    return _image_data

def setfullreport(data):
        global _report_
        _report_ = data
def getfullreport():
    return _report_

def del_path(path):
     if not os.path.exists(path):
         return
     if os.path.isfile(path) or os.path.islink(path):
         os.unlink(path)
     else:
         shutil.rmtree(path)


#ping
@Client.on_message(filters.command('ping') & filters.incoming)
async def ping(client, message):
                start_time = time.time()
                m = await message.reply('Pinging....')
                end_time = time.time()
                elapsed_time = (end_time - start_time) * 1000
                await m.edit(f'Pong!\n{elapsed_time:.3f}ms')
                
@Client.on_message(filters.command('start') & filters.incoming)
async def start(client, message):
                await message.reply(Script.START_TEXT)
                
@Client.on_message(filters.command('help') & filters.incoming)
async def help(client, message):
                await message.reply(Script.HELP_TEXT)


@Client.on_message(filters.document)
async def download_telegram_media(client, message):
        msg = await client.send_message(
	  chat_id=message.chat.id,
	  text='File started to download...'
	)
        analyze = await message.reply("📦 **Analyzing apk file...**")
        start_time = time.time()
        download_location = await client.download_media(
        message=message,
        file_name='./',
        progress=progress
        )
        await msg.delete()
        apk = APK(download_location)
        md5 = calculate_md5(download_location)
        sha = calculate_sha256(download_location)
        
        set_image_data(apk.icon_data)
        
        await analyze.delete()
        buttons = [
            [
                InlineKeyboardButton('🌆 Launcher icon ', callback_data='ic_launcher')
            ],
            [
                InlineKeyboardButton('📄 Full Report ', callback_data='full_report')
                ],
            [
                InlineKeyboardButton('🦠 Virus Total', url=f"https://www.virustotal.com/gui/search/{md5}"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply("\n\n**📃 APK ANALYZED REPORT 📃**\n\n**📂 File Name**: `{}`\n\n**📛 App Name: ** `{}`\n\n**📦 Package Name:** `{}`\n\n**🆚 Version Code: ** `{}`\n\n**🆚 Version Name: ** `{}`\n\n**🌆 Icon info: ** `{}`\n\n**#️⃣ MD5:** `{}`\n\n**#️⃣ SHA256:** `{}`".format(message.document.file_name, apk.application, apk.package, apk.version_code, apk.version_name, apk.icon_info, md5, sha), reply_markup=reply_markup)
        print("Started full analyze...", download_location)
        setfullreport(generate_apk_report(download_location))
        print("Trying to delete file", download_location)
        time.sleep(1)
        del_path(download_location)
        print("Successfully deleted", download_location)
        