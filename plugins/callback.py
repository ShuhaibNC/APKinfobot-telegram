from pyrogram import Client
from pyrogram.types import CallbackQuery
import asyncio
import os
from .commands import get_image_data, getfullreport
from io import BytesIO

# Handle callback queries
@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == 'ic_launcher':
        ic_out_name = f"{query.from_user.id}.jpg"
        image_data = get_image_data()

        if image_data:
            n_image_data = BytesIO(image_data)
            await client.send_photo(chat_id=query.message.chat.id, photo=n_image_data)
        else:
            await query.answer("No image data available!", show_alert=True)
        return

    elif query.data == 'full_report':
        out_name = f"{query.from_user.id}.txt"
        full_report = getfullreport()

        if full_report:
            # Write and send the full report asynchronously to avoid blocking
            await asyncio.to_thread(write_full_report, out_name, full_report)
            await client.send_document(chat_id=query.message.chat.id, document=out_name, caption="FULL REPORT 📄")

            # Ensure the file is deleted after it's sent
            await asyncio.sleep(1)
            await asyncio.to_thread(delete_file, out_name)

# Helper function for writing report to a file
def write_full_report(file_name, report_content):
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(report_content)

# Helper function for non-blocking file deletion
def delete_file(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)
