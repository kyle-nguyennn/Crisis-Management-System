from crisis.models import Case


class CaseDao:
    def getByUserType(self, userType):
        #userType matches category: for now its userType-category == 2
        return Case.objects.filter(category=userType-2)

    def getById(self, caseId):
        return Case.objects.get(id=caseId)

    def upDateStatus(self, userType, caseId, newStatus):
        case = self.getById(caseId)
        if userType - case.category != 2:
            return False
        else:
            case.staus = newStatus
            case.save(update_fields='status')
            return True