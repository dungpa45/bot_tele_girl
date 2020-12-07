import json
import re, requests
import random
from telegram.ext import Updater ,CommandHandler, InlineQueryHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, InputTextMessageContent, ReplyKeyboardMarkup
import glob, os
from yaml import Loader
from yaml import load

with open("/home/dung/OSAM/Build_bot/bot_tele_girl/secret.yaml","r") as yml_file:
    data = load(yml_file, Loader=Loader)

reply_keyboard = [['/start']]
markup = ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True)

def get_quote():
    data_quote = requests.get("https://favqs.com/api/qotd").json()
    quote = data_quote["quote"]["body"]
    author = data_quote["quote"]["author"]
    message = r'_"'+quote+r'"_'+"\n\n"+r'*'+author+r'*'
    print(message)
    return message

def start(bot, update):
    user = update.message.from_user
    update.message.reply_text(get_quote(),parse_mode=ParseMode.MARKDOWN, reply_markup=markup)

def help(bot, update):
    update.message.reply_text('''Nothing to help
    _Have fun_ :) ''',ParseMode.MARKDOWN)


def main():
    TOKEN = data["telegram"]["token_quote"]
    updater = Updater(token=TOKEN)
    dp = updater.dispatcher
    start_handler = CommandHandler('start',start)
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(start_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
