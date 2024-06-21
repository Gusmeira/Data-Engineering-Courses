# gdp.py -------------------------------------------
import scrapy
from countries_gdp.items import CountryGdpItem
from scrapy.loader import ItemLoader

class GdpSpider(scrapy.Spider):
    name = "gdp"
    allowed_domains = ["wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"]

    def parse(self, response):
        for country in response.css('table.wikitable.sortable tbody tr:not([class])'):
            item = ItemLoader(item=CountryGdpItem(), selector=country)
            item.add_css('country_name', 'td:nth_child(1) a')
            item.add_css('region', 'td:nth_child(2) a')
            item.add_css('gdp', 'td:nth_child(3)')
            item.add_css('year', 'td:nth_child(4)')
            yield item.load_item()

            # item = CountryGdpItem()
            # item['country_name'] = country.css('td:nth_child(1) a::text').get()
            # item['region'] = country.css('td:nth_child(2) a::text').get()
            # item['gdp'] = country.css('td:nth_child(3)::text').get()
            # item['year'] = country.css('td:nth_child(4)::text').get()
            # yield item
            
            # yield {
            #     'country_name':
            #     country.css('td:nth_child(1) a::text').get(),
            #     'region':
            #     country.css('td:nth_child(2) a::text').get(),
            #     'gdp':
            #     country.css('td:nth_child(3)::text').get(),
            #     'year':
            #     country.css('td:nth_child(4)::text').get(),
            # }


            
    


