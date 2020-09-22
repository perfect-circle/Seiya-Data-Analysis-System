import random
import scrapy
from seiya.spider.items import JobItem

class JobsSpider(scrapy.Spider):
    """拉钩网职位数据爬虫
    """
    name = 'jobs'
    allowed_domains = ['lagou.com']
    headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:80.0) Gecko/20100101 Firefox/80.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Referer": "https://www.lagou.com/zhaopin/",
            "Cookie": "user_trace_token=20200917110419-2026808f-2268-4c19-bd43-248d8223522c; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221749a051f148-09859b401ebe298-445c6e-1296000-1749a051f151ae%22%2C%22%24device_id%22%3A%221749a051f148-09859b401ebe298-445c6e-1296000-1749a051f151ae%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1600311861; LGUID=20200917110423-0e5826f1-fd0e-4dc9-a0b9-8e3bf2baf64c; _ga=GA1.2.224202090.1600311863; JSESSIONID=ABAAAECAAEBABII0FD87264FA86E52B1FC61E4C346C4596; WEBTJ-ID=20200917110420-1749a051de2618-0671280d3cfef18-445c6e-1296000-1749a051de34a1; X_HTTP_TOKEN=ae7ad0d92a82db9658757700612fa9c886ae6a8843; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1600775786; LGRID=20200922195627-b7f9f821-70fb-4f4e-aaf6-a2b9214e8cd3; SEARCH_ID=8a2c69785b414352a803c12ab4a0bc14; LGSID=20200922194116-224d4758-9ce0-4a7d-ab1c-94e5da8ae2a1; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fzhaopin%2F; _gid=GA1.2.658566788.1600774876; _gat=1"
            }

    def start_requests(self):
        urls = [
                'https://www.lagou.com/zhaopin/{}/'.format(i) for i in range(1,31)]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse,headers=self.headers)

    def parse(self, response):
        for job in response.xpath('//li[contains(@class,"con_list_item")]'):
            item = JobItem (
                    title = job.xpath('//div[@class="p_top"]/h3/text()')\
                            .extract_first().strip(),
                    city = job.xpath('//span[@class="add"]/em/text()')\
                            .extract_first.strip(),
                    salary = job.xpath('//div[@class="li_b_l"]/span/text()')\
                            .extract_first.strip(),
                    experience = job.xpath('//div[@class="position"]\
                            /div[@class="p_bot"]/div[@class="li_b_l"]/text()')\
                            .re(r'(.+)\s*'),
                    education = job.xpath('//div[@class="position"]\
                            /div[@class="p_bot"]/div[@class="li_b_l"]/text()')\
                            .re(r'.+\s*/\s*(.+)'),
                    tags = job.xpath('//div[@class="list_item_bot"]/span/text()\
                            ').extract(),
                    company = job.xpath('//div[@class="company"]/div[@class=\
                            "company_name"]/a/text()').extract_first.strip()
                    )
            yield item
