from crisis.models import Case


class CaseDao:

    def getByUserType(userType):
        #userType matches category: for now its userType-category == 2
        return Case.objects.filter(category=userType-2)