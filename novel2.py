import requests
import re
from lxml import etree
import threading
import pymongo


class Novel_Donwload(object):

  def __init__(self, target, compile, proxies):
    '''
      获取小说网站url


    '''
    self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)
    self.db = self.client['novel']
    self.collection = self.db['book']


    self.website_url = target
    self.sess = requests.session()
    self.sess.headers = {
      'Referer': target,
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
    }
    self.sess.proxies = proxies
    self.compile = compile

  def get_book_url(self):
      r = self.sess.get(self.website_url)
      books_url = re.findall(self.compile, r.text, re.S)

      return books_url
  
  def send_response(self, url_list):
    for url in url_list:
      full_url = 'https://www.biqukan.com' + url
      r = self.sess.get(url=full_url, timeout=5)
      r.encoding = 'gbk'
      self.get_response(r.text)
      break


  def get_response(self, html):
      book_info = {}
      book_info['name'] = re.findall('<h2>(.*?)</h2>',html, re.S )[0]
      book_info['author'] = re.findall('<span>作者：(.*?)</span>',html, re.S )[0]
      book_info['category'] = re.findall('<span>分类：(.*?)</span>',html, re.S )[0]
      book_info['status'] = re.findall('<span>状态：(.*?)</span>',html, re.S )[0]
      book_info['count'] = re.findall('<span>字数：(.*?)</span>',html, re.S )[0]
      book_info['update'] = re.findall('<span class="last">更新时间：(.*?)</span>',html, re.S )[0]
      book_info['profile'] = re.findall('<span>简介：</span>(.*?)<br/>',html, re.S )[0]
      chapter_list  = re.findall('<dd><a href ="(/\d+_\d+/\d+.html)">(.*?)</a></dd>', html, re.S)
      pool = []
      for item  in chapter_list:
        try:
          full_url = 'https://www.biqukan.com' + item[0]
          r = self.sess.get(url=full_url, timeout=5)
          r.encoding ='gbk'
          html = etree.HTML(r.text)
          content = html.xpath('//div[@id="content"]/text()')[:-2]
          print('\n'.join(content).replace('\u3000',''))
          book_info[item[1]] = '\n'.join(content).replace('\u3000','')
        except Exception as e:
          print(e)
      self.collection.save(book_info)
          

if __name__ == "__main__":

    # 代理服务器
  proxyHost = "http-dyn.abuyun.com"
  proxyPort = "9020"

  # 代理隧道验证信息
  proxyUser = "H7VEN14J241B327D"
  proxyPass = "E64E9433EA553CE2"

  proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host" : proxyHost,
    "port" : proxyPort,
    "user" : proxyUser,
    "pass" : proxyPass,
  }

  proxies = {
      "http"  : proxyMeta,
      "https" : proxyMeta,
  }
  url = 'https://www.biqukan.com/'
  compile = r'href="(/\d+_\d+/)"'
  novel = Novel_Donwload(target=url,compile=compile, proxies=proxies)
  urls =  novel.get_book_url()
  novel.send_response(url_list=urls)
  


