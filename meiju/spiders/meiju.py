# -*- coding: utf-8 -*-
import scrapy
from meiju.items import MovieItem
from scrapy import Request
class MeijuSpider(scrapy.Spider):
    name = "meiju"
    #allowed_domains = ["meijutt.com"]
    start_urls = ['http://www.meijutt.com/new100.html']

    def parse(self, response):
        movies = response.xpath('//ul[@class="top-list  fn-clear"]/li')
        for each_movie in movies:
            item = MovieItem()
            name = each_movie.xpath('./h5/a/@title').extract()[0].encode(encoding='UTF-8')
	    url = each_movie.xpath('./h5/a/@href').extract()[0]
	    imgurl = 'http://www.meijutt.com' + url
	    #print(imgurl)
	    item['name'] = name

            #yield item
	    yield Request(url=imgurl, callback=self.parse_image, meta={'item': item})

    def parse_image(self, response):
	    item = response.meta['item']
        item['url'] = response.xpath('//div[@class="o_big_img_bg_b"]/img/@src').get().encode(encoding='UTF-8')
        yield item
        next_image_url = response.xpath('//a[@id="pageNext"]/@href').extract_first()
        print("~" * 30)
        print(next_image_url)
        if next_image_url:
            yield response.follow(next_image_url, self.parse_image)
