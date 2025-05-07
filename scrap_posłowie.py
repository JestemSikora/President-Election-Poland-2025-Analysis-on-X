# Pobranie potrzebncy bibliotek

import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

# Z BeautifulSoup wysłanie requesta do strony Wikiperdii
url = "https://pl.wikipedia.org/wiki/Pos%C5%82owie_na_Sejm_Rzeczypospolitej_Polskiej_X_kadencji"
page = requests.get(url)
soup = BeautifulSoup(page.text, "lxml")

# Tablica na zescrapowanych posłów
poslowie = []

# Po inspekcji strony, precyzujemy która część kodu HTML nas interesuje
tables = soup.find_all("table", class_="wikitable")[2]
row_tables = tables.find_all("tr")

for row in row_tables:
    li_elements = row.find_all("li")

    for li in li_elements:
        title_value = li.get("title")
        name = li.get_text("a")
        poslowie.append(name)


# Czyścimy pobrane dane z przypisów Wikipedii
pattern = re.compile(r'\s*\[[^\]]+\]')
cleaned_poslowie = [pattern.sub('', name) for name in poslowie]

# Zapisujemy dane w pliku txt
with open('zabronione_konta', 'w', encoding='utf-8') as file:
    for posel in cleaned_poslowie:
        file.write(posel + '\n')
