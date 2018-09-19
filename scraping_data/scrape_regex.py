
import re
from util.crawler_util import download

def main():
  url = "http://example.webscraping.com/places/default/view/United-Kingdom-239"
  html = download(url)
  
  # Not robust to changes
  # get data
  re_data = re.compile(r'<td class=["\']w2p_fw["\']>(.*?)</td>',re.IGNORECASE)
  data_list = re.findall(re_data,html)

  # get labels
  re_labels = re.compile(r'<tr id="places_(.*?)__row">',re.IGNORECASE)
  label_list = re.findall(re_labels,html)

  # display in nice fashion
  for label, info in zip(label_list, data_list):
    print("{0} : {1}".format(label, info))



if __name__ == "__main__":
  main()
