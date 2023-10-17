import scrapy
import re
import csv
from scrapy.crawler import CrawlerProcess

class MySpider(scrapy.Spider):
    name = 'my_spider'
    start_urls = ['https://nodesk.co/remote-jobs/']

    def parse(self, response):
        #extract the url for each job category
        category_urls = response.css('div.cf.center-l.mw14-l.search-ui div a::attr(href)').getall()[9:-5]

        # Visit each category page and call the parse_category method
        for url in category_urls:
            yield scrapy.Request(url, callback=self.parse_category)

    def parse_category(self, response):
        # Extract the URLs for each job post on the category page
        job_post_urls = response.css('h2.f8.f7-ns.fw6.lh-title.mb1.mt0 a::attr(href)').getall()

        # Visit each job post URL and call the parse_job_post method
        for url in job_post_urls:
            yield scrapy.Request(url, callback=self.parse_job_post, cb_kwargs=dict(url=url))

    def parse_job_post(self, response, url):
        # Extract the information you need from the job post page
        # extract job details
            # extract company name
            company_name = response.css('div.dtc-ns.pl3-s.pl3-ns.v-top h3 * ::text').getall()
            # extract job title
            job_title = response.css('div.dtc-ns.pl3-s.pl3-ns.v-top h2 * ::text').getall()
            # extract country
            country = response.css('div.inline-flex.items-center.flex-wrap.flex-nowrap-l.mb1-l h5 * ::text').getall()
            # extract job type
            job_type = response.css('div.flex.inline-flex-s.inline-flex-ns.items-center.mr3-s.mr3-m.mr6-l.mv1.mv0-l.nowrap h4 * ::text').getall()
            # extract industries
            industries = response.css('div.inline-flex.items-center.mr3.mr6-l.mv1.mv0-l h4 * ::text').getall()
            # extract salary
            salary_els = response.css('div.inline-flex.items-center.mv1.mv0-l h4.f9.fw4.grey-700.mv0::text, div.inline-flex.items-center.mv1.mv0-l h4.f9.fw4.grey-900.mv0::text')
            if salary_els:
                salary = salary_els[0].get()
            else:
                salary = '0'
            # extract skills
            skills = response.css('div.mt2.mt3-s.mt3-l li * ::text').getall()
            
            # Yield a dictionary with the extracted information
            scraped_info =  {
                'url': url,
                'company': company_name,
                'job_title': job_title,
                'job_type': job_type,
                'country': country,
                'industry': industries,
                'salary': salary,
                'skills': skills
            }
            yield scraped_info

process = CrawlerProcess(settings={
    'FEED_FORMAT': 'csv',
    'FEED_URI': 'output.csv',
    'LOG_ENABLED': False
})

process.crawl(MySpider)
process.start()
