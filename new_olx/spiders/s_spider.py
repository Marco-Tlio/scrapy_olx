import scrapy
import json
from new_olx.items import NewOlxItem
def non(res):
    if(res is None):
        return "---"
    else:
        return res
    
class SSpiderSpider(scrapy.Spider):
    name = "s_spider"
    allowed_domains = ["www.olx.com.br"]
    url_raw = "https://www.olx.com.br/imoveis/estado-sc?o="
    start_urls = [url_raw + "1"]
    def parse(self, response):
        
        log_header_up = '================================= Started ======================================'
        log_header_down = '\n ================================= Finished ====================================== \n'
        
        self.log(log_header_up )
        self.log('Page: %s' % response.url)
        self.log(log_header_down)

        
        self.log(log_header_up)
        title_site = response.xpath('//title/text()').get()
        self.log('Title: %s' % title_site)
        self.log(log_header_down)
        
        js = response.css("#__NEXT_DATA__::text") 
        data = json.loads(js.get()) 
        json_inter = data["props"]['pageProps']['ads']
        
        for di in json_inter:
            item = NewOlxItem()
            title1 = None
            title2 = None
            price = None
            if not di.get('advertisingId'):
                aux1 = di.get('properties')
                title1 = next((item.get('value') for item in aux1 if item.get('name') == 'real_estate_type'), None)
                title2 = di.get('title')
                price = di.get('price')
                item['title'] = non(title1) + " | " + non(title2)
                item['price'] = non(price)
                yield item     
            else:
                continue
            
        
        for i in range(2,100):

            urls = self.url_raw + str(i)
            yield scrapy.Request(url=urls, callback=self.parse)
                    