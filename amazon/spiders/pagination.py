import scrapy


class PaginationSpider(scrapy.Spider):
    name = 'pagination'

    allowed_domains = ['amazon.com']
    def start_requests(self):
        yield scrapy.Request(url="https://www.amazon.com/s?k=laptop")

    def parse(self, response):
        total_pages = response.xpath("//span[@class='s-pagination-item s-pagination-disabled']/text()").get()        
        print(total_pages)        
        current_page =response.css(".s-pagination-item.s-pagination-selected::text").get()      
        print(response.url)
        if total_pages and current_page:
            if int(current_page) ==1:
                for i in range(2, int(total_pages)+1):
                    yield response.follow(url=f'https://www.amazon.com/s?k=laptop&page={i}')
                    
        for result in response.xpath('//*[@data-component-type="s-search-result"]'):
            # name_xpath = './/*[@class="a-size-medium a-color-base a-text-normal"]/text()'
            product_title = result.css('span.a-size-medium::text').get()
            price_dollar = result.xpath('.//*[@class="a-price-whole"]/text()').get()
            price_cents = result.xpath('.//*[@class="a-price-fraction"]/text()').get()

            item = dict()
            item['Product'] = product_title
            item['Price_Dollars'] = price_dollar
            item['Price_cents'] = price_cents

            yield item