import re
class DataValidator:

    @classmethod
    def isNotNull(Pradeep, val):
        if(val == None or val == ""):
            return False
        else:
            return True

    @classmethod
    def isNull(Pradeep,val):
        if(val == None or val == ""):
            return True
        else:
            return False

    def isInt(self, val):
        if(val == 0):
            return False
        else:
            return True

    def ismobilecheck(self,val):
        if re.match("^[6-9]\d{9}$",val):
            return False
        else:
            return True
