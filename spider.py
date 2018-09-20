import itertools
import urllib.parse

import scrapy


class WiproDigitalSpider(scrapy.Spider):
    name = "WiproDigitalSpider"
    start_urls = ["http://wiprodigital.com"]
    allowed_domains = ["wiprodigital.com"]

    def parse(self, response):
        next_pages = response.css("a")

        links = next_pages.xpath("@href")

        internal_links = set()
        external_links = set()

        for link in links.extract():
            # Parse the link and reconstruct it without '#fragment'
            scheme, netloc, path, params, query, fragment = (
                urllib.parse.urlparse(link))

            filtered_link = urllib.parse.urlunparse(
                (scheme, netloc, path, params, query, ""))

            if filtered_link == "":
                continue

            internal_domain = any(
                [a.endswith(b) for (a, b) in
                    zip(itertools.cycle([netloc]), self.allowed_domains)])

            if internal_domain or netloc == "":
                internal_links.add(filtered_link)
            else:
                external_links.add(filtered_link)

        imgs = response.css("img").xpath("@src")

        yield {
            "url": response.url,
            "internal_links": list(internal_links),
            "external_links": list(external_links),
            "imgs": list(set(imgs.extract()))
        }

        for next_page in next_pages:
            yield response.follow(next_page, self.parse)
