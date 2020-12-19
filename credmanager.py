import pymongo
import secrets
import time
from exceptions import InvalidToken
def dtconvert(s):
    if s.isnumeric():
        s=s+"d"
    d={"s":1,"m":60,"h":3600,"d":86400,"w":604800,"M":2628000,"y":31536000}
    multiplier=d[s[-1]]
    num=int(s[:-1])
    return multiplier*num


class SessionManager:
    def __init__(self,name,client=None):
        if client is None:
            client=pymongo.MongoClient()
        self.client=client
        self.db=self.client["CredManager"]
        self.col=self.db[name]
    def insertcred(self,expir="1w",token=None,dictofargs={}):
        if token is None:
            token=secrets.token_hex()
            while list(self.col.find({"cred":token}))!=[]:
                token=secrets.token_hex()
        expir=time.time()+dtconvert(expir)
        self.col.insert_one({"expir":expir,"cred":token}|dictofargs)
        return {"expir":expir,"cred":token}|dictofargs
    def expirecred(self,token):
        a=list(self.col.find({"cred":token}))
        if a==[]: raise InvalidToken("Token does not exist")
        self.col.delete_one({"cred":token})
    def checkcred(self,token,delete_if_expired=True):
        a=self.col.find({"cred":token})
        print(len(list(a)))
        if len(list(a))==0:
            return (False,None)
        print(list(a))
        if a["expir"]<=time.time():
            self.expirecred(token)
            return (False,a[0])
        return (True,a[0])
    def clean(self):
        # Do not do this often in prod databases, this will cause undue stress on
        # the database
        for element in self.client.find({}):
            if element["expir"]<=time.time():
                self.expirecred(element["cred"])
    def getcred(self,token):
        a=self.col.find({"cred":token})
        if list(a)==[]: raise InvalidToken("Token does not exist")
        return a[0]
    def getdocs(self,filter={}):
        return list(self.col.find(filter))
