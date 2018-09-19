from bs4 import BeautifulSoup
from pprint import pprint
from util.crawler_util import download

def main():
  url = "http://example.webscraping.com/places/default/view/United-Kingdom-239"
  html = download(url)
  soup = BeautifulSoup(html,'html5lib')
  tags = ['capital','country','population','area']
  for label in tags:
    flag_data_row = soup.find('tr',attrs={'id':'places_{}__row'.format(label)})
    print(flag_data_row.text)
  
def negative_case():
  """
  This function only demo the power of BeautifulSoup with html parser for error correction in html code
  """
  cui_html = "<ul class=country><li>Area<li>Population</ul><ul class=state><li>Area<li>Population</ul><ul class=country><li>Area<li>Population</ul>"
  soup=BeautifulSoup(cui_html,'html5lib')
  fixed = soup.prettify()
  first = soup.find('ul', attrs={'class':'country'})
  pprint(first.find_all('li'))
  ul = soup.find_all('ul',attrs={'class':'country'})
  pprint(ul)


if __name__ == "__main__":
  main()
