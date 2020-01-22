from django.db.models import Sum

from crisis.models import *
from crisis import my_email, sms, twitter_api
from crisis.sms import send_sms
from crisis.twitter_api import post_on_twitter


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
        my_email.send_to_pm(message)

    @classmethod
    def send_email_check(cls):
        level = CaseManager.getCrisisLevel()
        if level == 3:
            try:
                CaseManager.send_email()
                print("email sent")
            except:
                print("sent failed")
        else:
            pass

    @classmethod
    def send_sms(cls, phone_num):
        message = "Thank you for using CMS, your reported case has been recorded."
        result = sms.send_sms(phone_num, message)
        if result == False:
            print("Unable to send sms. An error has occurred.")

class NotificationManager:
    @classmethod
    def alertSubscriberNewIncident(cls, caseId):
        CASE_CATEGORY_CHOICE = [(0, 'Fire'), (1, 'Traffic Accient'), (2, 'Terrorist Attack'), (3, 'Gas leak')]
        case = Case.objects.get(id=caseId)
        categoryNo = case.category
        categoryText = "unknown"
        for x in CASE_CATEGORY_CHOICE:
            print("case " + str(x))
            print("x[0] " + str(x[0]))
            print("cat no " + str(categoryNo))
            if int(x[0]) == int(categoryNo):
                categoryText = x[1]
                print(x[1])
                break
        message = "Dear subscriber, a new incident of " + categoryText + " is occuring at " + case.place_name
        post_on_twitter(message)
        subscribers = list(Subscriber.objects.filter(category=categoryNo))
        print(subscribers)
        for subscriber in subscribers:
            print(subscriber.phoneNum)
            print(subscriber.category)
            try:
                phoneText = str(subscriber.phoneNum)
                print("string phone " + phoneText)
                send_sms(phoneText, message)
            except:
                print('error')

    @classmethod
    def alertSubscriberCloseIncident(cls, caseId):
        CASE_CATEGORY_CHOICE = [(0, 'Fire'), (1, 'Traffic Accient'), (2, 'Terrorist Attack'), (3, 'Gas leak')]
        case = Case.objects.get(id=caseId)
        categoryNo = case.category
        caseRegion = case.region
        categoryText = "unknown"
        for x in CASE_CATEGORY_CHOICE:
            print("case " + str(x))
            print("x[0] " + str(x[0]))
            print("cat no " + str(categoryNo))
            if int(x[0]) == int(categoryNo):
                categoryText = x[1]
                print(x[1])
                break
        message = "Dear subscriber, the incident of " + categoryText + " occuring at " + case.place_name + "is resolved." \
                        " The number of dead is " + str(case.dead) + " and the number of injured is "+\
                        str(case.injured) +". The estimated severity of this incident is " + str(case.severity) +\
                        "/5."
        subscribers = list(Subscriber.objects.filter(category=categoryNo).filter(region=caseRegion))
        print(subscribers)
        for subscriber in subscribers:
            print(subscriber.phoneNum)
            print(subscriber.category)
            try:
                phoneText = str(subscriber.phoneNum)
                print("string phone " + phoneText)
                send_sms(phoneText, message)
            except:
                print('error')

    @classmethod
    def alertRANewIncident(cls, case):
        CASE_CATEGORY_CHOICE = [(0, 'Fire'), (1, 'Traffic Accient'), (2, 'Terrorist Attack'), (3, 'Gas leak')]
        agency_contact = ['83826317', '83826317', '83826317', '83826317'] # The number RAs.
        categoryNo = case.category
        categoryText = "unknown"
        for x in CASE_CATEGORY_CHOICE:
            print("case " + str(x))
            print("x[0] " + str(x[0]))
            print("cat no " + str(categoryNo))
            if int(x[0]) == int(categoryNo):
                categoryText = x[1]
                print(x[1])
                break
        message = "Dear agency officer, a new incident of " + categoryText + " is occuring at " + case.place_name + \
                  ". Please login your account in the portal to proceed."

        print('alertRA: invoke send_sms, contact: ' + str(agency_contact[int(categoryNo)]))
        send_sms(str(agency_contact[int(categoryNo)]), message)
