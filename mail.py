import imaplib
import email
import datetime
today = datetime.datetime.now()
username = 'afellay_maruf@mail.ru'
password = 'afellay20sb'

gmail = imaplib.IMAP4_SSL('imap.mail.ru', '993')
gmail.login(username, password)

def get_email():
    today = datetime.datetime.now()
    dn = datetime.date.today().isoweekday()
    if dn > 5 and check_count() > 1:
        try:
            get_email1(1)
            get_email1(0)
        except:
            pass
    else:
        try:
            get_email1(0)
        except:
            pass
def check_count():


    stat, cnt = gmail.select('timetable')

    stat, dta = gmail.uid('search', None, 'ALL')
    #    (cnt[0]),\
    #        ('UID BODY[TEXT])')
    # print(dta[0])
    inbox_list = dta[0].split()
    return len(inbox_list)
def get_email1(k):
    stat, cnt = gmail.select('timetable')

    stat, dta = gmail.uid('search', None, 'ALL')
    #    (cnt[0]),\
    #        ('UID BODY[TEXT])')
    # print(dta[0])
    inbox_list = dta[0].split()
    oldest = inbox_list[-1-k]
    print(oldest)
    res, data = gmail.uid('fetch', oldest, '(RFC822)')

    raw_m = data[0][1].decode("utf-8")
    email_mes = email.message_from_string(raw_m)
    a = email_mes
    # print(a)
    # b = get_first_text_block(email_mes)
    # print(b)
    mail = email.message_from_bytes(data[0][1])

    if mail.is_multipart():
        for part in mail.walk():
            content_type = part.get_content_type()
            filename = part.get_filename()
            if filename:
                # Нам плохого не надо, в письме может быть всякое барахло
                with open(part.get_filename(), 'wb') as new_file:

                    new_file.write(part.get_payload(decode=True))
