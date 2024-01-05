from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, Filters
import requests
import json
import smtplib
from email.mime.text import MIMEText
from weather.models import WeatherData

TOKEN = '6950557210:AAGbHdoYK_n09LEdp1Ajk2Hz7s__3RgdMec' 
bot = Bot(token=TOKEN)
app = Flask(__name__)


OPENWEATHER_API_KEY = '54cfce9e11d0eaad583727ade774a135'  
OPENWEATHER_API_URL = 'http://api.openweathermap.org/data/2.5/weather'


DATABASE_URL = 'sqlite:///weather_data.db' 



# import os
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")
# import django
# django.setup()

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Assalomu alaykum! Bot ishga tushdi.")

def get_weather(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    user_email = update.message.from_user.email
    location = context.args[0] if context.args else "Toshkent"  

    params = {
        'q': location,
        'appid': OPENWEATHER_API_KEY,
        'units': 'metric'  
    }

    response = requests.get(OPENWEATHER_API_URL, params=params)
    weather_data = response.json()

    temperature = weather_data['main']['temp']
    weather_description = weather_data['weather'][0]['description']


    send_email(user_email, location, temperature)

    update.message.reply_text(f"Havo haqida ma'lumot: {temperature}°C, {weather_description}")

def send_email(email, location, temperature):
    WeatherData.objects.create(email=email, location=location, temperature=temperature)


import smtplib
from email.mime.text import MIMEText

def send_email(sender_email, recipient_email, subject, message):
    smtp_server = 'bahtiyormurotaliyev552@gmail.com'
    smtp_port = 587
    smtp_username = 'bahtiyor'
    smtp_password = 'Tashkent_123'

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        print('Email sent successfully.')
    except Exception as e:
        print(f'Failed to send email. Error: {str(e)}')


sender_email = input('Enter your sender email: 9')
recipient_email = input('Enter recipients address:today ')
subject = input('Enter the subject of the message: ')
message = input('Enter message text:Toshkent ')

send_email(sender_email, recipient_email, subject, message)


def echo(update: Update, context: CallbackContext):
    update.message.reply_text("Noma'lum buyruq, iltimos!")

@app.route('/webhook', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dp.process_update(update)
    return "ok"


if __name__ == '__main__':
    from telegram.ext import Dispatcher

    dp = Dispatcher(bot, None)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("weather", get_weather, pass_args=True))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))


    WEBHOOK_URL = 'https://webhook.site/8edb483a-9380-42e8-9fe2-7e8d3a16a741'  
    CERT_PATH = 'path/to/certificate.pem'  

    bot.delete_webhook()
    bot.set_webhook(WEBHOOK_URL, certificate=open(CERT_PATH, 'rb'))

    app.run(port=8443)
