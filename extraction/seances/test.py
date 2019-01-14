#!/usr/bin/env python
# test.py
import re

from bs4 import BeautifulSoup
from bs4 import SoupStrainer

import urllib

url = 'http://www.lachambre.be/doc/PCRI/html/54/ip264x.html'

html_doc = urllib.request.urlopen(url)

soup = BeautifulSoup(html_doc, 'lxml', parse_only=SoupStrainer('body')).get_text()

fichier = open('seance_54_264.txt', 'w')

fichier.write(soup)
fichier.close

def traiterCR(fichier):
    """ premier traitement de forme afin d'obtenir un fichier "propre" sans lignes blanches """
    
    
    fichier_nouveau = fichier[0:5]
    lines = []

    with open(fichier, "r") as f:
        line = f.readlines()

    for char in line:
            if (char != "\n" and
            char != " \n" and
            char != "\t\n"):
                lines.append(char)

    with open(fichier_nouveau, "w") as f:
            for char in lines:
                f.write(char)
    
    with open(fichier_nouveau, "r") as f:
        chaine = f.readlines()
    
    print('TraiterCR is ok.')

    return chaine

    
def obtenirNumero(vote):
    if vote > 9:
        numero = str(vote)
    else:
        numero = "0" + str(vote)
    return numero

    
def extractionNom(vote, chaine, oui, non, abs):

    titre = "Vote nominatif - Naamstemming: 0" + obtenirNumero(vote)
    i = 0
    
    for ligne in chaine:
        if ligne[0:34] == titre:
            if oui != 0:
                iOui = i+4
            else:
                iOui = i+3
            
            if non != 0:
                iNon = iOui+4
            else:
                iNon = iOui+3
                
            if abs != 0:
                iAbs = iNon+4
            else:
                iAbs = iNon+3
            print('OK !')
            nomOUI = chaine[iOui].split(", ")
            nomNON = chaine[iNon].split(", ")
            nomABS = chaine[iAbs].split(", ")
        i +=1

    return nomOUI, nomNON, nomABS
                
def extractionVote(chaine):
    
    i = 0
    voteTotal = 0
    voteDoublon = 0
    for ligne in chaine:
        if ligne[0:14] == "(Stemming/vote":
            try:
                ligneVote = chaine[i]
                try:
                    nbVote = int(ligneVote[15:17])
                except ValueError:
                    nbVote = int(ligneVote[15:16])
                ligneOui = chaine[i+2]
                nbOui = int(ligneOui[0:3])
                ligneNon = chaine[i+5]
                nbNon = int(ligneNon[0:3])
                ligneAbs = chaine[i+8]
                nbAbs = int(ligneAbs[0:3])
                lignetotal = chaine[i+11]
                nomOUI, nomNON, nomABS = extractionNom(nbVote, chaine, nbOui, nbNon, nbAbs)    
                nbTotal = int(lignetotal[0:3])
                voteTotal = voteTotal+1
                if nbVote < 10:
                    nbVote = '0' + str(nbVote)
                vote_fichier = 'votes/vote_' + str(nbVote) + '.txt'
                doc = open(vote_fichier, 'w')
                doc.write('Type de vote:' + '\n')
                data = "Vote n°" + str(nbVote) + " ayant reçu " + str(nbOui) + " OUI, " + str(nbNon) + " NON et " + str(nbAbs) + " abstention, pour un total de " + str(nbTotal) + " votes." + "\n"
                print (data)
                doc.write(data)

                doc.write('Résultat du vote:' + '\n')
                data = "Personnes ayant voté POUR : " + str(nomOUI) + "\n"
                doc.write(data)
                data = "Personnes ayant voté CONTRE : " + str(nomNON) + "\n"
                doc.write(data)
                data = "Personnes ayant voté ABSTENTION : " + str(nomABS)
                doc.write(data)
            except ValueError:
                voteDoublon = voteDoublon+1
                # print("Vote doublon du précédent.")
        i = i+1

def initif():
    lien = 'seance_54_264.txt'

    chaine = traiterCR(lien)
    
    extractionVote(chaine)

initif()
