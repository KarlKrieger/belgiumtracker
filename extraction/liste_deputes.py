# Documentation
# BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# Afin de récupérer les différentes données dans une page html
# 
# urllib.request: https://docs.python.org/3/library/urllib.request.html
# Pour récupérer le contenu de la page html

from bs4 import BeautifulSoup
import urllib
# import warnings
# warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

url = 'http://www.lachambre.be/kvvcr/showpage.cfm?section=/depute&language=fr&cfm=cvlist54.cfm?legis=54&today=y'
html_doc = urllib.request.urlopen(url)

NB_DEPUTE = 5

niveau_max = BeautifulSoup(html_doc, 'html.parser')

fichier = 'seances_deputes' + '.csv'
doc = open(fichier, 'w')
doc.write('name,first_name,last_name,parti_id,date_naissance,date_deces,genre,langue,site,email,photo' + '\n')

# Fouille les données de la page du député
def fouille_depute(url):
    code_depute = BeautifulSoup(url, 'html.parser')
    for niveau_0 in code_depute.find_all('img', border='1', alt='Picture'):
        picture = 'http://www.lachambre.be' + niveau_0.get('src')
        print('Photo:    ' + picture)
    print(url)
    for niveau_0 in code_depute.find_all('td', limit=1):
        print('Langue:   ' + 'Introuvable')
        for niveau_1 in niveau_0.find_all('i', limit=1):
            print('Langue:   ' + niveau_1.string)
            liste_mandats = []
            for niveau_0 in code_depute.find_all('div', id='story'):
                for niveau_1 in niveau_0.find_all('form', id='myform'):
                    for niveau_2 in niveau_1.find_all('div', id='section'):
                        for niveau_3 in niveau_2.find_all('div', 'menu'):
                            for niveau_4 in niveau_3.find_all('a'):
                                liste_mandats.append(niveau_4.string)
            print ('Mandats:  ' + str(liste_mandats))

print('-------------------------------------------')

for niveau_0 in niveau_max.find_all('tr', limit=NB_DEPUTE):
    url_depute = ' '
    i = 1
    for niveau_1 in niveau_0.find_all('td'):
        if i == 1:
            i = i + 1
            for niveau_2 in niveau_1.find_all('a', limit=1):
                url_depute = str('http://www.lachambre.be/kvvcr/') + str(niveau_2.get('href'))
                text = niveau_2.find('b').string
                name = " ".join(text.split())
                print('Député:   ' + name)
                doc.write(name)
                doc.write(',')
                
                # Séparer les noms et prénoms
                first_name = 'prénom'
                doc.write(first_name)
                doc.write(',')

                last_name = 'nom'
                doc.write(last_name)
                doc.write(',')

        elif i == 2:
            i = i + 1
            parti_id = niveau_1.find('a').string
            parti_id = str(" ".join(parti_id.string.split()))
            print('Parti:    ' + parti_id)
            doc.write(parti_id)
            doc.write(',')
            doc.write('\n')
        elif i == 3:
            i = i + 1
            try:
                text = niveau_1.find('a', 'mail').string[::-1]
            except TypeError:
                text = 'Pas d\'adresse mail'
            print('E-mail:   ' + str(text))
        else:
            try:
                text = niveau_1.find('a', target='_blank').get('href')
            except NameError:
                text = 'Pas de site web'
            except AttributeError:
                text = 'Pas de site web'
            print('Site:     ' + str(text))
    
    fouille_depute(url_depute)

    print('---------------------------------------')

doc.close
