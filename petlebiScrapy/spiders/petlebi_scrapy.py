import scrapy
from inline_requests import inline_requests
import json
from scrapy_splash import SplashRequest

class PetlebiScrapySpider(scrapy.Spider):
    name = "petlebi_scrapy"
    
    def __init__(self):
        self.allowed_domains = ["www.petlebi.com"]
        self.start_urls = ["https://www.petlebi.com"]
  
        self.script = '''
            function main(splash, args)
            url = args.url
            assert(splash:go(url))
            assert(splash:wait(10))
            return splash:html()
            end
            '''
    @inline_requests
    def parse(self, response):
        cards = response.xpath("//ul[@class='mobile-sub wsmenu-list']")
        links = []
        for i in range(3):
            a_tags = cards.xpath(f".//li[{i+1}]/div/div/ul/li[1]/div/div/div/div[@class='col-lg-12 col-md-12 clearfix']//a")
            hrefs = [a.xpath("@href").get() for a in a_tags]
            links += hrefs
        
        ul = response.xpath("(//ul[@class='clearfix'])[1]")
        for li in ul.xpath(".//li"):
            a_tags = li.xpath(".//a")
            hrefs = [a.xpath("@href").get() for a in a_tags]
            links += hrefs
        
        for link in links:
            yield scrapy.Request(url=link, callback=self.parse_link)
            
        next_page = response.xpath("//a[@rel='next']/@href").get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
            
    def parse_link(self, response):
        divs = response.xpath("//div[@class='card-body pb-0 pt-2 pl-3 pr-3']")

        for div in divs:
            a_tag = div.xpath(".//a")
            product_url = a_tag.xpath("@href").get()
            
            data_gtm = a_tag.xpath("@data-gtm-product").get()
            if data_gtm:
                data_gtm = json.loads(data_gtm)
                product_name = data_gtm["name"]
                product_id = data_gtm["id"]
                product_price = data_gtm["price"]
                product_category = data_gtm["category"]
                product_brand = data_gtm["brand"]
            
                data = {
                    'product_name': product_name,
                    'product_id': product_id,
                    'product_price': product_price,
                    'product_category': product_category,
                    'product_brand': product_brand,
                    'product_barcode' : None,
                    'product_description' : None,
                    'product_images' : None,
                    'product_stock' : None,
                    'product_sku' : None
                    
                }
                
                print("product_url: ", product_url)
                yield SplashRequest(url=product_url, callback=self.parse_product_link, endpoint="execute", args={"lua_source": self.script}, meta={'data': data})
            


        
    def parse_product_link(self,response):
        data = response.meta['data']
        product_barcode = response.xpath("//div[@class='row mb-2']/div[2]/text()").get()
        product_description = response.xpath('//span[@id="productDescription"]')
        product_description = ''.join(product_description.xpath('.//text()').extract())
        images_src = response.xpath("//div[@class='mcs-items-container']//a/@href").extract()
        product_stock = len(response.xpath("//select[@id='quantity']/option"))
        
        
        data['product_barcode'] = product_barcode
        data['product_description'] = product_description
        data['product_images'] = images_src
        data['product_stock'] = product_stock
        
        print("---------------------------------------------------------------")
        print("data: ", data)
        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
        
        yield data
        
                
    