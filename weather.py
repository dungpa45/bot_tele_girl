import json
import requests
from datetime import datetime
from telegram import ParseMode
from telegram.ext import Updater
TOKEN = "876374897:AAGL2K9-sUb_7mnVso8WddzlYn69_9bIsHg"
USER_ID = "-1001468916747"
TELEGRAM_URL = "https://api.telegram.org/bot{}/sendMessage".format(TOKEN)
API_key = '55c03daa40e239aa99126c8d7b6dbcb0'
place = "Hanoi"
content = requests.get('http://api.openweathermap.org/data/2.5/weather?q={}&lang=vi&appid={}'.format(place,API_key))
degree_sign= u'\N{DEGREE SIGN}' + "C"

thunderstorm = u'\U0001F4A8'    # Code: 200's, 900, 901, 902, 905
drizzle = u'\U0001F4A7'         # Code: 300's
rain = u'\U00002614'            # Code: 500's
snowflake = u'\U00002744'       # Code: 600's snowflake
snowman = u'\U000026C4'         # Code: 600's snowman, 903, 906
atmosphere = u'\U0001F301'      # Code: 700's foogy
clearSky = u'\U00002600'        # Code: 800 clear sky
fewClouds = u'\U000026C5'       # Code: 801 sun behind clouds
clouds = u'\U00002601'          # Code: 802-803-804 clouds general
hot = u'\U0001F525'             # Code: 904
defaultEmoji = u'\U0001F300'    # default emojis

def getEmoji(weatherID):
    if weatherID:
        if str(weatherID)[0] == '2' or weatherID == 900 or weatherID==901 or weatherID==902 or weatherID==905:
            return thunderstorm
        elif str(weatherID)[0] == '3':
            return drizzle
        elif str(weatherID)[0] == '5':
            return rain
        elif str(weatherID)[0] == '6' or weatherID==903 or weatherID== 906:
            return snowflake + ' ' + snowman
        elif str(weatherID)[0] == '7':
            return atmosphere
        elif weatherID == 800:
            return clearSky
        elif weatherID == 801:
            return fewClouds
        elif weatherID==802 or weatherID==803 or weatherID==804:
            return clouds
        elif weatherID == 904:
            return hot
        else:
            return defaultEmoji

def process_message(input):
    try:
        # Loading JSON into a string
        raw_json = json.loads(input)
        # Outputing as JSON with indents
        output = json.dumps(raw_json, indent=4)
    except:
        output = input
    return output

def temp_K_to_C(temp):
    return int(temp - 273.15)

def unix_time_to_UTC(time):
    return datetime.fromtimestamp(time).strftime('%H:%M:%S')

data = content.json()
weather_id = data["weather"][0]["id"]

emoji = getEmoji(weather_id)
weather = data["weather"][0]["main"]
weather_des = data["weather"][0]["description"]
main = data["main"]
temp = temp_K_to_C(main['temp'])
feels = temp_K_to_C(main["feels_like"])
temp_min = temp_K_to_C(main["temp_min"])
tepm_max = temp_K_to_C(main["temp_max"])
humidity = main["humidity"]
wind = data["wind"]
sunrise = unix_time_to_UTC(data["sys"]["sunrise"])
sunset = unix_time_to_UTC(data["sys"]["sunset"])
# print(main.keys())
# print(main.values())

print(content.json())

# print(weather,weather_des,temp,feels,main["feels_like"]-273.15)

tmp = "Thời tiết hôm nay"+ \
    "\n"+ emoji + emoji + emoji +\
    "\nNhiệt độ: "+str(temp)+degree_sign+\
    "\nCao nhất: "+str(temp_min)+degree_sign+" - Thấp nhất: "+str(tepm_max)+degree_sign+\
    "\nCảm giác như: "+str(feels)+degree_sign+\
    "\nĐộ ẩm: "+str(humidity)+"%"+\
    "\nThời tiết: " +weather_des +\
    "\nMặt trời: "+str(sunrise)+" - "+str(sunset)

message = process_message(tmp)

payload = {
    "text": message.encode("utf8"),
    "chat_id": USER_ID
}

requests.post(TELEGRAM_URL, payload)
# chat_id = update.message.chat_id
# bot.sendMessage(chat_id=chat_id,text="a")