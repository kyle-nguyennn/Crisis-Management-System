from django_cron import CronJobBase, Schedule
from crisis import caseManager


class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 30 # every 30 minutes

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'crisis.scheduled_email'    # a unique code

    def do(self):
        caseManager.CaseManager.send_email()