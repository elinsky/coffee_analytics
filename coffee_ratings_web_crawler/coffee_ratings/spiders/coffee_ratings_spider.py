import scrapy
import os.path


class CoffeeRatingsSpider(scrapy.Spider):
    name = "coffee_ratings_spider"

    def start_requests(self):
        urls = [
            'https://www.coffeereview.com/review/panama-boquete-flor-de-mariposa-geisha-espresso/',
            'https://www.coffeereview.com/review/yemen-al-mashtal-al-burhani/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        def extract_table_field(table_selector, idx: int) -> str:
            return table_selector.xpath('//tr')[idx].xpath('td//text()').extract()[1]

        def save_raw_data(response, page_dirname: str) -> None:
            page = response.url.split("/")[-2]
            filename = f'{page}.html'
            with open(os.path.join(page_dirname, filename), 'wb') as f:
                f.write(response.body)
            self.log(f'Saved file {filename}')

        def parse_review_page(response) -> dict:
            # Parse content
            scraped_data = {}
            scraped_data['roaster'] = response.xpath('//*[@id="genesis-content"]/article/div/div/div[1]/div[2]/p/text()').get()
            scraped_data['bean'] = response.xpath('//*[@id="genesis-content"]/article/div/div/div[1]/div[2]/h1/text()').get()
            scraped_data['rating'] = response.xpath('//*[@id="genesis-content"]/article/div/div/div[1]/div[1]/span/text()').get()

            table = response.xpath('//*[@id="genesis-content"]/article/div/div/div[2]/div[1]/table')
            scraped_data['roaster_location'] = extract_table_field(table, 0)
            scraped_data['coffee_origin'] = extract_table_field(table, 1)
            scraped_data['roast_level'] = extract_table_field(table, 2)
            scraped_data['agtron'] = extract_table_field(table, 3)
            scraped_data['estimated_price'] = extract_table_field(table, 4)
            scraped_data['review_date'] = extract_table_field(table, 5)
            scraped_data['aroma'] = extract_table_field(table, 6)
            scraped_data['acidity_structure'] = extract_table_field(table, 7)
            scraped_data['body'] = extract_table_field(table, 8)
            scraped_data['flavor'] = extract_table_field(table, 9)
            scraped_data['aftertaste'] = extract_table_field(table, 10)

            scraped_data['blind_assessment'] = response.xpath('//*[@id="genesis-content"]/article/div/div/p[1]/text()').get()
            scraped_data['notes'] = response.xpath('//*[@id="genesis-content"]/article/div/div/p[2]/span[1]/text()').get()
            scraped_data['bottom_line'] = response.xpath('//*[@id="genesis-content"]/article/div/div/p[3]/text()').get()

            return scraped_data

        page_dirname = 'raw_coffee_data'

        save_raw_data(response, page_dirname)

        scraped_data = parse_review_page(response)

        yield scraped_data


# TODO - I need to figure out how to crawl the website
# High level plan - start the extract on the latest reviews page: https://www.coffeereview.com/review/
# Then extract that page
# Write a function that tells you if a page is a review page.
# If review page, then extract and terminate
# If not review page, then look for links to reviews (maybe look for all 'read complete reviews' links
# I also need to change pages.
# TODO - I need to handle the case where a review does not have all of the field that I want.