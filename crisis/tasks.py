from crisis import twitter_api
from crisis.caseManager import CaseManager
from celery import shared_task

@shared_task
def periodic_email_to_pm():
    CaseManager.send_email()

@shared_task
def test_task(s):
    print(s)