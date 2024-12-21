from pyrogram import Client, filters
from pyrogram.types import *
import Script
import time
from pyaxmlparser import APK
import os
from func import calculate_hashes, generate_apk_report, progress
import asyncio 
import shutil

class Appstate:
    def __init__(self):
        self._image_data = None
        self._report_ = None
        
appstate = Appstate()

# Asynchronous file deletion to avoid blocking
async def del_path(path):
    if not os.path.exists(path):
        return
    if os.path.isfile(path) or os.path.islink(path):
        await asyncio.to_thread(os.unlink, path)  # Non-blocking deletion
    else:
        await asyncio.to_thread(shutil.rmtree, path)  # Non-blocking directory removal

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
    analyze = await message.reply(f"📦 **Analyzing {message.document.file_name}...**")
    
    # Non-blocking media download
    download_location = await client.download_media(
        message=message,
        file_name='./',
        progress=progress
    )
    
    await msg.delete()
    
    try:
        apk = APK(download_location)
        md5, sha = calculate_hashes(download_location)

        appstate._image_data = apk.icon_data
        await analyze.delete()

        buttons = [
            [InlineKeyboardButton('🌆 Launcher icon', callback_data='ic_launcher'),
            InlineKeyboardButton('📄 Full Report', callback_data='full_report')],
            [InlineKeyboardButton('🦠 Virus Total', url=f"https://www.virustotal.com/gui/search/{md5}")]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)

        # APK Report Reply
        await message.reply(
            f"\n\n**📃 APK ANALYZED REPORT 📃**\n\n"
            f"**📂 File Name**: `{message.document.file_name}`\n\n"
            f"**📛 App Name:** `{apk.application}`\n\n"
            f"**📦 Package Name:** `{apk.package}`\n\n"
            f"**🆚 Version Code:** `{apk.version_code}`\n\n"
            f"**🆚 Version Name:** `{apk.version_name}`\n\n"
            f"**🌆 Icon info:** `{apk.icon_info}`\n\n"
            f"**#️⃣ MD5:** `{md5}`\n\n"
            f"**#️⃣ SHA256:** `{sha}`",
            reply_markup=reply_markup
        )

        # Move report generation to background task to avoid blocking
        asyncio.create_task(process_and_cleanup(download_location))

    except Exception as e:
        await message.reply(f"Error analyzing APK: {e}")
        print(f"Error: {e}")

# Move full report generation and cleanup to a background task
async def process_and_cleanup(download_location):
    print("Started full analyze...", download_location)
    appstate._report_ = generate_apk_report(download_location)
    print("Trying to delete file", download_location)

    # Non-blocking sleep and delete
    await asyncio.sleep(1)
    await del_path(download_location)
    print("Successfully deleted", download_location)
