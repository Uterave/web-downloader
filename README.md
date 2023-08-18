# web-downloader
Program do automatycznego pobierania strony HTML wraz z jej zasobami (np. zdjęcia, style, pliki PDF i dowolne inne pliki). Ma na celu usprawnienie procesu pobierania dużej ilości danych (zdjęć, PDF, ...) ze strony, aby uniknąć bardziej czasochłonnego pobierania za pomocą "Ctrl+S".

## Instrukcja
Do uruchomienia programu potrzebne są następujące zmienne:

| zmienna  | opis |
| ------------- | ------------- |
| nazwaStrony  | nazwa strony do pobrania w systemie plików  |
| url  | adres URL strony do pobrania  |
| urlPod  | adres URL do pobrania zasobów z danej strony |
| pobierzInfo  | tablica zawierająca informacje dotyczące zasobów do pobrania |

Struktura argumentów w zmiennej pobierzInfo:

| nr argumentu  | opis |
| ------------- | ------------- |
| 1  | nazwa lokalnego folderu do którego zostaną pobrane pliki  |
| 2  | rozszerzenie pobieranych plików  |
| 3  | nazwa tagu elementów do pobrania  |
| 4  | nazwa atrybutu odnosząca się do adresu URL plików do pobrania |

## Przykład użycia
```rb
def main():
  nazwaStrony = 'przedsOlimpiada.html'
  url = 'https://www.olimpiada.edu.pl/baza-wiedzy/testy/'
  urlPod = 'https://www.olimpiada.edu.pl/'

  pobierzInfo = [
      #folder, rozszerzenie, tag, atrybut
      ['prz_pliki','.pdf','a','href'],
      ['prz_style','.css','link','href'],
      ['prz_zdj','.gif','img','src'],
  ]

  pobierzStrone(nazwaStrony, url, urlPod, pobierzInfo)
  ```
W tym przykładzie zostanie pobrana strona Olimpiady z przedsiębiorczości wraz z trzema typami plików: pdf, css i gif. Zostaną stworzone lokalne dowiązania plików do strony, więc możliwe będzie otwieranie lokalnych plików (np. PDF) bezpośrednio z lokalnej strony. Lokalna strona oprócz plików PDF będzie również zawierać style (css) i zdjęcia (gif).
