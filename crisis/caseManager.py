from django.db.models import Sum

from crisis.models import Case


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


