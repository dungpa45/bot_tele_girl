import json
import re, requests
import random
from telegram.ext import Updater ,CommandHandler, InlineQueryHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode, InputTextMessageContent, ReplyKeyboardMarkup

reply_keyboard = [['/quiz','/random_country']]
markup = ReplyKeyboardMarkup(reply_keyboard,one_time_keyboard=True)

data_all = requests.get("https://restcountries.eu/rest/v2/all").json()


def flag(code):
    OFFSET = 127462 - ord('A')
    code = code.upper()
    flag_emo = chr(ord(code[0]) + OFFSET) + chr(ord(code[1]) + OFFSET)
    return flag_emo

def get_info_by_name(search_name):
    name_url = "https://restcountries.eu/rest/v2/name/{}".format(search_name)
    l_info = requests.get(name_url).json()
    l_region_info = []
    for info in l_info:
        name = info["name"]
        code2 = info["alpha2Code"].lower()
        icon = " "+flag(code2)
        capital = info["capital"]
        spelling = ", ".join(info["altSpellings"])
        region = info["region"]
        subregion = info["subregion"]
        population = info["population"]
        demonym = info["demonym"] #dan toc
        area = info["area"]
        timezone = ", ".join(info["timezones"])
        borders = ", ".join(info["borders"]) #bien gioi
        languages =", ".join(lang["name"] for lang in info["languages"])
        currencies = ", ".join(curr["name"] for curr in info["currencies"])
        gini = info["gini"] #chi so binh dang thu nhap
        regionalBlocs = ", ".join(trade["name"] for trade in info["regionalBlocs"])
        regionalBlocs_acronym = ", ".join(trade["acronym"] for trade in info["regionalBlocs"])
        domain = info["topLevelDomain"][0]
        callingcode = info["callingCodes"][0]
    
        temp = "_Information about:_ "+"*"+name+"*"+icon+icon+\
            "\nSpelling: "+spelling+\
            "\nCapital: "+capital+\
            "\nRegion: "+region+" - Subregion: "+subregion+\
            "\nPopulation: "+str(population)+\
            "\nDemonym: "+demonym+\
            "\nArea: "+str(area)+" km2"+\
            "\nTimezone: "+timezone+\
            "\nBorders: "+borders+\
            "\nLanguage: "+languages+\
            "\nCurrencies: "+currencies+\
            "\nTrade blocs: "+regionalBlocs+" - "+regionalBlocs_acronym+\
            "\nincome inequality: "+str(gini)+\
            "\nTop level Domain: "+domain+\
            "\nCalling code: "+callingcode
        l_region_info.append(temp)
    return l_region_info

def get_country_by_capital(name_cap):
    name_url = "https://restcountries.eu/rest/v2/capital/{}".format(name_cap)
    l_data = requests.get(name_url).json()
    l_region = []
    for data in l_data:
        name = data["name"]
        code2 = data["alpha2Code"].lower()
        icon = " "+flag(code2)
        capital = data["capital"]
        temp = "*"+name+"*"+icon+icon+"\n"+capital
        l_region.append(temp)
    return l_region

def start(bot, update):
    user = update.message.from_user
    update.message.reply_text('''Hello {} \nYou can type name of country you want find more information.
    You want to play, let press quiz.
    \nPlease type keyword with English'''.format(user.full_name), reply_markup=markup)

def help(bot, update):
    update.message.reply_text('''Help:
    You want to find all info about country: info <country>
    You want to find country with capital: cap <capital>

    _Have fun_ :) ''',ParseMode.MARKDOWN)

def rep(bot, update):
    user_text = update.message.text
    input_text = user_text.split(" ")
    print(input_text, type(input_text),input_text[0])
    
    if input_text[0] == "info":
        info_data = "\n\n".join(get_info_by_name(input_text[1]))
        update.message.reply_text(info_data,ParseMode.MARKDOWN)
    elif input_text[0] == "cap":
        name_region = "\n".join(get_country_by_capital(input_text[1]))
        update.message.reply_text(name_region,ParseMode.MARKDOWN)
    else:
        update.message.reply_text("*incorrect syntax*\nYou can type /help for guide",ParseMode.MARKDOWN)

def quiz(bot,update):
    button = [[InlineKeyboardButton("VN",callback_data="Viet Nam"),
               InlineKeyboardButton("ENG",callback_data="England")
            ]]
    reply_markup = InlineKeyboardMarkup(button)
    update.message.reply_text("text",reply_markup=reply_markup)
    
def button(bot, update):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Selected option: {}".format(query.data))


def main():
    TOKEN = "1160546832:AAGOlNtpsTmJMho90BHtcnRfjCnaGtMCmRw"
    updater = Updater(token=TOKEN)
    dp = updater.dispatcher
    start_handler = CommandHandler('start',start)
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('quiz', quiz))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text,rep))
    dp.add_handler(start_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()