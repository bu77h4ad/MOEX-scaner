#!/usr/bin/python3

import requests
import json
from pprint import pprint
import telebot
import time

"""
#print(r.content)
files = {'photo':r.content }
data = {'chat_id' : "375937375"}
r= requests.post(urlBot+'sendPhoto', files = {'photo':r.content }, data =  { 'chat_id' : "375937375"})
print(r.json())


,
           {
                "text": "\ud83d\ude18",
                "callback_data": "HELLO222"
              }

url ="https://api.telegram.org/bot546038157:AAHZLzQbE-wNix_UWLTE-6vV_m5YfMB1Vpw/"

json_string =
{
    "chat_id":"375937375",
    "text":"nj asjhd las dkfhjladkfjdkfj sl;df ;sldkf ;sdl klsdlaksdjf sd",
    "reply_markup":{
       "inline_keyboard": [[
           {
                "text": "\u2764\ufe0f",
                "callback_data": "+1"
           }

            ]]
        }
}

