import urllib.request as urlreq
from urllib.error import URLError, HTTPError, ContentTooShortError
from ssl import CertificateError
import re
from urllib.parse import urljoin

def download(url,user_agent = "iphone Xs",retry = 2):
  print("Downloading URL : {}".format(url))
  request = urlreq.Request(url)
  request.add_header('User-agent',user_agent)
  
  try:
    html = urlreq.urlopen(request).read()
  except (URLError, HTTPError, ContentTooShortError,CertificateError) as e:
    if isinstance(e,CertificateError):
      err_msg = "SSL Certificate Error"
    else:
      err_msg = e.reason
    print("Error getting {0} : {1}".format(url,err_msg))
    if retry > 0 and hasattr(e,'code') and 500 <= e.code < 600:
      html = download(url,user_agent,retry-1)
    else:
      html = None
  return str(html)

def link_crawler(start_url, link_regex):
  queue = [start_url]
  crawled = set()
  while queue:
    url = queue.pop()
    if url[0] == "/":
      url = start_url + url
    if url not in crawled:
      html = download(url)
      if html is None:
        continue
      for link in get_links(html):
        if re.match(link_regex,link):
          queue.append(link)
      crawled.add(url)

def get_links(html):
  # This regex ignores javascript links, emails and anchors within pages
  page_regex = re.compile(r'<a +href ?= ?[\"\']([^#|(?:javascript|mailto)].*?)[\"\']',re.IGNORECASE)
  return page_regex.findall(html)

def parse_url(url):
  url_parser = re.compile(r'(?:https?\:\/\/)?(?:[A-z0-9]+\.)*([A-z0-9]+)\.(?:com|net|org|edu|gov|mil|int)(?:\.([A-z]{2}))?',re.IGNORECASE)
  domain,country = url_parser.findall(url)[0]
  print(domain,country)

if __name__ == "__main__":
  url = "https://serebii.net.sg"
  parse_url(url)
  #link_crawler(url,re.compile(r'.',re.IGNORECASE))
