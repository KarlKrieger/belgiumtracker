# -*- coding: utf-8 -*

import urllib
from bs4 import BeautifulSoup

def retirer_html(lien):
    html = urllib.request.urlopen(lien)
    soup = BeautifulSoup(html, 'html.parser')

    # kill all script and style elements
    for script in soup(["script", "style"]):
      script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunks)

url = 'http://www.lachambre.be/doc/PCRI/html/54/ip264x.html'

texte = retirer_html(url)

print (texte)

doc = open('seance_0264.txt', 'w')
doc.close
