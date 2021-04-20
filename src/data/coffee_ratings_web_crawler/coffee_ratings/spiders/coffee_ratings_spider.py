import scrapy
import os.path


class CoffeeRatingsSpider(scrapy.Spider):
    name = "coffee_ratings_spider"

    def start_requests(self):
        urls = [
            # 'https://www.coffeereview.com/review/nayamasasa-democratic-republic-of-the-congo/'
            'https://www.coffeereview.com/review'
            # 'https://www.coffeereview.com/review/foundry-blend/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        def save_raw_data(response, page_dirname: str) -> None:
            page = response.url.split("/")[-2]
            filename = f'{page}.html'
            with open(os.path.join(page_dirname, filename), 'wb') as f:
                f.write(response.body)
            self.log(f'Saved file {filename}')

        def extract_if_exists(xpath: str):
            return response.xpath(xpath).get() if response.xpath(xpath) else 'NA'

        def parse_review_page(response) -> dict:
            # Parse content
            scraped_data = {}

            scraped_data['roaster'] = extract_if_exists('//*[@class=\"review-roaster\"]//text()')
            scraped_data['bean'] = extract_if_exists('//*[@class=\"review-title\"]//text()')
            scraped_data['rating'] = extract_if_exists('//*[@class=\"review-template-rating\"]//text()')

            scraped_data['roaster_location'] = extract_if_exists('//*[text()[contains(.,"Roaster Location")]]/following-sibling::td//text()')
            scraped_data['coffee_origin'] = extract_if_exists('//*[text()[contains(.,"Coffee Origin")]]/following-sibling::td//text()')
            scraped_data['roast_level'] = extract_if_exists('//*[text()[contains(.,"Roast Level")]]/following-sibling::td//text()')
            scraped_data['agtron'] = extract_if_exists('//*[text()[contains(.,"Agtron")]]/following-sibling::td//text()')
            scraped_data['estimated_price'] = extract_if_exists('//*[text()[contains(.,"Est. Price")]]/following-sibling::td//text()')
            scraped_data['review_date'] = extract_if_exists('//*[text()[contains(.,"Review Date")]]/following-sibling::td//text()')
            scraped_data['aroma'] = extract_if_exists('//*[text()[contains(.,"Aroma")]]/following-sibling::td//text()')
            scraped_data['acidity_structure'] = extract_if_exists('//*[text()[contains(.,"Acidity") and contains(.,"Structure")]]/following-sibling::td//text()')

            scraped_data['body'] = extract_if_exists('//*[text()[contains(.,"Body")]]/following-sibling::td//text()')
            scraped_data['flavor'] = extract_if_exists('//*[text()[contains(.,"Flavor")]]/following-sibling::td//text()')
            scraped_data['aftertaste'] = extract_if_exists('//*[text()[contains(.,"Aftertaste")]]/following-sibling::td//text()')
            scraped_data['with_milk'] = extract_if_exists('//*[text()[contains(.,"With Milk")]]/following-sibling::td//text()')


            scraped_data['blind_assessment'] = extract_if_exists('//*[text()[contains(.,"Blind Assessment")]]/following-sibling::text()')
            scraped_data['notes'] = extract_if_exists('//*[text()[contains(.,"Notes")]]/following-sibling::text()')
            scraped_data['bottom_line'] = extract_if_exists('//*[text()[contains(.,"The Bottom Line")]]/following-sibling::text()')
            scraped_data['who_should_drink_it'] = extract_if_exists('//*[text()[contains(.,"Who Should Drink It")]]/following-sibling::text()')

            return scraped_data

        def extract_coffee_review_urls(response) -> list:
            """Given a url that has a list of reviews (e.g. the latest reviews webpage), crawl the page, parse urls to
            other review pages, and return the list of those urls.
            """
            return response.xpath('//a[@title="Read Complete Review"]/@href').getall()

        def extract_next_page_url(response) -> list:
            """Given a url that has a list of reviews, crawl the page, return the url to teh next page of reviews."""
            if response.xpath('//li[@class="pagination-next"]//a/@href'):
                return [response.xpath('//li[@class="pagination-next"]//a/@href').get()]
            else:
                return []

        def calculate_raw_data_dir():
            dir = os.path.dirname(__file__)
            dir = os.path.dirname(dir)
            dir = os.path.dirname(dir)
            dir = os.path.dirname(dir)
            dir = os.path.dirname(dir)
            dir = os.path.dirname(dir)
            dir += '/data/raw/'
            return dir

        page_dirname = calculate_raw_data_dir()
        self.log("parsing page: " + response.url)

        urls_to_crawl = extract_coffee_review_urls(response)
        urls_to_crawl += extract_next_page_url(response)

        self.log("URLs scraped to review still " + str(urls_to_crawl))
        if urls_to_crawl:
            for url in urls_to_crawl:
                yield scrapy.Request(url=url, callback=self.parse)
        else:
            save_raw_data(response, page_dirname)
            self.log("parse a single review for: " + str(response.url))
            scraped_data = parse_review_page(response)
            yield scraped_data

# TODO - add the URL to the parsed JSON document
# TODO - add a try catch to the parse, log when you get an error parsing.
# TODO - if I've already downloaded and parsed the page, then don't download again.