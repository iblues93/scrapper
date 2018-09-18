import urllib.request as urlreq
from urllib.error import URLError, HTTPError, ContentTooShortError
from ssl import CertificateError
import re,time
from urllib import robotparser
from urllib.parse import urlparse

class Throttle:
  """
  This class is used to do delaying and keep track of time for domains
  """
  def __init__(self, delay):
    self.delay = delay
    self.domains = {}
  
  def wait(self,url):
    domain = urlparse(url).netloc
    try:
      last_accessed = self.domains.get(domain)
      if self.delay > 0  and last_accessed is not None:
        sleep_sec = self.delay - (time.time() - last_accessed)
        if sleep_sec > 0:
          time.sleep(sleep_sec)
      self.domains[domain] = time.time()
    except Exception:
      self.add(domain)

  def add(self,domain):
    self.domains[domain] = 0

def get_robot_parser(url):
  rp = robotparser.RobotFileParser()
  rp.set_url(url)
  rp.read()
  return rp

def download(url,user_agent = "iphone Xs",retry = 2,charset='utf-8',proxy = None):
  print("Downloading URL : {}".format(url))
  request = urlreq.Request(url)
  request.add_header('User-agent',user_agent)
  
  try:
    if proxy:
      proxy_sup = urlreq.ProxyHandler({'http':proxy})
      opener = urlreq.build_opener(proxy_sup)
      urlreq.install_opener(opener)
    resp = urlreq.urlopen(request)
    cs = resp.headers.get_content_charset()
    if not cs:
      cs = charset
    html = resp.read().decode(cs)
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

def get_links(html):
  # This regex ignores javascript links, emails and anchors within pages
  page_regex = re.compile(r'<a +href ?= ?[\"\']([^#|(?:javascript|mailto)].*?)[\"\']',re.IGNORECASE)
  return page_regex.findall(html)

def parse_url(url):
  url_parser = re.compile(r'(?:https?\:\/\/)?(?:[A-z0-9]+\.)*([A-z0-9]+)\.(?:com|net|org|edu|gov|mil|int|shtml)(?:\.([A-z]{2}))?',re.IGNORECASE)
  domain,country = url_parser.findall(url)[0]
  return domain,country

def link_crawler(start_url, link_regex, robot_url = None,user_agent = "DefinitelyNotABot"):
  if not robot_url:
    robot_url = start_url+"/robots.txt"
  rp = get_robot_parser(robot_url)
  delay = rp.crawl_delay(user_agent)
  timer = Throttle(delay)
  queue = [start_url]
  crawled = set()
  while queue:
    url = queue.pop()
    if url[0] == "/":
      url = start_url + url
    if rp.can_fetch(user_agent,url):
      if url not in crawled:
        timer.wait(url)
        html = download(url,user_agent = user_agent)
        for link in get_links(html):
          if re.match(link_regex,link):
            queue.append(link)
        crawled.add(url)
      #else:
      #  print("Skipped {}".format(url))
    else:
      print('Blocked by Robots.txt : {}'.format(url))

if __name__ == "__main__":
  url = "http://example.webscraping.com"
  url_parser = re.compile(r'(/.+)*/(index|view)/?',re.IGNORECASE)
  link_crawler(url,url_parser,user_agent = "GoodCrawler")
