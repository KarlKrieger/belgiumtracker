# -*- coding: utf-8 -*

from bs4 import BeautifulSoup, SoupStrainer
import urllib

##################
#                #
#     TO DO      #
#                #
##################
#
# 1. Gérer la récupération du numéro des votes et du vote annulé
# 2. Gérer la concaténation de la liste des députés. Attention qu'il faut rajouter des espaces en fin de ligne.
#

# Pour tester, faire varier le numéro de la séance
SEANCE = '262'

url = 'http://www.lachambre.be/doc/PCRI/html/54/ip'+ str(SEANCE) + 'x.html'
fichier = 'seance_' + str(SEANCE) +'.txt'
html_doc = urllib.request.urlopen(url)

# Récupération uniquement des données contenues dans le <body> de la page, car il y a plus haut 1000 lignes de css en commentaire dans le code. -_-
doc = BeautifulSoup(html_doc, 'lxml', parse_only=SoupStrainer('body')).text

# Retire les lignes blanches du fichier
def remove_empty_lines(filename):
    with open(filename) as f:
        lines = f.readlines()
    with open(filename, 'w') as f:
        lines = filter(lambda x: x.strip(), lines)
        f.writelines(lines)

# Ecrit le code html dans le fichier
with open (fichier, 'w') as f:
    f.write(str(doc))

# Lance le retrait des lignes blanches
remove_empty_lines(fichier)

# Phrase à rechercher pour localiser les votes en fin de fichier
vote = 'Naamstemming: '

ligne_votes = []

# Récupération du numéro de la ligne du début du vote
with open(fichier, 'r') as f:
    num = 0
    for num, ligne in enumerate(f, 1):
        if vote in ligne:
            ligne_votes.append(num)
    ligne_votes.append(num)

liste_votes = []

# Récupération du reste du vote
with open(fichier, 'r') as f: 
    lines = f.readlines()
    # Boucle entre le début du vote et le début du vote suivant
    for compteur in range(0, len(ligne_votes) - 1):
        debut = ligne_votes[compteur] -1
        fin = ligne_votes[compteur + 1] -2
        temp = []
        # Suppression des '\n' et '\xa0'
        for i in range(debut, fin):
            data = lines[i].rstrip('\n')
            data = lines[i].rstrip()
            temp.append(data)

        #########
        # TO DO #
        #########
        # Récupérer uniquement les 3 derniers caractères du temp [0] qui donne le numéro du vote.
        # Gérer le vote numéro 37 qui a été annulé
        print(temp[0])
        
        #########
        # TO DO #
        #########
        # Il faut concaténer les députés dans le même élément de la liste car les lignes ont été découpées au moment de la récupération du code html.
        # Pour le moment, le code est foireux. Il met tout dans la case des OUI.
        # Ne pas oublier de rajouter des espaces en fin de ligne pour ne pas joindre noms et prénoms.
        resultats = []
        resultats.append(temp.index('Oui'))
        resultats.append(temp.index('Non'))
        resultats.append(temp.index('Abstentions'))
        
        # REGROUPER PAR VOTE
        vote = []
        for i in temp:
            # OUI
            vote.append(temp[resultats[0]])
            vote.append(temp[resultats[0]+1])
            j = 2
            while j < resultats[1]:
                data += ' ' + str(temp[resultats[0]+j])
                j += 1
            vote.append(data)
        liste_votes.append(vote)
