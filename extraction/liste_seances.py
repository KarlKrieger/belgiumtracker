# Documentation
# BeautifulSoup: https://www.crummy.com/software/BeautifulSoup/bs4/doc/
# Afin de récupérer les différentes données dans une page html
# 
# urllib.request: https://docs.python.org/3/library/urllib.request.html
# Pour récupérer le contenu de la page html

from bs4 import BeautifulSoup
import urllib.request

html_doc = urllib.request.urlopen('http://www.lachambre.be/kvvcr/showpage.cfm?section=/cricra&language=fr&cfm=dcricra.cfm?type=plen&cricra=cri&count=all&legislat=54')

soup = BeautifulSoup(html_doc, 'html.parser')
for link in soup.find_all('a', title='Version HTML prête à copier'):
    print(str('www.lachambre.be/') + link.get('href'))
