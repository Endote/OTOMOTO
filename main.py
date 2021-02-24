from requests_html import HTMLSession
from bs4 import BeautifulSoup
import requests
import re


class OTOMOTO:
    def __init__(self):
        print('Witaj w przeglądarce OTOMOTO')
        self.session = HTMLSession()

        self.search_history = []

        self.url = 'https://www.otomoto.pl'
        self.cat = ['osobowe', 'czesci', 'dostawcze', 'motocykle-i-quady',
                    'ciezarowe', 'maszyny-budowlane', 'przyczepy', 'rolnicze']

        self.f_link = ''

        self.act_url = self.url

        self.act_cat = 0
        self.act_brand = ''
        self.act_model = ''
        self.act_from = ''
        self.act_location = ''
        self.act_min_price = ''
        self.act_max_price = ''
        self.act_to = ''
        self.act_mileage_from = ''
        self.act_mileage_to = ''
        self.act_fuel_type = ''
        self.act_country = ''
        self.act_search = ''

        self.user()

    def param_switch(self, x):
        switcher = {
            0: 'Marka',
            1: "Model",
            2: "Minimalny rok produkcji",
            3: "Maksymalny rok produkcji",
            4: "Minimalna Cena",
            5: "Maksymalna Cena",
            6: "Lokalizacja",
            7: "Minimalny Przebieg",
            8: "Maksymalny Przebieg",
            9: "Typ Paliwa",
            10: "Kraj",
            11: "Fraza",
            #12: "December"
        }
        print(switcher.get(x, 'Nie odnaloziono parametru...'))

    def user(self):
        for indx, c in enumerate(self.cat):
            print(indx, c)
        self.act_cat = self.choose_cat()
        print('0 Marka')
        print('1 Model (tylko jeśli Marka została wybrana)')
        print('2 Minimalny rok produkcji')
        print('3 Maksymalny rok produkcji')
        print('4 Minimalna Cena')
        print('5 Maksymalna Cena')
        print('6 Lokalizacja')
        print('7 Maksymalna Cena')
        print('8 Maksymalna Cena')
        print('9 Typ Paliwa')
        print('10 Kraj')
        print('11 Fraza')


        x = input('Ustal parametry z listy...\nWybierz cyfrę parametru, który chcesz zmienić  ')

        print(self.param_switch(x))


    def set_cat(self, int):
        global cat
        global act_cat
        global act_url
        try:
            act_cat = int
            act_url = f'{act_url}/{cat[act_cat]}'
        except:
            print('set cat failed')

    def set_brand(self, txt):
        try:
            self.act_brand = txt
            self.act_url = f'{self.act_url}/{self.act_brand}'
        except:
            print('set brand failed')

    def set_model(self, txt):
        global act_model
        global act_url
        try:
            if not self.act_brand:
                raise
            act_model = txt
            act_url = f'{act_url}/{act_model}'
        except:
            print('set model failed')

    def set_from(self, txt):
        global act_from
        global act_url
        try:
            act_from = txt
        except:
            print('set from failed')


    def set_location(self, txt):
        global act_location
        global act_url
        try:
            act_location = txt
        except:
            print('set location failed')


    def set_min_price(self, txt):
        global act_min_price
        global act_url
        try:
            act_min_price = txt
        except:
            print('set min price failed')


    def set_max_price(self, txt):
        global act_max_price
        global act_url
        try:
            act_max_price = txt
        except:
            print('set max price failed')


    def set_search(self, txt):
        global act_search
        global  act_url
        try:
            act_search = txt
        except:
            print('set search failed')


    def choose_cat(self):
        try:
            act = int(input('Interesuje Cię kategoria numer?  '))
            if act == 3 or act == 0:
                print(f'Wybrana Kategoria: {self.cat[act]}')
                return act
            else:
                raise
        except:
            print('Kategoria nie jest obsługiwana')
            self.choose_cat()

    def choose_brand(self):
        r = self.session.get(act_url)
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


    def choose_model(self):
        r = self.session.get(act_url)
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


    def get_links(self, urll):
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


    def get_details(self, url):
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


    def f_link_builder(self):

        OMParams = [self.cat[self.act_cat], self.act_brand, self.act_model,
                    self.act_from, self.act_location, self.act_min_price, self.act_max_price,
                    self.act_to, self.act_mileage_from, self.act_mileage_to, self.act_fuel_type,
                    self.act_country, self.act_search]

        link = f'https://www.otomoto.pl'
        query = False
        for p in OMParams:
            if p:
                if p == self.act_min_price:
                    if not query:
                        link += '/'+f'?search%5Bfilter_float_price%3Afrom%5D={str(p)}'
                        query = True
                        continue
                    else:
                        link += '/'+f'&search%5Bfilter_float_price%3Afrom%5D={str(p)}'

                if p == self.act_max_price:
                    if not query:
                        link += '/'+f'?search%5Bfilter_float_price%3Ato%5D={str(p)}'
                        query = True
                        continue
                    else:
                        link += '/'+f'&search%5Bfilter_float_price%3Ato%5D={str(p)}'
                if p == self.act_search:
                    link += '/q-'+str(p)
                    continue
                if p == self.act_from:
                    link += '/od-'+str(p)
                else:
                    link += '/'+str(p)
        return link


if __name__ == '__main__':
    # print('#!# Jesli zostawisz puste pole to pokażesz wszystkie opcje #!#')

#    Step by step filling

    om = OTOMOTO()
    #
    # om.set_brand('BMW')
    #
    # om.f_link = om.f_link_builder()
    # print(om.f_link)
    # print(cat[0])
    #
    # f_link = f'https://www.otomoto.pl/{act_cat}/{act_brand}/{act_model}/od-{act_from}{act_location}/?search%5Bfilter_float_price%3Afrom%5D={act_min_price}&search%5Bfilter_float_price%3Ato%5D={act_max_price}&search%5Bfilter_float_year%3Ato%5D={act_to}&search%5Bfilter_float_mileage%3Afrom%5D={act_mileage_from}&search%5Bfilter_float_mileage%3Ato%5D={act_mileage_to}&search%5Bfilter_enum_fuel_type%5D%5B0%5D={act_fuel_type}&search%5Bfilter_enum_country_origin%5D%5B0%5D={act_country}&'
    #
    # links = om.get_links(om.f_link)
    # for link in links:
    #     print(*om.get_details(link), sep='\n')