import os

from flask import Flask, request
from telebot import types
import time
import qrcode
import telebot

TOKEN = '5286040884:AAGJ5Qx-2uc4tu0mCJ9ewN4cWdRoWQptbTg'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

@bot.message_handler(content_types = ["text"])
def start_message(message):
  keyboard = types.ReplyKeyboardMarkup()
  keyboard.add("картинка")
  keyboard.add("текст")
  keyboard.add("сылку")
  bot.send_message(message.chat.id,"привет я могу перевести в qr код : картинки, тект и сылки")
  time.sleep(1)
  bot.send_message(message.chat.id,"что хочешь перевести в qr код?",reply_markup=keyboard)
  bot.register_next_step_handler(message,choose)

def choose (message):
  if message.text == "картинка" :
    bot.send_message(message.chat.id,"тогда присылай её")
    bot.register_next_step_handler(message,image)
  elif message.text == "текст" :
    bot.send_message(message.chat.id,"тогда присылай его")
    bot.register_next_step_handler(message,test)
  elif message.text == "сылка" :
    bot.send_message(message.chat.id,"тогда присылай её")
    bot.register_next_step_handler(message,test)


def test(message):
  qr = qrcode.make(message.text)
  qr.save('qr.png')
  qrImage = open("qr.png", "rb")
  bot.send_message(message.chat.id,"вот твой qr код")
  bot.send_photo(message.chat.id, qrImage)
  review(message)


def image(message):
  qr = qrcode.make(message.text)
  bot.send_message(message.chat.id,"вот твой qr код")
  bot.send_photo(message.chat.id, qr)
  review(message)

def review(message):
  review_keyboard = types.ReplyKeyboardMarkup()
  review_keyboard.add("да")
  review_keyboard.add("нет")
  bot.send_message(message.chat.id,"ты доволен роботой бота?",reply_markup=review_keyboard)
  bot.register_next_step_handler(message,review_answer)

def review_answer(message):
  if message == "да" :
    bot.send_message(message.chat.id,"я рад что ты доволен роботой бота!")
  if message == "нет" :
    bot.send_message(message.chat.id,"мне очень важен твой отзыв,пожалуйста напиши поподробние что не так на почту yankingeorge2@gmail.com")

bot.polling(none_stop = True)

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200
    
@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://bazzzz.herokuapp.com/' + TOKEN)
    return "!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
