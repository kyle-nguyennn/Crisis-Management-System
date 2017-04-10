from django.db.models import Sum

from crisis.models import Case
from crisis import email, sms, twitter_api


class CaseManager:
    @classmethod
    def getActive(cls):
        result = Case.objects.filter(status=0).count() + Case.objects.filter(status=1).count()
        return result

    @classmethod
    def getResolved(cls):
        return Case.objects.filter(status=2).count()

    @classmethod
    def getTotal(cls):
        return Case.objects.all().count()

    @classmethod
    def getCrisisLevel(cls):
        point = 0
        querySet = []
        querySet += Case.objects.filter(status=0)
        querySet += Case.objects.filter(status=1)
        for case in querySet:
            point += case.severity
        if point < 50:
            return 1
        elif point < 90:
            return 2
        else:
            return 3

    @classmethod
    def countCaseGroupByCategory(cls):
        result = {}
        result['fire']=Case.objects.filter(category=0).count()
        result['traffic_accident'] = Case.objects.filter(category=1).count()
        result['terrorist_activity'] = Case.objects.filter(category=2).count()
        result['gas_leak'] = Case.objects.filter(category=3).count()
        return result

    @classmethod
    def countInjuredGroupByCategory(cls):
        result = {}
        result['fire'] = Case.objects.filter(category=0).aggregate(Sum('injured'))["injured__sum"]
        result['traffic_accident'] = Case.objects.filter(category=1).aggregate(Sum('injured'))["injured__sum"]
        result['terrorist_activity'] = Case.objects.filter(category=2).aggregate(Sum('injured'))["injured__sum"]
        result['gas_leak'] = Case.objects.filter(category=3).aggregate(Sum('injured'))["injured__sum"]
        return result

    @classmethod
    def countDeadGroupByCategory(cls):
        result = {}
        result['fire'] = Case.objects.filter(category=0).aggregate(Sum('dead'))["dead__sum"]
        result['traffic_accident'] = Case.objects.filter(category=1).aggregate(Sum('dead'))["dead__sum"]
        result['terrorist_activity'] = Case.objects.filter(category=2).aggregate(Sum('dead'))["dead__sum"]
        result['gas_leak'] = Case.objects.filter(category=3).aggregate(Sum('dead'))["dead__sum"]
        return result

    @classmethod
    def send_email(cls):
        message = '''Dear Sir,

        The crisis state is triggered, please see the following link for the detailed report of the situation. Thank you.

        http://localhost:8000/government_report/

        CMS Team
        '''
        email.send_to_pm(message)

    @classmethod
    def send_email_check(cls):
        level = CaseManager.getCrisisLevel()
        if level == 3:
            CaseManager.send_email()
        else:
            pass

    @classmethod
    def send_sms(cls, phone_num):
        message = "Thank you for using CMS, your reported case has been recorded."
        result = sms.send_sms(phone_num, message)
        if result == False:
            print("Unable to send sms. An error has occurred.")

