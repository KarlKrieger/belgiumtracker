# Documentation
# BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# Afin de récupérer les différentes données dans une page html
# 
# urllib.request: https://docs.python.org/3/library/urllib.request.html
# Pour récupérer le contenu de la page html

from bs4 import BeautifulSoup
import urllib

html_doc = urllib.request.urlopen('http://www.lachambre.be/kvvcr/showpage.cfm?section=/depute&language=fr&cfm=cvlist54.cfm?legis=54&today=y')

# Pour afficher un certain nombre de députés. Ne fonctionne pas vraiment.
NB_DEPUTE = 10

soup = BeautifulSoup(html_doc, 'html.parser')
for link in soup.find_all('td', limit=NB_DEPUTE*3):
    for line in link.find_all('a', limit=1):
        for data in line.find_all('b', limit=1):
            page_depute = str('http://www.lachambre.be/kvvcr/') + data.parent.get('href')
            page_html = urllib.request.urlopen(page_depute)
            code_depute = BeautifulSoup(page_html, 'html.parser')
            data = 'Député:   ' + " ".join(data.string.split())
            print(data)
            for img in code_depute.find_all('img', border='1', alt='Picture'):
                picture = 'http://www.lachambre.be' + img.get('src')
                print('Photo:    ' + picture)
            for niveau_1 in code_depute.find_all('td', limit=1):
                print('Langue:   ' + 'Introuvable')
                for niveau_2 in niveau_1.find_all('i', limit=1):
                    print('Langue:   ' + niveau_2.string)
            liste_mandats = []
            for niveau_1 in code_depute.find_all('div', id='story'):
                for niveau_2 in niveau_1.find_all('form', id='myform'):
                    for niveau_3 in niveau_2.find_all('div', id='section'):
                        for niveau_4 in niveau_3.find_all('div', 'menu'):
                            for niveau_5 in niveau_4.find_all('a'):
                                liste_mandats.append(niveau_5.string)
            print ('Mandats:  ' + str(liste_mandats))
            print('-------------------------------------------')
