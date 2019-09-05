from telegram.ext import Updater ,CommandHandler, InlineQueryHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
import requests, re, os
from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, ReplyKeyboardMarkup
from PIL import Image 
import glob, cv2, random

reply_keboard = [['/girl','/woman','/vsbg']]
markup = ReplyKeyboardMarkup(reply_keboard,one_time_keyboard=True)

CHOOSE = 1

def get_girl_img():
    img_dir = "F:\ANH\Girls\GaiChauA"
    data_path = os.path.join(img_dir,'*.jpg')
    files = glob.glob(data_path)
    img_ = random.choice(files)
    img = img_.replace('\\','/')
    return img

def get_woman_img():
    img_dir = "F:\ANH\Girls\GaiXinhChonLoc"
    data_path = os.path.join(img_dir,'*.jpg')
    files = glob.glob(data_path)
    img_ = random.choice(files)
    img = img_.replace('\\','/')
    return img

def get_vsbg_img():
    img_dir = "F:\ANH\Girls\VSBG"
    data_path = os.path.join(img_dir,'*.jpg')
    files = glob.glob(data_path)
    img_ = random.choice(files)
    img = img_.replace('\\','/')
    return img

def start(bot,update):
    user = update.message.from_user
    update.message.reply_text(
        "Hello master {} \nType /gái /sexygirl /girl /vsbg /woman to see random picture\nHave fun :)".format(user.full_name),
        reply_markup=markup)

def girl(bot,update):
    girl = get_girl_img()
    #Get the recipient’s ID
    chat_id = update.message.chat_id
    mess_id = update.message.message_id
    #it’s time to send the message, which is an image.
    bot.send_photo(chat_id=chat_id,reply_to_message_id=mess_id, photo=open(girl,"rb"))

def woman(bot,update):
    woman = get_woman_img()
    #Get the recipient’s ID
    chat_id = update.message.chat_id
    mess_id = update.message.message_id
    #it’s time to send the message, which is an image.
    bot.send_photo(chat_id=chat_id,reply_to_message_id=mess_id, photo=open(woman,"rb"))
    
def vsbg(bot,update):
    vsbg = get_vsbg_img()
    #Get the recipient’s ID
    chat_id = update.message.chat_id
    mess_id = update.message.message_id
    #it’s time to send the message, which is an image.
    bot.send_photo(chat_id=chat_id,reply_to_message_id=mess_id, photo=open(vsbg,"rb"))

def main():
    TOKEN = "876374897:AAGL2K9-sUb_7mnVso8WddzlYn69_9bIsHg"
    # PORT = int(os.environ.get('PORT', '8443'))
    updater = Updater(TOKEN)
    
    dp = updater.dispatcher
    start_handler = CommandHandler('start',start)
    dp.add_handler(CommandHandler('girl',girl))
    dp.add_handler(CommandHandler('gái',girl))
    dp.add_handler(CommandHandler('woman',woman))
    dp.add_handler(CommandHandler('gái',woman))
    dp.add_handler(CommandHandler('vsbg',vsbg))
    dp.add_handler(CommandHandler('sexygirl',vsbg))
    dp.add_handler(start_handler)
    # dp.add_handler(conv_handler)
    #start the bot
    updater.start_polling()
    #Run the bot until press ctrl +C
    updater.idle()
    
if __name__ == '__main__':
    main()