from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution

from ..main.api import crawler

import sys

# This is the function you want to schedule - add as many as you want and then register them in the start() function below
def crawl():
    print("Crawling the news...")
    #crawler.crawl()


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(crawl, "interval", hours = 8, name = "crawl_news", jobstore = "default", id = "news_crawler")
    register_events(scheduler)
    scheduler.start()
    print("Scheduler started...", file = sys.stdout)