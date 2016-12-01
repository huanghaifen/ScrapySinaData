#coding:utf-8
import cookielib
import logging
import urllib2

import requests
from bs4 import BeautifulSoup

from db.SQLiteHelper import SqliteHelper

logger = logging.getLogger('spider')
__author__ = 'QC'
sinaurl='http://news.sina.com.cn/'
sqlHelper = SqliteHelper()
class GetSinaData(object):
    def __init__(self):
        self.cj = cookielib.LWPCookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj))
    def run(self):
            logger.info("Start to run spider")
            #获取新浪要闻
            sinas = GetSinaData().getdata()
            sqlHelper.batch_insert(sqlHelper.tableName, sinas)
    def getdata(self):
        sinas = []
        req = urllib2.Request(sinaurl)
        response = urllib2.urlopen(req)
        self.operate = self.opener.open(req)
        thePage = response.read()
        soup = BeautifulSoup(thePage, 'html.parser')
        html=soup.find_all(attrs={"data-client": "headline"})
        for news in html:
            if len(news.select('a'))>0:
                h2=news.select('a')[0].text
                a=news.select('a')[0]['href']
                ss = [h2,a]
                sinas.append(ss)
        return sinas
        # #解析内容
        # print html
    def getdata2(self):
        sinas = []
        sinaurl='http://news.sina.com.cn/china/'
        html=requests.get(sinaurl)
        html.encoding = 'utf-8'
        html_sample =html.text
        soup = BeautifulSoup(html_sample, 'html.parser')
        for news in soup.select('.news-item'):
            if len(news.select('h2'))>0:
                h2=news.select('h2')[0].text
                a=news.select('a')[0]['href']
                ss = [h2,a]
                sinas.append(ss)
        return sinas



if __name__=="__main__":
    getsinadata=GetSinaData()
    getsinadata.run()
