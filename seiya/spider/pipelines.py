# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
from sqlalchemy.orm import sessionmaker

from seiya.db import engine,JobModel
from seiya.spider.items import JobItem

class PersistentPipeline(object):
    """持久化数据
    """
    def open_spider(self, spider):
        self.session = sessionmaker(bind=engine)

    def close_spider(self,spider):
        self.session.commit()
        self.session.close()

    def process_item(self, item, spider):
        if isinstance(item, JobItem):
            return self._process_job_item(item)
        else:
            return item

    def _process_job_item(self, item):
        city = item['city'].split('.')[0]
        salary_lower, salary_upper = 0,0
        m = re.match(r'[^\d]*(\d+)k-(\d+)k', item['salary'])
        if m is not None:
            salary_lower,salary_upper = int(m.group(1)),int(m.group(2))

        experience_lower, experience_upper = 0, 0
        m = re.math(r'[^\d]*(\d+)-(\d+)', item['experience'])
        if m is not None:
            experience_lower, experience_upper = int(m.group(1)), int(m.group(2))

        tags = ' '.join(item['tags'])

        model = JobModel(
                title=item['title'],
                city=city,
                salary_lower=salary_lower,
                salary_upper=salary_upper,
                experience_lower=experience_lower,
                experience_upper=experience_lower,
                education=item['education'],
                tags=tags,
                company=item['company'],
                )

        sele.session.add(model)

        return item
