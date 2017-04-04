from crisis.models import Case


class CaseDao:

    def getByUserType(userType):
        return Case.objects.all()