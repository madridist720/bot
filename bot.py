# -*- coding: utf-8 -*-
import config
import telebot
import datetime
import timetable
import timetable1
import db
import mail
from parse import get_top_machts as tm
from telebot import types

import logging

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

mail.get_email()
a="ENF  " + str(config.file) + ' .xlsx' #ENF  1 .xlsx
timetable.start(a)
a="GF  " + str(config.file) + ' .xlsx'
timetable1.start(a)
today = datetime.datetime.now()
bot = telebot.TeleBot(config.token)
if (today.day==1 and today.hour==0):
    config.file=config.file+1
    config.week=config.week+1

user_makeup=telebot.types.ReplyKeyboardMarkup(True,False)
user_makeup.row('расписание')
user_makeup.row('регистрация на подписку')
user_makeup.row('моё расписание на сегодня')
user_makeup.row('отписка')

admin_makeup = telebot.types.ReplyKeyboardMarkup(True, False)
admin_makeup.row('кол-во подписчиков')
admin_makeup.row('exit')
@bot.message_handler(commands=["admin"])
def admin(message):
    if message.chat.id == 120929625:
        message = bot.send_message(message.chat.id, 'ok', reply_markup=admin_makeup)
        a = bot.register_next_step_handler(message, count_users)
    else:
        bot.send_contact(message.chat.id,992901200120,'Maruf')
        bot.send_message(message.chat.id, 'вы не админ', reply_markup=user_makeup)

@bot.message_handler(commands=["send_to_all"])
def admin(message):
    if message.chat.id == 120929625:
        bot.send_message(message.chat.id, "Закончите сообщение фразой /send" )
        bot.register_next_step_handler(message, send_to_all)



def send_to_all(message):
    if '/send' in message.text:
        db.send_to_all(message.text)
        try:
            bot.send_message(message.chat.id, "Отправлено")
        except:
            pass
    else:
        bot.send_message(message.chat.id, "Закончите сообщение фразой /send" )
        send_to_all(message)
def count_users(message):
    a = db.users_count()
    if message.text == 'кол-во подписчиков':
        bot.send_message(message.chat.id, 'кол-во подписчиков = '+str(a), reply_markup=admin_makeup)
        doc = open('user.txt', 'rb')
        bot.send_document(message.chat.id, doc )
        admin(message)
    elif message.text == 'exit':
        handle_start(message)
@bot.message_handler(commands=["topmatch"])
def topmatch(message):
    try:
        text = tm()
    except:
        text = 'Нет топ-матчей'
    bot.send_message(message.chat.id, text,parse_mode="markdown")


@bot.message_handler(commands=["start"])
def handle_start(message):
    user_makeup=telebot.types.ReplyKeyboardMarkup(True,False)
    user_makeup.row('расписание')
    user_makeup.row('регистрация на подписку')
    user_makeup.row('моё расписание на сегодня')
    user_makeup.row('отписка')
    bot.send_message(message.chat.id, 'Добро пожаловать ' + str(message.from_user.first_name),
                     reply_markup=user_makeup)
'''def repeat_all_messages(message): # Название функции не играет никакой роли, в принципе
    bot.send_message(message.chat.id, message.text)'''
# @bot.message_handler(content_types=["voice"])
# def voice(message):
#     import requests
#     import bd
#
#     file_info = bot.get_file(message.voice.file_id)
#     file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(config.token, file_info.file_path)).content
#     myf = open("apple.wav", 'wb')
#     myf.write(file)
#     myf.close()
#     print("Голос")
#     result=bd.start()
#     print("Голос1")
#     print(result)
#     message.text = 'Моё расписание на сегодня'
#     handle_text(message)

# # Обычный режим
# @bot.message_handler(content_types=["text"])
# def any_msg(message):
#     keyboard = types.InlineKeyboardMarkup()
#     callback_button = types.InlineKeyboardButton(text="РЕАЛ МАДРИД", callback_data="REAL")
#     callback_button1 = types.InlineKeyboardButton(text="БАРСЕЛОНА", callback_data="BARSA")
#     keyboard.add(callback_button)
#     keyboard.add(callback_button1)
#     bot.send_message(message.chat.id, "Я – сообщение из обычного режима", reply_markup=keyboard)

# import psycopg2 as p
# con = p.connect(database='dfq6banncblc4l', user='vtudqaibjctcaw', host='ec2-23-23-142-5.compute-1.amazonaws.com', password='d9dcd45b804a1510e232ff7b13f9ff260332692b9328bef3e21b8a752ffb389c')
# cur=con.cursor()
# cur.execute('create table result(barsa integet, real integer)')
# con.commit()

# @bot.callback_query_handler(func=lambda call: True)
# def callback_inline(call):
#     print(call)

#     import psycopg2 as p
#     bot = telebot.TeleBot(config.token)
#     con = p.connect(database='dfq6banncblc4l', user='vtudqaibjctcaw', host='ec2-23-23-142-5.compute-1.amazonaws.com',
#                     password='d9dcd45b804a1510e232ff7b13f9ff260332692b9328bef3e21b8a752ffb389c')
#     cur = con.cursor()
#     # Если сообщение из чата с ботом
#     if call.message:
#         cur.execute("select * from result")
#         m = cur.fetchall()
#         print(m)
#         if call.data == "REAL":
#             text = call.message.text[0:(call.message.text).index('\n')]
#             text = text + call.message.text[(call.message.text).index('\n'):(call.message.text).index('-')+1]+' '+str(m[0][1]+1)+'\n'
#             cur.execute("update result set real=" + str(m[0][1]+1)+ '''
#             where real='''+str(m[0][1]))
#             con.commit()
#             text = text + call.message.text[(call.message.text).rindex('\n')+1:(call.message.text).rindex('-')+1]+' '+str(m[0][0])+'\n'
#             print(text)
#             bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text)

#     # Если сообщение из инлайн-режима
#         elif call.data == "BARSA":
#             text = call.message.text[0:(call.message.text).index('\n')]
#             text = text + call.message.text[
#                           (call.message.text).index('\n'):(call.message.text).index('-') + 1] + ' ' + str(
#                 m[0][1]) + '\n'
#             cur.execute("update result set barsa=" + str(m[0][0] + 1)+ '''
#             where barsa='''+str(m[0][0]))
#             con.commit()
#             text = text + call.message.text[
#                           (call.message.text).rindex('\n') + 1:(call.message.text).rindex('-') + 1] + ' ' + str(
#                 m[0][0]+1) + '\n'
#             print(text)
#             bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=text)


# def parse_message(message):
#     print(message.text)
#     if message.text == 'Нажми меня':
#         bot.send_message(message.chat.id, message.text)

@bot.message_handler(content_types=["text"])
def handle_text(message):
    print(message.text)
    #bot.send_message(message.chat.id, message.text)
    if message.text == 'расписание':
        mail.get_email()
        a = "ENF  " + str(config.file) + ' .xlsx'  # ENF  1 .xlsx
        timetable.start(a)
        a = "GF  " + str(config.file) + ' .xlsx'
        timetable1.start(a)
        a=config.file
        db.new_week()
        print(a)
        if config.file!= a :
            print("да")
            a = "ENF  " + str(config.file) + ' .xlsx'
            timetable.start(a)
            a = "GF  " + str(config.file) + ' .xlsx'
            timetable1.start(a)
        db.new_week()
        print(config.file)
        keyboard=types.ReplyKeyboardMarkup()
        keyboard.add('ЕНФ')
        keyboard.add('ГФ')
        message1=bot.send_message(message.chat.id,'выберите факультет',reply_markup=keyboard)
        bot.register_next_step_handler(message1, fuc)
        #rasp_type(message)
    elif message.text =='вначало':
        handle_start(message)
        #bot.send_message(message.chat.id, "Подписка разрабатывается")
    elif message.text=="регистрация на подписку":
        regist(message)
    elif message.text =='отписка':
        a = db.delete_me(message.chat.id)
        bot.send_message(message.chat.id, a, parse_mode="markdown",reply_markup=user_makeup )
    elif message.text=='моё расписание на сегодня':
        mail.get_email()
        a = "ENF  " + str(config.file) + ' .xlsx'  # ENF  1 .xlsx
        timetable.start(a)
        a = "GF  " + str(config.file) + ' .xlsx'
        timetable1.start(a)
        res=db.search_my(message)
        if res!=[]:
            my_time(message, res)
        else:
            bot.send_message(message.chat.id, "Вы не подписаны на расписание 😣 \nнажмите на кнопку  \n'регистрация на подписку'")
            handle_start(message);
    else:
        bot.send_message(message.chat.id,"НЕПРАВИЛЬНАЯ КОМАНДА ")
        handle_start(message);
def my_time(message, res):
    print(res)
    pr= res[0][1]
    kr=res[0][2]
    print(pr)
    print(kr)  
    a=config.file
    b=config.week
    db.new_week()
        
    if config.file!= a :
        print("да")
        a = "ENF  " + str(config.file) + ' .xlsx'
        timetable.start(a)
        a = "GF  " + str(config.file) + ' .xlsx'
        timetable1.start(a)
    db.new_week()
    today = datetime.datetime.now()
    sl="Ваше расписание на сегодня :\n"
    print(today.time().hour, today.time().minute)
    dn = datetime.date.today().isoweekday()
    if (today.time().hour>=13 ):
        dn=dn+1
        if dn>7:
            dn=1
            a = "ENF  " + str(int(config.file)+1) + ' .xlsx'
            timetable.start(a)
            a = "GF  " + str(int(config.file)+1) + ' .xlsx'
            timetable1.start(a)
        sl="Сегодня больше пар нет😉\n💼Ваше расписание на завтра🎓:\n"
    if pr in ("МО", "ГМУ"):
        z=timetable1.get_day(pr,kr, dn)
    elif pr == "Лингв":
        z=timetable1.get_day('ЛИНГВ',kr,dn)
    else:
        if pr=='ПМИ':
            z = timetable.get_day("ПМИИ",kr,dn)
        elif pr=='Геология':

            z = timetable.get_day("ГЕОЛ",kr,dn)
            print(z)
        elif pr=='Химия':
            z = timetable.get_day("ХИМФ",kr, dn)
        
    bot.send_message(message.chat.id, sl+z,parse_mode="markdown",reply_markup=user_makeup)


def regist(message):
    keyboard1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    today = datetime.date.today().isoweekday()
    keyboard1.add("МО", "ГМУ","Лингв")
    keyboard1.add("ПМИ","Геология", "Химия")
    message1 = bot.send_message(message.chat.id, 'выберите направление', reply_markup=keyboard1)
    bot.register_next_step_handler(message, regist1)
def regist1(message):
    config.pod_pr=message.text
    pr=message.text
    if pr in ("МО", "ГМУ","Лингв","ПМИ","Геология", "Химия"):
        keyboard2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard2.add("1-ый курс", '2-ой курс')
        keyboard2.add('3-ий курс', '4-ый курс')
        bot.send_message(message.chat.id, 'выберите курс', reply_markup=keyboard2)
        bot.register_next_step_handler(message,start)
    elif pr=="Реклама":
        start(message)
def start(message):
    pr=config.pod_pr
    kr=message.text
    if pr in ("МО", "ГМУ", "Лингв","ПМИ","Геология", "Химия"):
        z=db.start(message,pr,kr[0])
        bot.send_message(message.chat.id,z)
        handle_start(message)
    elif pr=="Реклама":
        z=db.start(message, pr, 0)
        bot.send_message(message.chat.id, z)
        handle_start(message)
def fuc(message):
    if message.text=='ЕНФ':
        rasp_type(message)
    elif message.text=='ГФ':
        rasp_type1(message)
def rasp_type1(message):
    from telebot import types
    keyboard1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    today = datetime.datetime.now()
    keyboard1.add("Расписание на сегодня")
    keyboard1.add("Расписание на оставшиеся дни")
    if (today.isoweekday() == 7) or (today.isoweekday() == 6 and today.hour >= 13):
        keyboard1.add("Расписание на след неделю")
    keyboard1.add("Назад")

    message1 = bot.send_message(message.chat.id, 'выберите тип расписания', reply_markup=keyboard1)
    bot.register_next_step_handler(message1, start_m1)
def start_m1(message):
    if message.text in ("Расписание на сегодня","Расписание на оставшиеся дни","Расписание на след неделю"):
        config.rasp_type=message.text
        keyboard1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        today = datetime.date.today().isoweekday()
        keyboard1.add("МО","ГМУ")
        keyboard1.add("Лингвистика")
        keyboard1.add("Назад")
        message1 = bot.send_message(message.chat.id, 'выберите направление', reply_markup=keyboard1)
        bot.register_next_step_handler(message1, start_nap1)
    elif message.text=="Назад":
        fuc(message)

    else:
        bot.send_message(message.chat.id, "выбран неправельный тип расписания")
        rasp_type1(message)
def start_nap1(message1):
    from telebot import types
    user_makeup = telebot.types.ReplyKeyboardRemove()
    pr = (message1.text)
    if pr in ("МО", "ГМУ", "Лингвистика", 'Реклама'):
        config.pr = pr
        keyboard2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard2.add("1-ый курс", '2-ой курс')
        keyboard2.add('3-ий курс', '4-ый курс')
        keyboard2.add("Назад")
        if pr =='Реклама':
            if (config.rasp_type == 'Расписание на сегодня'):
                 start_kur1(message1)
                 return 0
            elif (config.rasp_type == "Расписание на оставшиеся дни"):
                pasp_ned1(message1)
                return 0
            elif (config.rasp_type == "Расписание на след неделю"):
                a = config.file
                # print(z)
                config.file = a

                past_nex_ned1(message1)
                return 0
        bot.send_message(message1.chat.id, 'Теперь выбери курс', reply_markup=keyboard2)
        if (config.rasp_type == 'Расписание на сегодня'):
            bot.register_next_step_handler(message1, start_kur1)
        elif (config.rasp_type == "Расписание на оставшиеся дни"):
            bot.register_next_step_handler(message1, pasp_ned1)
        elif (config.rasp_type == "Расписание на след неделю"):
            a = config.file
            # print(z)
            config.file = a

            bot.register_next_step_handler(message1, past_nex_ned1)


    elif pr == "Назад":
        rasp_type1(message1)

    else:
        bot.send_message(message1.chat.id, 'ошибка выберите направление')
        bot.register_next_step_handler(message1, start_nap1)
def start_kur1(message1):
    pr = config.pr
    f = open('text.txt', 'r')
    a = f.read()
    f.close()
    # print(a)
    global user_makeup
    a = a.split()
    if str(message1.chat.id) not in a:
        f = open('text.txt', 'a')
        f.write(
            str(message1.chat.id) + ' ' + str(message1.from_user.first_name) + ' ' + str(message1.from_user.last_name))
    f.close()
    print(message1.chat.id)
    from telebot import types
    #user_makeup = telebot.types.ReplyKeyboardRemove()
    kr = message1.text
    # print(kr)
    if pr =="Реклама":
        dn = datetime.date.today().isoweekday()
        bot.send_message(message1.chat.id, 'загрузка с файла...')
        z = timetable1.get_day("РЕКС",0, dn)
        bot.send_message(message1.chat.id, z, reply_markup=user_makeup, parse_mode='markdown')

        return 0
    if kr[0] in ("1", "2", "3", "4") :
        dn = datetime.date.today().isoweekday()
        bot.send_message(message1.chat.id, 'загрузка с файла...')
        # rasp.start()
        if pr == 'МО':
            z = timetable1.get_day("МО", int(kr[0]), dn)
        elif pr == 'ГМУ':

            z = timetable1.get_day("ГМУ", int(kr[0]), dn)
        elif pr =="Лингвистика":
            z=timetable1.get_day("ЛИНГВ",int(kr[0]), dn)
        try:
            bot.send_message(message1.chat.id, z, reply_markup=user_makeup, parse_mode='markdown')
        # bot.send_message(message1.chat.id, '*продолжим?*', parse_mode='markdown')
        except:
            bot.send_message(message1.chat.id, z, reply_markup=user_makeup)
        # handle_start(message1)
        #bot.send_message(message1.chat.id, "для продолжения нажмите на /start")

    elif kr == "Назад":
        start_nap1(message1)
    else:
        bot.send_message(message1.chat.id, 'ошибка выберите курс')
        bot.register_next_step_handler(message1, start_kur1)
def pasp_ned1(message1):
    pr = config.pr
    from telebot import types
    #user_makeup = telebot.types.ReplyKeyboardRemove()
    kr = message1.text
    print(kr)
    z = ''
    dn = datetime.date.today().isoweekday()
    if kr[0] in ("1", "2", "3", "4"):
        bot.send_message(message1.chat.id, 'загрузка расписания...')
        # rasp.start()
        if pr == 'МО':
            z = timetable1.get_last_day("МО", int(kr[0]), dn)
        elif pr == 'ГМУ':

            z = timetable1.get_last_day("ГМУ", int(kr[0]), dn)
            print(z)
        elif pr == 'Лингвистика':
            z = timetable1.get_last_day("ЛИНГВ", int(kr[0]), dn)


        bot.send_message(message1.chat.id, z, parse_mode='markdown', reply_markup=user_makeup)
        # bot.send_message(message1.chat.id, '*продолжим?*', parse_mode='markdown')
        # rasp_t=config.rasp_type

        # bot.send_message(message1.chat.id, z, parse_mode='markdown')
        # handle_start(message1)
        #bot.send_message(message1.chat.id, "для продолжения нажмите на  /start")
    elif pr == "Реклама":
        z = timetable1.get_last_day("РЕКС", 0, dn)
        bot.send_message(message1.chat.id, z, parse_mode='markdown', reply_markup=user_makeup)
        # bot.send_message(message1.chat.id, '*продолжим?*', parse_mode='markdown')
        # rasp_t=config.rasp_type

        # bot.send_message(message1.chat.id, z, parse_mode='markdown')
        # handle_start(message1)
        #bot.send_message(message1.chat.id, "для продолжения нажмите на  /start")
    elif kr == "Назад":
        start_nap1(message1)
    else:
        bot.send_message(message1.chat.id, 'ошибка выберите курс')
        bot.register_next_step_handler(message1, start_kur1)
def past_nex_ned1(message1):
    pr = config.pr
    from telebot import types
    #user_makeup = telebot.types.ReplyKeyboardRemove()
    kr = message1.text
    print(kr)
    z = ''
    bot.send_message(message1.chat.id, '*Расписание загружается, подождите...*', parse_mode='markdown')
    a = "GF  " + str(int(config.file)+1) + ' .xlsx'
    timetable1.start(a)


    dn = datetime.date.today().isoweekday()
    if kr[0] in ("1", "2", "3", "4"):
        bot.send_message(message1.chat.id, 'загрузка расписания...')
        # rasp.start()
        if pr == 'МО':
            z = timetable1.get_week("МО", int(kr[0]))
        elif pr == 'ГМУ':

            z = timetable1.get_week("ГМУ", int(kr[0]))
            print(z)
        elif pr == 'Лингвистика':
            z = timetable1.get_week("ЛИНГВ", int(kr[0]))

        bot.send_message(message1.chat.id, z, parse_mode='markdown', reply_markup=user_makeup)
        # bot.send_message(message1.chat.id, '*продолжим?*', parse_mode='markdown')
        # rasp_t=config.rasp_type

        # bot.send_message(message1.chat.id, z, parse_mode='markdown')
        # handle_start(message1)
        #bot.send_message(message1.chat.id, "для продолжения нажмите на  /start")
        a = "GF  " + str(config.file) + ' .xlsx'
        timetable1.start(a)
    elif pr == "Реклама":
        z = timetable1.get_week("РЕКС", 0)
        bot.send_message(message1.chat.id, z, parse_mode='markdown', reply_markup=user_makeup)
        # bot.send_message(message1.chat.id, '*продолжим?*', parse_mode='markdown')
        # rasp_t=config.rasp_type

        # bot.send_message(message1.chat.id, z, parse_mode='markdown')
        # handle_start(message1)
        #bot.send_message(message1.chat.id, "для продолжения нажмите на  /start")
    elif kr == "Назад":
        start_nap1(message1)
    else:
        bot.send_message(message1.chat.id, 'ошибка выберите курс')
        bot.register_next_step_handler(message1, start_kur1)
def rasp_type(message):
    from telebot import types
    keyboard1=types.ReplyKeyboardMarkup(resize_keyboard=True)
    today=datetime.datetime.now()
    keyboard1.add("Расписание на сегодня")
    keyboard1.add("Расписание на оставшиеся дни")
    if(today.isoweekday()==7) or (today.isoweekday()==6 and today.hour>=13):
        keyboard1.add("Расписание на след неделю")
    keyboard1.add("Назад")

    message1=bot.send_message(message.chat.id, 'выберите тип расписания', reply_markup=keyboard1)
    bot.register_next_step_handler(message1,start_m)
def start_m(message):
    if message.text in ("Расписание на сегодня","Расписание на оставшиеся дни","Расписание на след неделю"):
        config.rasp_type=message.text
        keyboard1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        today = datetime.date.today().isoweekday()
        keyboard1.add("ПМИ","Геология")
        keyboard1.add("Химия")
        keyboard1.add("Назад")
        message1 = bot.send_message(message.chat.id, 'выберите направление', reply_markup=keyboard1)
        bot.register_next_step_handler(message1, start_nap)
    elif message.text=="Назад":
        handle_start(message)

    else:
        bot.send_message(message.chat.id, "выбран неправельный тип расписания")
        rasp_type(message)
def start_nap(message1):
    #print(message1.text)
    from telebot import types
    user_makeup = telebot.types.ReplyKeyboardRemove()
    pr=(message1.text)
    if pr in ("ПМИ", "Геология","Химия"):
        config.pr=pr
        keyboard2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard2.add("1-ый курс",'2-ой курс')
        keyboard2.add('3-ий курс','4-ый курс')
        keyboard2.add("Назад")
        bot.send_message(message1.chat.id, 'Теперь выбери курс', reply_markup=keyboard2)

        if (config.rasp_type == 'Расписание на сегодня'):
            bot.register_next_step_handler(message1, start_kur)
        elif (config.rasp_type=="Расписание на оставшиеся дни"):
            bot.register_next_step_handler(message1,pasp_ned)
        elif (config.rasp_type=="Расписание на след неделю"):
                a=config.file
                #print(z)
                config.file=a

                bot.register_next_step_handler(message1,past_nex_ned)
    elif pr=="Назад":
       rasp_type(message1)

    else:
        bot.send_message(message1.chat.id, 'ошибка выберите направление')
        bot.register_next_step_handler(message1,start_nap)



    #bot.send_message(message1.chat.id,'',reply_markup=user_makeup)
def start_kur(message1):
    pr=config.pr

    print(message1.chat.id)
    from telebot import types
    #user_makeup = telebot.types.ReplyKeyboardRemove()
    kr=message1.text
    #print(kr)
    if kr[0] in ("1","2","3","4"):
        dn = datetime.date.today().isoweekday()
        bot.send_message(message1.chat.id, 'загрузка с файла...')
        #rasp.start()
        if pr=='ПМИ':
            z = timetable.get_day("ПМИИ",int(kr[0]),dn)
        elif pr=='Геология':

            z = timetable.get_day("ГЕОЛ",int(kr[0]),dn)
            print(z)
        elif pr=='Химия':
            z = timetable.get_day("ХИМФ",int(kr[0]), dn)
        try:
            bot.send_message(message1.chat.id, z, reply_markup=user_makeup, parse_mode='markdown')
        #bot.send_message(message1.chat.id, '*продолжим?*', parse_mode='markdown')
        except:
            bot.send_message(message1.chat.id, z, reply_markup=user_makeup)
        #handle_start(message1)
        #bot.send_message(message1.chat.id, "для продолжения нажмите на /start")
    elif kr=="Назад":
        start_nap(message1)
    else:
        bot.send_message(message1.chat.id, 'ошибка выберите курс')
        bot.register_next_step_handler(message1, start_kur)

def pasp_ned(message1):
    pr = config.pr
    from telebot import types
    #user_makeup = telebot.types.ReplyKeyboardRemove()
    kr = message1.text
    print(kr)
    z=''
    dn = datetime.date.today().isoweekday()
    if kr[0] in ("1", "2", "3", "4"):
        bot.send_message(message1.chat.id, 'загрузка расписания...')
        #rasp.start()
        print(pr)
        if pr == 'ПМИ':
            z = timetable.get_last_day("ПМИИ", int(kr[0]),dn)
            print('sended')
        elif pr == 'Геология':
            z = timetable.get_last_day("ГЕОЛ", int(kr[0]),dn)
        elif  pr == 'Химия':
            z = timetable.get_last_day("ХИМФ", int(kr[0]),dn)

        bot.send_message(message1.chat.id, z, parse_mode='markdown', reply_markup=user_makeup)
        #bot.send_message(message1.chat.id, '*продолжим?*', parse_mode='markdown')
        #rasp_t=config.rasp_type

        #bot.send_message(message1.chat.id, z, parse_mode='markdown')
        #handle_start(message1)
        #bot.send_message(message1.chat.id, "для продолжения нажмите на  /start")
    elif kr=="Назад":
        start_nap(message1)
    else:
        bot.send_message(message1.chat.id, 'ошибка выберите курс')
        bot.register_next_step_handler(message1, start_kur)
def past_nex_ned(message1):
    pr = config.pr
    from telebot import types
    #user_makeup = telebot.types.ReplyKeyboardRemove()
    kr = message1.text
    #print(kr)
    z = ''
    dn = datetime.date.today().isoweekday()
    if kr[0] in ("1", "2", "3", "4"):
        bot.send_message(message1.chat.id, '*Расписание загружается, подождите...*', parse_mode='markdown')

        a = "ENF  " + str(int(config.file)+1) + ' .xlsx'
        timetable.start(a)


        if pr == 'ПМИ':
            z = z + timetable.get_week("ПМИИ", int(kr[0]))
        elif pr == 'Геология':
            z = z + timetable.get_week("ГЕОЛ", int(kr[0]))
        elif pr == 'Химия':
            z = z+timetable.get_week("ХИМФ", int(kr[0]))
        #bot.send_message(message1.chat.id, z, parse_mode='markdown', reply_markup=user_makeup)
        #z.replace('*','')
        #rasp_t = config.rasp_type

        bot.send_message(message1.chat.id, z, parse_mode='markdown',reply_markup=user_makeup)

        a = "ENF  " + str(config.file) + ' .xlsx'
        timetable.start(a)
        #handle_start(message1)
        #bot.send_message(message1.chat.id, "для продолжения нажмите на  /start")
    elif kr=="Назад":
        start_nap(message1)
    else:
        bot.send_message(message1.chat.id, 'ошибка выберите курс')
        bot.register_next_step_handler(message1, start_kur)

def while_main():
    bot.polling()
    
if __name__ == '__main__':
    try:
        bot.polling()
    except:
        while_main()

