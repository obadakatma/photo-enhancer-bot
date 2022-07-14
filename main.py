import cv2 as cv
import numpy as np
import telegram
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

# import Token  # File that contain my telegram bot token
import Token

token = Token.Token
bot = telegram.Bot(token=token)
updater = Updater(token, use_context=True)


def start(update: Update, context: CallbackContext):
    bot.send_message(chat_id=update.message.chat_id, text="Hello and welcome to PhotoEnhance_bot.\nThis bot will "
                                                          "enhance your photo and make it "
                                                          "look prettier.\n All you need to do to upload the photo "
                                                          "you need to enhance and you "
                                                          "will receive the enhanced photo.\n Please enjoy.")


def enhanced_photo(update, context):
    img = cv.imread("temp_photo.jpg")
    dst = cv.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 21)
    cv.imwrite("enhanced_photo.jpg", dst, [cv.IMWRITE_JPEG_QUALITY, 100])
    bot.sendPhoto(chat_id=update.message.chat_id, photo=open("enhanced_photo.jpg", 'rb'))


def image_handler(update, context):
    file = update.message.photo[-1].file_id
    obj = context.bot.get_file(file)
    obj.download(custom_path="temp_photo.jpg")
    update.message.reply_text("Image received.\nWe are working on it.")
    enhanced_photo(update=update, context=context)


# when "/start" command sent to the bot , start function will be called
updater.dispatcher.add_handler(CommandHandler('start', start))
# when photo sent to the bot , image_handler function will be called
updater.dispatcher.add_handler(MessageHandler(Filters.photo, image_handler))

updater.start_polling()
