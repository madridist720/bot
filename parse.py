from urllib.request import urlopen as ur
from bs4 import BeautifulSoup as b


def plus_flag(name):

    if 'Италии' in name:
        flag = '🇮🇹'
    elif 'Испании' in name:
        flag = '🇪🇸'
    elif 'Англии' in name:
        flag = '🏴󠁧󠁢󠁥󠁮󠁧󠁿'
    elif 'Франции' in name:
        flag = '🇫🇷'
    elif 'Португалии' in name:
        flag = '🇵🇹'
    elif 'России' in name:
        flag = '🇷🇺'
    else:
        flag=''
    return flag+name[:35]
def get_top_machts():
    html = ur('http://football.kulichki.net/')
    bs = b(html.read())
    div = bs.find('div', {"class":'col2 inl vtop'}).center.table
    tr_list = div.find_all('tr')
    result = ''
    for item in tr_list[1:]:
        if item.find('span') is not None:

            flag = plus_flag(item.find('span').text)
            plus_flag(flag)
            result = result + flag + '\n'
        else:
            a = item.find('p', {"align":"left"}).text
            a = a.replace('\n', '')
            a = a.replace('  ', ' ')
            matchtime = a[1:a.index('.')]
            timeplus = (int(matchtime[:2]) + 2) % 24
            timeplus = str(timeplus)
            if len(timeplus)==1:
                timeplus = '0'+timeplus

            matchname = a[a.index('.')+2:a.rindex('-')]
            result = result+ '*'+timeplus+matchtime[2:]+'* _'+ matchname +'_\n'
    return result
