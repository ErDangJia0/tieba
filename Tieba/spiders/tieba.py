import scrapy
from Tieba.items import TiebaItem
from bs4 import BeautifulSoup
import re


class TiebaSpider(scrapy.Spider):
    tName = input("请输入你要爬取的贴吧：")
    page = int(input("请输入要爬取的页数："))
    name = 'tieba'
    pn = 0
    url = 'http://tieba.baidu.com/f?kw=' + tName + '&pn='
    start_urls = [url + str(pn)]
    baseurl = 'http://tieba.baidu.com'

    def parse(self, response):
        for num in response.xpath('//div[@class="t_con cleafix"]/div/div/div/a/@href').extract():
            # 交给调度器，指定解析函数
            yield scrapy.Request(self.baseurl + num, callback=self.getHtml)
        if self.pn < (self.page - 1) * 50:
            self.pn += 50
        yield scrapy.Request(self.url + str(self.pn), callback=self.parse)

    def getHtml(self, response):
        soup = BeautifulSoup(response.body, 'html.parser')
        infoList = soup.find_all("img", attrs={"class": "BDE_Image"})
        for l in infoList:
            item = TiebaItem()
            item['url'] = l['src']
            item['tName'] = self.tName
            print("-------------图片下载中-------------")
            yield item
