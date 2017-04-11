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

    @classmethod
    def getById(cls,caseId):
        return Case.objects.get(id=caseId)

    @classmethod
    def upDateStatus(cls,userType, caseId, newStatus):
        case = cls.getById(caseId)
        category = case.category
        if (userType, category) in cls.userCaseMatch:
            print('new status is ' + str(newStatus))
            Case.objects.filter(id=caseId).update(status=newStatus)
            return True
        else:
            return False
    @classmethod
    def updateSeverity(cls, userType, caseId, newSeverity):
        case = cls.getById(caseId)
        category = case.category
        if (userType, category) in cls.userCaseMatch:
            case.severity = newSeverity
            case.save(update_fields=['severity'])
            return True
        else:
            return False

    @classmethod
    def updateDead(cls, userType, caseId, dead):
        case = cls.getById(caseId)
        category = case.category
        if (userType, category) in cls.userCaseMatch:
            case.dead = dead
            case.save(update_fields=['dead'])
            return True
        else:
            return False

    @classmethod
    def updateInjured(cls, userType, caseId, newInjured):
        case = cls.getById(caseId)
        category = case.category
        if (userType, category) in cls.userCaseMatch:
            case.injured = newInjured
            case.save(update_fields=['injured'])
            return True
        else:
            return False

    @classmethod
    def getActiveCase(cls):
        result = []
        result+=Case.objects.filter(status=0)
        result += Case.objects.filter(status=1)
        return result
