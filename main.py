from requests_html import HTMLSession
import pprint
import os
import re
import time
import pandas
from bs4 import BeautifulSoup

pp = pprint.PrettyPrinter(indent=2)

print('Welcome to your best betting advisor!')

url = 'https://www.flashscore.pl/'

html = ''
date = ''

'''
:param url:
:return:

x is returned table with all event info in such configuration:
a) upcoming
[id, state, Time, Home, "-", Away]
b) live
[id, state, Stage, Home, Score, Away, Half-time]
c) past
[id, state, Stage, Home, Score, Away, Half-time]

if Stage is null then a)
else if Stage is int between (0,130) then b)
else then c)

update for check up on a) and b)
c) is terminated and archived
'''
x = []

# create an HTML Session object
session = HTMLSession()

print(session.cookies)

def getPostJS(url):

    # Use the object above to connect to needed webpage
    r = session.get(url)

    print(r.cookies)

    # Run JavaScript code on webpage
    r.html.render()

    # return generated html
    return r.html.html

#find meaning of tokens jig-saw

def resolve(arr):
    result = []
    tmp_line = ''
    soup = BeautifulSoup(html, 'html.parser')
    for a in arr:
        line = soup.find(text = re.compile(str(a)))
        # try:
        if isinstance(line, str) and line is not tmp_line and len(line) < 30:
           # print('a: '+line)
           result.append(line)
           tmp_line = line
           # print([(x,y) for x in line for y in result])
           tokens = line.split()
           print([(x,y) for x in tokens for y in result if x == y ])
        else:
            pass

    if len(result) == 3:
        line0 = soup.find(text = re.compile(result[0]))
        # line1 = soup.find(text = re.compile(result[1]))
        # line2 = soup.find(text = re.compile(result[2]))

        print('When 3(0): '+str(line0) +'\n')


    return result

def log(msg):
    # file = open('log.txt', 'a+')
    t = time.localtime()
    ct = time.strftime("%H:%M:%S", t)
    print(ct +" "+ msg)
    # f.write()

def append_to_csv(r1, r2):
    # create directory for today

    folder_name = str
    folder = os.path.join(os.path.dirname(os.path.abspath(__file__))
                          +'/'+str(date))
    file_name = '{}.txt'.format(folder_name)
    file = os.path.join(folder, file_name)
    os.makedirs(folder)
    with open(file, 'w') as f:
        f.write('Some text')

    # with open(str(date)+'//matches.csv', mode='a+') as mf:
    #     fieldnames = ['Stage', 'Home', 'Score', 'Away', 'Half-time']
    #
    #     mf_writer = csv.DictWriter(mf, fieldnames=fieldnames)
    #
    #     mf_writer.writeheader()
    #     mf_writer.writerow({'Stage' : r2[0],
    #                         'Home' : r1[0], 'Score' : '-', 'Away' : r1[1], 'Half-time' : '-'})


    # Pandas write

    # df = pandas.read_csv(str(date)+'//matches.csv', index_col='Stage', names=['Stage', 'Home', 'Score', 'Away', 'Half-time'])
    # df.to_csv()


# MAIN #

html = getPostJS(url)

# BeautifulSoup approach
soup = BeautifulSoup(html, 'html.parser')
'''
    Find a tag element with a  given class
    soup.find_all('div', {"class":"event__"})
    '''
divs = soup.find_all('div', {"class":"event__match"})

teams = soup.find_all('div', {'class':'event__participant'})

date = soup.find('div', {'class': 'calendar__datepicker'})
date = date.text[:5]
# print(f"today's ({date}) matches:")

# print Matches

for d in divs:
    # keys = ['kobiety']
    # if any(word in d for word in keys):
    # print(type(d.text))
    # if [re.findall('ŚWIAT:', str(d))]:
    #     pass

    r1 = re.findall(r"[A-Z]{1,2}[a-z]*", d.text)
    r2 = re.findall(r"[\d]+[:][\d]+", d.text)

    print(r1)
    print(r2)

    # if r1[0] == 'Atl':
    #     print(r1[0])
    #     r1 = resolve(r1)
    #     print(r1)

    if len(r1) != 2:
        print('% TRANSFORMATION %')
        r1 = resolve(r1)
        print(r1)
        print(r2)
        # print(f'Match between {r1[0]} and {r1[1]} is going to start at {r2}')
        #append_to_csv(r1,r2)

        # except:
        #     print("Can't load "+str(r1))