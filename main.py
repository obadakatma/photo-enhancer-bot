"""
This bot developed by Obada Katma
"""

import aspose.words as aw
from PIL import Image, ImageEnhance
from cryptography.fernet import Fernet

import telegram
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters

# import Token  # File that contain my telegram bot token
import Token

encryptedFiles = ['temp_photo.png', 'enhanced_photo.png', 'enhanced_photo.pdf']

token = Token.Token
bot = telegram.Bot(token=token)
updater = Updater(token, use_context=True)


def start(update: Update, context: CallbackContext):
    bot.send_message(chat_id=update.message.chat_id, text="Hello and welcome to PhotoEnhance_bot.\nThis bot will "
                                                          "enhance your photo and make it "
                                                          "look prettier.\nAll you need to do to upload the photo "
                                                          "you need to enhance and you "
                                                          "will receive the enhanced photo.\nType /about to know who "
                                                          "developed this bot and more information about the bot."
                                                          "\nPlease enjoy.")


def about(update: Update, context: CallbackContext):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="Welcome to PhotoEnhance_bot.\nBot developer:@obadaalkatma\nBe sure that all your files are "
                         "encrypted.\nSome images may not be enhanced,so we are sorry about that and we are working "
                         "to improve it.")


def enhanced_photo(update, context):
    # Enhancing the image.
    img = Image.open("temp_photo.png")
    img_con = ImageEnhance.Contrast(img)
    image = img_con.enhance(1.3)
    image.save('enhanced_photo.png', format='png')
    # Saving the image as PDF file.
    doc = aw.Document()
    builder = aw.DocumentBuilder(doc)
    builder.insert_image("enhanced_photo.png")
    doc.save("enhanced_photo.pdf")
    # Sending the image.
    bot.sendMessage(chat_id=update.message.chat_id, text="Enhanced photo : ")
    bot.send_document(chat_id=update.message.chat_id, document=open('enhanced_photo.pdf', 'rb'), timeout=100)
    bot.sendMessage(chat_id=update.message.chat_id, text="enhanced photo as png : ")
    bot.send_photo(chat_id=update.message.chat_id, photo=open('enhanced_photo.png', 'rb'))


def image_handler(update, context):
    # Getting the file of sent image and save it.
    file = update.message.photo[-1].file_id
    obj = context.bot.get_file(file)
    obj.download(custom_path="temp_photo.png")

    update.message.reply_text("Image received.\nWe are working on it.")
    enhanced_photo(update=update, context=context)
    bot.sendMessage(chat_id=update.message.chat_id, text="Be sure that all your files are encrypted.\nThanks for "
                                                         "using our service 😊")
    # encrypting all files.
    for element in encryptedFiles:
        key = Fernet.generate_key()

        with open('filekey.key', 'wb') as filekey:
            filekey.write(key)

        with open('filekey.key', 'rb') as filekey:
            key = filekey.read()

        fernet = Fernet(key)

        with open(element, 'rb') as file:
            original = file.read()

        encrypted = fernet.encrypt(original)

        with open(element, 'wb') as encrypted_file:
            encrypted_file.write(encrypted)


def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text("Sorry I can't understand what are you saying")


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text("Sorry '%s' is not a valid command" % update.message.text)


# when "/start" command sent to the bot , start function will be called
updater.dispatcher.add_handler(CommandHandler('start', start))
# when "/about" command sent to the bot , about function will be called
updater.dispatcher.add_handler(CommandHandler('about', about))
# when photo sent to the bot , image_handler function will be called
updater.dispatcher.add_handler(MessageHandler(Filters.photo, image_handler))
# Filters out unknown commands
updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))
# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

updater.start_polling()
