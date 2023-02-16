import telebot
import requests
from bs4 import BeautifulSoup
from decouple import config


TOKEN = config('TOKEN')
STACKOVERFLOW = 'https://stackoverflow.com'
SEARCH_URL = 'https://stackoverflow.com/search?q='
TAGGED_URL = 'https://stackoverflow.com/questions/tagged/'
bot = telebot.TeleBot(TOKEN)

keyboard = telebot.types.ReplyKeyboardMarkup()
python = telebot.types.KeyboardButton('python')
django = telebot.types.KeyboardButton('django')
drf = telebot.types.KeyboardButton('rest framework')
js = telebot.types.KeyboardButton('java script')
html = telebot.types.KeyboardButton('html')
css = telebot.types.KeyboardButton('css')
keyboard.add(
    python, django, drf,
    js, html, css
)

@bot.message_handler(commands=['start', 'ask'])
def start(message):
    bot.send_message(message.chat.id, 'hey', reply_markup=keyboard)
    bot.register_next_step_handler(message, check)

def check(message):
    if message.text.lower() in ['quit', 'exit', 'q']:
        bot.send_message(message.chat.id, 'Goodbye!')
    elif message.text.lower() in [
        'python', 'django', 'rest framework',
        'java script', 'html', 'css'
    ]:
        html = requests.get(TAGGED_URL+''.join(message.text.split())).text
        soup = BeautifulSoup(html, 'lxml')
        answers = soup.find_all('h3', class_='s-post-summary--content-title')[:3]
        for elem in answers:
            link = STACKOVERFLOW + elem.find("a", class_="s-link").get("href")
            title = elem.text
            bot.send_message(message.chat.id, f'{link}\n\n{title}')
    # TODO: finish else block
    # else:
    #     html = requests.get(SEARCH_URL+'+'.join(message.text.split())).text
    #     soup = BeautifulSoup(html, 'lxml')
    #     answers = soup.find_all('h3', class_='s-post-summary--content-title')[:3]
    #     for elem in answers:
    #         link = STACKOVERFLOW + elem.find("a", class_="s-link").get("href")
    #         title = elem.text
    #         bot.send_message(message.chat.id, f'{link}\n\n{title}')

bot.polling()
