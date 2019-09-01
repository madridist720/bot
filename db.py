import psycopg2 as p
import config
import telebot
import datetime
import timetable
import timetable1
bot = telebot.TeleBot(config.token)
con = p.connect(database='dfq6banncblc4l', user='vtudqaibjctcaw', host='ec2-23-23-142-5.compute-1.amazonaws.com', password='d9dcd45b804a1510e232ff7b13f9ff260332692b9328bef3e21b8a752ffb389c')
cur=con.cursor()
a=[]


def start(message,fuc,kurs):
    #cur.execute('ALTER TABLE users MODIFY (fuc varchar(20));')
    con.commit()
    cur.execute('select * from users')
    con.commit()
    a.clear()
    for row in cur:
        a.append(row[0])
    print(a)
    if message.from_user.id in a:
        cur.execute('update  users set name = ' + str(message.from_user.id) + ', fuck = ' + "'" + fuc + "'" + ', kurs = ' + str(kurs) + ', username = ' + "'" + str(message.from_user.username) + "'" + ' where name = ' + str(message.from_user.id)+';')
        con.commit()
        return "Подписка обновлена"
        a.clear()
    else:
        try:
            cur.execute('INSERT INTO users VALUES ('+str(message.from_user.id)+','+"'"+fuc+"'"+','+str(kurs)+','+ "'" + str(message.from_user.username) + "'"+');')
            con.commit()
            return "Успешно добавлена"
        except:

            a.clear()
            return "Произошла ошибка при регистрации. Обратитесь к @madridist20"

def rassilka():
    cur.execute("select * from users")
    dn = datetime.date.today().isoweekday()
    for row in cur:
        print(row[1])
        print(row[2])
        if row[1] in ("МО", "ГМУ","Лингв", "Реклама"):
            if row[1] == 'МО':
                z = timetable1.get_day("МО", int(row[2]), dn)
            elif row[1] == 'ГМУ':

                z = timetable1.get_day("ГМУ", row[2], dn)
            elif row[1] == "Лингв":
                z = timetable1.get_day("ЛИНГВ", row[2], dn)
            bot.send_message(row[0], z,  parse_mode='markdown')
        elif row[1] in ("ПМИ", "Геология","Химия"):
            if row[1] == 'ПМИ':
                z = timetable.get_day("ПМИИ",int(row[2]), dn)
            elif row[1] == 'Геология':

                z = timetable.get_day("ГЕОЛ", row[2], dn)
                print(z)
            elif row[1] == 'Химия':
                z = timetable.get_day("ХФММ", row[2], dn)
            bot.send_message(row[0], z, parse_mode='markdown')
def new_week():
    cur.execute("select * from config")
    m = cur.fetchall()

    print(m)
    config.file=m[0][0]
def search_my(message):
    cur.execute('select * from users where name='+str(message.from_user.id))
    m=cur.fetchall()
    return m
          
def delete_me(user_id):
    try:
        cur.execute('select * from users')
        mylist=[]
        mylist.clear()
        for row in cur:
            mylist.append(row[0])
        print(mylist)
        if user_id in mylist:
            cur.execute("delete from users where name = " + str(user_id))
            a = 'Вы успешно отписались'
        else:
            a = 'Извините, вы не подписаны'
    except:
        a = 'Извините произошла ошибка, либо вы не подписаны на рассылку'
    con.commit()
    return a
def users_count():
    cur.execute('select * from users')
    a = cur.fetchall()
    new = open('user.txt', 'w')
    new.write('')
    new.close()
    new = open('user.txt', 'wb')
    m = ''
    for i in a:
        b = bot.get_chat(i[0])
        # print(str(a.id) +' '+str(a.username) +  ' '+str(a.first_name)  +' '+ str(a.last_name))
        m = m + str(b.id) + ' ' + str(b.username) + ' ' + str(b.first_name) + ' ' + str(b.last_name) + '\n'
    new.write(m.encode("utf-8"))
    new.close()
    print('end')
    return len(a)

def send_to_all(text):
    cur.execute('select * from users')
    for row in cur:
        bot.send_message(row[0], text, parse_mode='markdown')