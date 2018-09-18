"""
This is for chapter 1, iterating the website through sitemaps. 
"""

import urllib.request as urlreq
from urllib.error import URLError, HTTPError, ContentTooShortError
from ssl import CertificateError
import re

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

def get_sitemap(url,user_agent = "iphone Xs",retry = 2):
  # Getting the robots.txt, and obtaining the sitemap if exist, and return
  # the list of links found in the sitemap
  robots = download(url+"/robots.txt").lower()
  sitemap = re.findall(r'sitemap.*((?:https?|www).+)\\n',robots)
  return re.findall(r'<loc>((?:https?|www).+?)</loc>',download(sitemap[0]))

def crawl_sitemap(url):
  links = get_sitemap(url)
  for link in links:
    content = download(link)

if __name__ == "__main__":
  url = "http://example.webscraping.com"
  crawl_sitemap(url)