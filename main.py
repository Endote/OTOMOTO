from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests
import re

# Press the green button in the gutter to run the script.
session = HTMLSession()

url = 'https://www.otomoto.pl'
cat = ['osobowe', 'czesci', 'dostawcze', 'motocykle-i-quady', 'ciezarowe', 'maszyny-budowlane', 'przyczepy', 'rolnicze']

f_link = ''

act_url = url



act_cat = -1
act_brand = ''
act_model = ''
act_from = ''
act_location = ''
act_min_price = ''
act_max_price = ''
act_to = ''
act_mileage_from = ''
act_mileage_to = ''
act_fuel_type = ''
act_country = ''


def set_cat(int):
    global act_cat
    global act_url
    try:
        act_cat = int
        act_url = f'{act_url}/{cat[act_cat]}'
    except:
        print('set cat failed')

def set_brand(txt):
    global act_brand
    global act_url
    try:
        act_brand = txt
        act_url = f'{act_url}/{act_brand}'
    except:
        print('set brand failed')

def set_model(txt):
    global act_model
    global act_url
    try:
        if not act_brand:
            raise
        act_model = txt
        act_url = f'{act_url}/{act_model}'
    except:
        print('set model failed')

def set_from(txt):
    global act_from
    global act_url
    try:
        act_from = txt
    except:
        print('set from failed')

def set_location(txt):
    global act_location
    global act_url
    try:
        act_location = txt
    except:
        print('set location failed')


def choose_cat():
    print('Wybierz kategorię spośród podanych, wpisz liczbę:')
    global act_cat
    for indx, c in enumerate(cat):
        print(str(indx)+'. '+c)
    act = input('Interesuje Cię kategoria numer?  ')
    try:
        if int(act) == 3 or int(act) == 0:
            raise
        print('\nWybrana kategoria to: ' + cat[int(act)] +'\n')
        act_cat = act
    except:
        print('Kategoria nie jest obsługiwana')
        choose_cat()

def choose_brand():
    r = session.get(act_url)
    r.html.render()

    '''
        Find a tag element with a  given class
        soup.find_all('div', {"class":"event__"})
    '''
    soup = BeautifulSoup(r.html.html, 'html.parser')
    brands = soup.find('select', {'title':'Marka pojazdu'}).text.split('\n')
    brands = brands[1:]
    print('Możliwe marki: ')
    for indx, b in enumerate(brands):
        if b == brands[0]:
            pass
        else:
            try:
                tokens = b.split()
                print(tokens[:-1], tokens[-1], ' aktywnych ogłoszeń')
            except:
                print('To wszystkie marki pojazdów \n')
    act = input('Wpisz nazwę marki, jak wyżej:   ')

    # try:
    #     if str(act) not in [x[0] for x in brands]:
    #         raise
    #     return act
    # except:
    #     print('Podana Marka jest niewłaściwa')
    #     chooseBrand()

    # while str(act) not in [x for x in brands]:
    #     act = input('Wpisz POPRAWNĄ nazwę marki:   ')

    return act


'''
Task manager attempt

def runMenu(x):
        print('wtf')
        switcher = {
            0: (chooseCat()),
            1: (chooseBrand()),
            2: (chooseModel()),
        }
        return switcher.get(x, 'nothing')
'''


def choose_model():
    r = session.get(act_url)
    r.html.render()

    '''
        Find a tag element with a  given class
        soup.find_all('div', {"class":"event__"})
    '''
    soup = BeautifulSoup(r.html.html, 'html.parser')
    models = soup.find('select', {'title':'Model pojazdu'}).text.split('\n')


    models = models[1:]
    print('Możliwe marki: ')

    tokens = str(models[0])[7:]
    tokens = tokens.split()
    print(*tokens[::2], sep ='\n')
    act = input('Wybierz model:   ')
    return act

def get_links(urll):
    # r = session.get(act_url)
    # r.html.render()
    r = requests.get(urll)

    soup = BeautifulSoup(r.text, 'html.parser')
    adds = []

    for a in soup.find_all('a', href=True):
        if str(a['href']).startswith('https://www.otomoto.pl/oferta'):
            #print('found the URL: ', a['href'])
            if a['href'] not in adds:
                adds.append(a['href'])

    return adds

def get_details(url):
    details = []
    params  = []
    r = requests.get(url=str(url))


    soup = BeautifulSoup(r.text, 'html.parser')

    labels = soup.find_all('span', {'class': 'offer-params__label'})
    values = soup.find_all('div', {'class': 'offer-params__value'})
    price  = soup.find('span', {'class': 'offer-price__number'})

    details_dict = {
        'Cena': price.text.strip()
    }

    for i in range(0, len(labels)-1):
        # params.append([labels[i].text.strip(), values[i].text.strip()])
        details_dict[labels[i].text.strip()] = values[i].text.strip()


    # print(params)

    # print(str(params[4])+' '+str(params[5])+' '+str(params[6]))

    details.append(details_dict)
    details.append(url)

    return details


def f_link_builder():
    link = f'https://www.otomoto.pl'
    for p in OMParams:
        if p:
            if p == act_from:
                link += '/od-'+str(p)
            else:
                link += '/'+str(p)
    return link


if __name__ == '__main__':
    print('Witaj w przeglądarce OTOMOTO')
    print('#!# Jesli zostawisz puste pole to pokażesz wszystkie opcje #!#')

#    Step by step filling

    # act_cat = chooseCat()
    # act_url = f'{act_url}/{cat[3]}'
    choose_cat()
    # act_brand = choose_brand()
    # act_url = f'{act_url}/{act_brand}'
    set_brand('BMW')
    # act_model = chooseModel()
    # act_url = f'{act_url}/{act_model}'
    set_model('C1')

    # set_from(2021)

    #set_location('/Warszawa')

    #act_url = 'https://www.otomoto.pl/motocykle-i-quady/suzuki/rm-z/'

    # print(act_url)

    OMParams = [cat[act_cat], act_brand, act_model, act_from, act_location, act_min_price, act_max_price,
                act_to, act_mileage_from, act_mileage_to, act_fuel_type, act_country]

    f_link = f_link_builder()
    print(f_link)
    print(cat[0])
    #
    # f_link = f'https://www.otomoto.pl/{act_cat}/{act_brand}/{act_model}/od-{act_from}{act_location}/?search%5Bfilter_float_price%3Afrom%5D={act_min_price}&search%5Bfilter_float_price%3Ato%5D={act_max_price}&search%5Bfilter_float_year%3Ato%5D={act_to}&search%5Bfilter_float_mileage%3Afrom%5D={act_mileage_from}&search%5Bfilter_float_mileage%3Ato%5D={act_mileage_to}&search%5Bfilter_enum_fuel_type%5D%5B0%5D={act_fuel_type}&search%5Bfilter_enum_country_origin%5D%5B0%5D={act_country}&'
    #
    # links = get_links(f_link)
    # for link in links:
    #     print(*get_details(link), sep='\n')