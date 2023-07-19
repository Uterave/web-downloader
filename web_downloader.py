#Python 3.10
import requests
import os
from bs4 import BeautifulSoup

#pobiera plik z url i zapisuje do nazwaFolderu/nazwaPliku
def pobierz(url : str, nazwaPliku : str, nazwaFolderu: str, czyWysw=True):
    if czyWysw:
        print(f'pobieram {url}') 
    try:
        odp = requests.get(url)
    except requests.exceptions.ConnectionError as blad:
        print(f'błąd {blad}')
        return 1
    if odp.status_code != 200:
        print(f'niepoporawny statuscode {odp.status_code} {url}')
        return 1
    
    nowaNazwaP = url.split('/')[-1]
    if nazwaFolderu == '':
        if nazwaPliku == '':
            nazwaPliku = nowaNazwaP
            sciezka = os.path.join(nazwaPliku)
        else:
            sciezka = os.path.join(nazwaPliku)
    else:
        if not os.path.exists(nazwaFolderu):
            os.mkdir(nazwaFolderu)
        if nazwaPliku == '':
            nazwaPliku = nowaNazwaP
            sciezka = os.path.join(nazwaFolderu,nazwaPliku)
        else:
            sciezka = os.path.join(nazwaFolderu,nazwaPliku)

    with open(sciezka,'wb') as plik:
        plik.write(odp.content)
    if czyWysw:
        print(f'pobrano {url} -> {nazwaFolderu+"/" if nazwaFolderu != "" else ""}{nazwaPliku}')
    return 0

def zwrocTabliceUrl(nazwaPliku: str, podstawowyURL: str, rozszerzenie: str, tagZew, tagWew, czyDodacUkosnik=True):
    tab = []
    if not os.path.exists(nazwaPliku):
        print(f'ścieżka do "{nazwaPliku}" nie istnieje')
        return tab
    with open (nazwaPliku,'rb') as plik:
        dane = plik.read()
    soup = BeautifulSoup(dane, 'html.parser')
    for adres in soup.find_all(tagZew):
        adr = str(adres.get(tagWew,""))
        if adr.endswith(rozszerzenie):
            if adr.__contains__('http'):
                if not adr in tab:
                    tab.append(adr)
            else:
                nowy = podstawowyURL+adr
                if czyDodacUkosnik:
                    nowy = podstawowyURL+'/'+adr
                if not nowy in tab:
                    tab.append(nowy)
    return tab

def pobierzTabliceUrl(tablica, nazwaFolderu): #pobiera tablicę do nazwaFolderu
    liczbaBledow = 0
    coIleOdswiezac = 10
    print(f'plików do pobrania: {len(tablica)}')
    for i in range(len(tablica)):
        liczbaBledow += pobierz(tablica[i],'',nazwaFolderu,0)
        if (i+1) % coIleOdswiezac == 0:
            print(f'przetworzono {i+1}')
    print(f'liczba błędów: {liczbaBledow}')
    if liczbaBledow == 0:
        print('pobrano wszystko')
    return


def stworzLokalneUrl(nazwaPliku, nazwaFolderu, rozszerzenie, tagZew, tagWew): # zmienia adresy URL na lokalne
    if not os.path.exists(nazwaPliku):
        print(f'ścieżka do "{nazwaPliku}" nie istnieje. Nie można stworzyć lokalnych dowiązań')
        return
    with open (nazwaPliku,'rb') as plik:
        dane = plik.read()
    soup = BeautifulSoup(dane, 'html.parser')
    for adres in soup.find_all(tagZew):
        adr = str(adres.get(tagWew,""))
        if adr.endswith(rozszerzenie):
            nowy = nazwaFolderu+'/'+adr.split('/')[-1]
            adres[tagWew] = nowy
    nowaStrona = soup.prettify()
    with open(nazwaPliku,'w',encoding='utf-8') as plik:
        plik.write(nowaStrona)
    return

def usunJs(nazwaStrony): #usuwa JS i inne elementy ze strony
    if not os.path.exists(nazwaStrony):
        print(f'ścieżka do "{nazwaStrony}" nie istnieje. Nie można usunąć JS')
        return
    with open (nazwaStrony,'rb') as plik:
        dane = plik.read()
    soup = BeautifulSoup(dane, 'html.parser')
    for skrypt in soup.find_all('script'):
        skrypt.string = ''
        if 'src' in skrypt.attrs:
            skrypt['src'] = ''
    for base in soup.find_all('base'): #usuwamy href z <base />
        if 'href' in base.attrs:
            base['href'] = ''
    nowaStrona = soup.prettify()
    with open(nazwaStrony,'w',encoding='utf-8') as plik:
        plik.write(nowaStrona)

    return

def pobierzStrone(nazwaStrony,urlStrony, urlPodstawowy, pobierzInfo):
    pobierz(urlStrony,nazwaStrony,'')
    usunJs(nazwaStrony)
    for el in pobierzInfo:
        tab = zwrocTabliceUrl(nazwaStrony, urlPodstawowy, el[1], el[2], el[3], 0)
        print(f'pobieram {el[0]} {el[1]} {el[2]} {el[3]}')
        pobierzTabliceUrl(tab, el[0])
    for el in pobierzInfo:
        stworzLokalneUrl(nazwaStrony,el[0], el[1], el[2], el[3])

    return

def main():

    nazwaStrony = 'przedsOlimpiada.html'
    url = 'https://www.olimpiada.edu.pl/baza-wiedzy/testy/'
    urlPod = 'https://www.olimpiada.edu.pl/'

    pobierzInfo = [
        #folder, rozszerzenie, tagZew, tagWew
        ['prz_pliki','.pdf','a','href'],
        ['prz_style','.css','link','href'],
        ['prz_zdj','.gif','img','src'],
    ]

    pobierzStrone(nazwaStrony, url, urlPod, pobierzInfo)

    return
    

main()
