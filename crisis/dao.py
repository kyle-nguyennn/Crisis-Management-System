from crisis.models import Case


class CaseDao:
    userCaseMatch = [(0,0), (0,1), (0,2), (0,3),(1,0), (1,1), (2,2), (3,3)]

    @classmethod
    def getByUserType(cls, userType):
        querySet = []
        for x in cls.userCaseMatch:
            if x[0] == userType:
                querySet += Case.objects.filter(category=x[1])
        return querySet

    def getById(self, caseId):
        return Case.objects.get(id=caseId)

    def upDateStatus(self, userType, caseId, newStatus):
        case = self.getById(caseId)
        category = case.category
        if (userType, category) in self.userCaseMatch:
            case.staus = newStatus
            case.save(update_fields='status')
            return True
        else:
            return False

    def updateSeverity(self, userType, caseId, newSeverity):
        case = self.getById(caseId)
        category = case.category
        if (userType, category) in self.userCaseMatch:
            case.severity = newSeverity
            case.save(update_fields='severity')
            return True
        else:
            return False

    def updateCasualties(self, userType, caseId, newCasualties):
        case = self.getById(caseId)
        category = case.category
        if (userType, category) in self.userCaseMatch:
            case.casualties = newCasualties
            case.save(update_fields='casualties')
            return True
        else:
            return False

    def updateInjured(self, userType, caseId, newInjured):
        case = self.getById(caseId)
        category = case.category
        if (userType, category) in self.userCaseMatch:
            case.injured = newInjured
            case.save(update_fields='injured')
            return True
        else:
            return False

    @classmethod
    def getActiveCase(cls):
        result = []
        result+=Case.objects.filter(status=0)
        result += Case.objects.filter(status=1)
        return result
