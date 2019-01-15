# Documentation
# BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# Afin de récupérer les différentes données dans une page html
# 
# urllib.request: https://docs.python.org/3/library/urllib.request.html
# Pour récupérer le contenu de la page html

from bs4 import BeautifulSoup
import urllib.request

# Nombre de séances plénières à afficher. S'il faut les afficher toutes, 
# retirer l'attribut 'limit' dans la première boucle for
NB_MAX = 1000

N_LEGISLATURE = 54

# Récupération du code source de la page

url = 'http://www.lachambre.be/kvvcr/showpage.cfm?section=/cricra&language=fr&cfm=dcricra.cfm?type=plen&cricra=cri&count=all&legislat=' + str(N_LEGISLATURE)
html_doc = urllib.request.urlopen(url)

soup = BeautifulSoup(html_doc, 'lxml')
fichier = 'seances_legislature_' + str(N_LEGISLATURE) + '.csv'
doc = open(fichier, 'w')
doc.write('name,legislature_id,date,moment,approuve' + '\n')
for link in soup.find_all('tr', valign='top', limit=NB_MAX):
    record = ''
    # Numéro de la séance
    for line in link.find_all('td', height="25px", limit=1):
        for data in line.find_all('a'):
            print(str('ID:          ') + data.string)
            record = record + data.string + ','
    # Numéro de la législature
    print('Legistature: ' + str(N_LEGISLATURE))
    record = record + str(N_LEGISLATURE) + ','
    # Récupération de la date: JJ mois YYYY
    for line in link.find_all('td', style='line-height: 1.0em;', width='110px', limit=1):
        line = " ".join(line.string.split())
        print(str('Date:        ') + line)
        jour, mois, annee = line.split(' ',2)
        def mois_en_chiffre(mois):
            return {
                'janvier': '01',
                'février': '02',
                'mars': '03',
                'avril': '04',
                'mai': '05',
                'juin': '06',
                'juillet': '07',
                'août': '08',
                'septembre': '09',
                'octobre': '10',
                'novembre': '11',
                'décembre': '12'
            }.get(mois, 'NOT FOUND')
        record = record + annee + str(mois_en_chiffre(mois)) + jour + ','

    # Récupération du jour et du moment de la journée (AM, PM, Soir)
    for line in link.find_all('i', style='font-size: 1.0em;color: 999999;', limit=1):
        line = " ".join(line.string.split())
        try:
            jour, moment = line.split(' ',1)
        except ValueError:
            jour = 'jour'
            moment = 'journée'
        print(str('Moment:      ') + str(moment) + '\n' + str('Jour:        ' + str(jour)))
        record = record + moment + ','

    # Récupération du lien pour le pdf structuré, la brochure bilingue et le contenu en html
    for line in link.find_all('a', title='La brochure imprim?e', limit=1):
        print(str('Pdf:         ') + str('www.lachambre.be') + line.get('href'))
    for line in link.find_all('a', title='PDF structuré', limit=1):
        print(str('Pda:         ') + str('www.lachambre.be') + line.get('href'))
    for line in link.find_all('a', title='Version HTML prête à copier', limit=1):
        print(str('Text:        ') + str('www.lachambre.be') + line.get('href'))
    
    # Récupération du statut du PV de la séance (approuvé ou pas)
    for line in link.find_all('i', style='font-size: 0.9em;color: 999999;', limit=1):
        line = " ".join(line.string.split())
        if line == 'version définitive':
            version = 'True (définitive)'
            approuve = 'true'
        else:
            version = 'False (provisoire)'
            approuve = 'false'
        print(str('Version:     ') + version)
        record = record + approuve
    
    # Vérifie s'il y a une annexe ou pas. Si oui, donne le lien. Sinon, n'affiche rien.
    # limit=4 parce le style est le même que pour les 3 documents 
    # pdf/pda/text et que je ne veux que l'annexe.        
    for line in link.find_all('td', style='line-height: 1.0em;', width='70px', limit=4):
        for data in line.find_all('a'):
            if data.string == 'Annexe':
                print('Annexe:      ' + 'www.lachambre.be' + data.get('href'))
    print('csv:         ' + record)
    doc.write(record + '\n')
    print('-------------------------------------')
doc.close
