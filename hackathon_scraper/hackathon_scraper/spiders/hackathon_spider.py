import scrapy


class HackathonSpider(scrapy.Spider):
    name = "hackathon_spider"
    start_urls = [
        'https://hackathon-planning-kit.org/',  # Start with the main page
    ]

    def parse(self, response):
        # Extract content and references
        page_content = {
            "url": response.url,
            "title": response.xpath('//title/text()').get(),
            "headings": response.xpath('//h1/text() | //h2/text() | //h3/text()').getall(),
            "paragraphs": response.xpath('//p/text()').getall(),
            "links": response.xpath('//a/@href').getall(),
        }

        # Save extracted content
        yield page_content

        # Follow links to other pages within the website
        for link in response.xpath('//a/@href').getall():
            # Ensure links are within the website domain
            if link.startswith('/') or 'hackathon-planning-kit.org' in link:
                yield response.follow(link, callback=self.parse)

