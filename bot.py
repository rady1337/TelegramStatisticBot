# -*- coding: utf-8 -*-


import telebot
from telebot import types
import src.config
from src.parser import parse
from src.sqlite_manger import SQLManage


TOKEN = src.config.BOT_TOKEN
ADMIN_ID = src.config.ADMIN_ID
ADMIN_INPUT = 0


bot = telebot.TeleBot(TOKEN)
db = SQLManage('src/db.db')


# def



@bot.message_handler(commands=['start', 'help', 'back', 'назад'])
def bot_start(message):
    global ADMIN_ID
    global ADMIN_INPUT
    ADMIN_INPUT = 0
    start_key = types.ReplyKeyboardMarkup()
    start_key.add('📈 Статистика о Сайте', '📒 О Боте')
    if str(message.chat.id) == str(ADMIN_ID):
        start_key.row('🔑 Админ Панель')
    bot.send_message(
        message.chat.id, '😉Привет!😉\n📊Я Бот, который умеет собирать информацию и статистику о сайтах!📊\n\n\n👑Создатель: @iamscriptkiddie 👑', reply_markup=start_key)
    if not(db.user_exists(int(message.chat.id))):
        db.add_user(int(message.chat.id))


@bot.message_handler(content_types=['text'])
def bot_main(message):
    global ADMIN_INPUT
    global ADMIN_ID
    if db.check_status(int(message.chat.id)) == [('True',)]:
        info = parse(message.text)
        if info == 'Wrong Host!':
            bot.send_message(message.chat.id,
                             '🆘Ошибка!\n🆘Неверный Адресс!')
        else:
            countries = ''
            for country in info[2]:
                countries += country + '\n'
            sites = ''
            for site in info[3]:
                sites += site + '\n'
            ip_history = ''
            for ip in info[4]:
                ip_history += ip + '\n'
            info_text = f"💻Веб-Сайт: {message.text}\n\n📈Просмотры:\n🕐День: {info[0][0]}\n🕦Неделя: {info[0][1]}\n🕙Месяц: {info[0][2]}\n\n📈Посетители:\n🕐День: {info[1][0]}\n🕦Неделя: {info[1][1]}\n🕙Месяц: {info[1][2]}\n\n🏴Страны:\n{countries}\n🖥Похожие Сайты:\n{sites}\n📊История IP:\n{ip_history}"
            bot.send_message(message.chat.id, info_text)
        db.status_off(int(message.chat.id))
    else:
        if message.text == '🔑 Админ Панель' and str(message.chat.id) == str(ADMIN_ID):
            admin_key = types.ReplyKeyboardMarkup()
            admin_key.add('Рассылка по всем пользователям',
                          'Кол-во пользователей бота')
            admin_key.add('ID всех пользователей')
            admin_key.row('/назад')
            bot.send_message(message.chat.id, 'Добро пожаловать в Админ Панель!',
                             reply_markup=admin_key)
        elif ADMIN_INPUT == 1 and str(message.chat.id) == str(ADMIN_ID):
            if message.text.strip() == 'ВЫХОД':
                ADMIN_INPUT = 0
            else:
                admin_text = message.text
                users_id = db.get_all_id()
                for idd in users_id:
                    idd = str(idd)
                    idd = idd[1:]
                    idd = idd[:-2]
                    idd = idd.strip()
                    bot.send_message(int(idd), admin_text)
                ADMIN_INPUT = 0
    
    
        
        elif message.text == 'Кол-во пользователей бота' and str(message.chat.id) == str(ADMIN_ID):
            user_count = db.get_all_id()
            bot.send_message(message.chat.id, f'Кол-во пользователей бота: {len(user_count)}')
    
        elif message.text == 'ID всех пользователей' and str(message.chat.id) == str(ADMIN_ID):
            users_id = db.get_all_id()
            users_id_str = ''
            for idd in users_id:
                idd = str(idd)
                idd = idd[1:]
                idd = idd[:-2]
                users_id_str += str(idd) + '\n'
            bot.send_message(message.chat.id, users_id_str)
    
        elif message.text == 'Рассылка по всем пользователям' and str(message.chat.id) == str(ADMIN_ID):
            ready_key = types.ReplyKeyboardMarkup()
            ready_key.add('Да, я готов отправить рассылку', '/назад')
            bot.send_message(
                message.chat.id, 'Внимание! Вы будете должны подтвердить своё дейтсвие!', reply_markup=ready_key)
    
        elif message.text == 'Да, я готов отправить рассылку' and str(message.chat.id) == str(ADMIN_ID):
            bot.send_message(
                message.chat.id, 'Пишитие текст для рассылки(для выхода напишите /назад)')
            ADMIN_INPUT = 1
            
    
        elif message.text == '📒 О Боте':
            about = '😉Привет! Я Бот-Парсер 😉\n\n📊Я могу выдавать статистику о сайте, который ты мне отправишь📊\n\n❗P.S. Не все сайты могут работать❗️\n\n\n\n👑Создатель: @iamscriptkiddie 👑\n\n(Бот для Портфолио)'
            bot.send_message(message.chat.id, about)
    
        elif message.text == '📈 Статистика о Сайте':
            db.status_on(int(message.chat.id))
            bot.send_message(message.chat.id, '🖥 Введите адресс сайта: ')

        else:
            help_key = types.ReplyKeyboardMarkup()
            help_key.row('/help')
            bot.send_message(
                message.chat.id, 'Я тебя не понимаю😦...\nНапиши /help', reply_markup=help_key)


bot.polling(none_stop=True, interval=0)
