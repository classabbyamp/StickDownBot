"""
stickdownbot

Copyright (c) 2020 classabbyamp
Released under the BSD-3-Clause license
"""


import logging
from io import BytesIO, BufferedReader

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from data import keys


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


def start(update, context):
    update.message.reply_text("Send me stickers, and I'll convert them to PNGs!")


def help_command(update, context):
    update.message.reply_text("Send me stickers, and I'll convert them to PNGs!")


def get_sticker(update, context):
    sticker = update.message.sticker
    if not sticker.is_animated:
        sticker_file = sticker.get_file()
        pack = sticker.set_name
        uid = sticker.file_unique_id
        filename = f"{pack if pack is not None}{'_' if pack is not None}{uid}.png"
        caption = f"t.me/addstickers/{pack}" if pack is not None else ""
        with BytesIO() as sticker_obj:
            sticker_file.download(out=sticker_obj)
            sticker_obj.seek(0)
            update.message.reply_document(document=sticker_obj, filename=filename, caption=caption)


if __name__ == "__main__":
    updater = Updater(keys.tg_token, use_context=True)

    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help_command))
    dp.add_handler(MessageHandler(Filters.sticker, get_sticker))

    updater.start_polling()
    updater.idle()
