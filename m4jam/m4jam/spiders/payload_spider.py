import scrapy
from m4jam.items import M4JamItem
from urlparse import urlparse


class PayloadSpider(scrapy.Spider):
    name = "m4jam_payload"
    allowed_domains = ["app.m4jam.com"]
    base = "https://app.m4jam.com/"
    start_urls = [
        base + "app/dashboard/providers/1666/campaigns/2298/payloads/?reset",
    ]

    def __init__(self, username='', password=''):
        self.username = username
        self.password = password

    def parse(self, response):
        return [scrapy.http.FormRequest.from_response(response,
                    formdata={'username': self.username, 'password': self.password},
                    callback=self.after_login)]

    def after_login(self, response):
        row_xpath = '//a[contains(@href, "/jobber-data/payloads/")]/../..'
        for row in response.xpath(row_xpath):
            item = M4JamItem()

            id_xpath = 'td[1]/a/text()'
            id = row.xpath(id_xpath)[0].extract()
            item['payload_id'] = id

            job_name_xpath = 'td[2]/div/text()'
            job_name = row.xpath(job_name_xpath)[0].extract().strip()
            item['job_name'] = job_name

            image_xpath = 'td[7]/table/tbody/tr/td[3]/div/img/@src'
            image_path = row.xpath(image_xpath)[0].extract()

            item['file_urls'] = [self.base + image_path]
            yield(item)

        next_link_xpath = '//li[@class="next"]/a/@href'
        next_link = response.xpath(next_link_xpath)[0].extract()

        url = urlparse(response.url)
        next_abs = "%s://%s" % (url.scheme, url.netloc + url.path + next_link)
        print
        print(next_abs)
        print
        yield scrapy.Request(next_abs, callback=self.after_login)
