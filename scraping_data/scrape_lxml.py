from lxml.html import fromstring, tostring
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

def main2():
  html = "<ul class=country><li>Area<li>Population</ul><ul class=state><li>Area<li>Population</ul><ul class=country><li>Area<li>Population</ul>"
  url = "http://example.webscraping.com/places/default/view/United-Kingdom-239"
  html = download(url)
  tree = fromstring(html)
  fixed = tostring(tree,pretty_print = True)
  labels = tree.cssselect('tr > td.w2p_fl')
  datas = tree.cssselect('tr > td.w2p_fw')
  for label,data in zip(labels,datas):
    print("{0}{1}".format(label.text_content(),data.text_content()))

def main3():
  # use xpath
  html = "<ul class=country><li>Area<li>Population</ul><ul class=state><li>Area<li>Population</ul><ul class=country><li>Area<li>Population</ul>"
  url = "http://example.webscraping.com/places/default/view/United-Kingdom-239"
  html = download(url)
  tree = fromstring(html)
  labels = tree.xpath('//tr/td[@class="w2p_fl"]')
  datas = tree.xpath('//tr/td[@class="w2p_fw"]')
  for label, data in zip(labels,datas):
    print("{0}{1}".format(label.text_content(),data.text_content()))

if __name__ == "__main__":
  #main()
  #main2()
  main3()
