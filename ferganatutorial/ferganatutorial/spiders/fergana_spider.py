import scrapy
from ..items import FerganatutorialItem

class FerganatutorialSpider(scrapy.Spider):
    name = 'fergana_2'
    page_number = 2
    name2 = input("Search for: ")
    start_urls = [
        'https://fergana.agency/search/?search=%s' % name2
    ]
    current_page = start_urls[0]

    def parse(self, response):

        all_div_quotes2 = response.css('li.news-list__item')

        for fergana2 in all_div_quotes2:
            content_link = fergana2.css('a::attr(href)').get()
            yield response.follow(content_link, callback=self.parse_content)
            yield response.follow(FerganatutorialSpider.current_page, callback=self.parse_none)

        p_num = int(response.css('div.pagination__container  span::text')[0].extract())

        next_page = FerganatutorialSpider.start_urls[0] + '&n=' + str(FerganatutorialSpider.page_number)
        if FerganatutorialSpider.page_number-1 == p_num:
            yield response.follow(next_page, callback=self.parse)
            FerganatutorialSpider.current_page = next_page
            FerganatutorialSpider.page_number += 1

    def parse_content(self, response):
        items = FerganatutorialItem()
        title = response.css('div.article-top h1::text').extract()
        all_div_content = response.css('div.article-content--narrow')

        content = response.css('p::text').extract()

        for cont in all_div_content:
            content += cont.css('p::text').extract()

        items['title'] = title
        items['content'] = content
        items['author'] = 'Fr'

        yield items

    def parse_none(self):
        {}