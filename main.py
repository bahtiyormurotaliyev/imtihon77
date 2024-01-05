import telebot
import wikipedia

bot = telebot.TeleBot("6840330612:AAEIsKG2RbvRWPdhbQ0W1fABPRmZeOvePrI")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom🙂:Men sizga Wikipedia orqali ma'lumot beraman")

@bot.message_handler(func=lambda message: True)
def search(message):
    wikipedia.set_lang('uz') 
    query = message.text
    results = wikipedia.search(query)
    if not results:
        bot.send_message(message.chat.id, 'Afsus!😔 Topilmadi.')
        return
    page = wikipedia.page(results[0])
    bot.send_message(message.chat.id, page.url)

bot.polling()