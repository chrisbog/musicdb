from app import db
import logging

from app.models import Configuration


class AppConfig:


    def __init__(self):
        pass

    def getitem(self, key):

        qry = db.session.query(Configuration).filter(Configuration.key==key)
        results = qry.all()
        if results:
            return results[0].value
        else:
            return None

    def setitem(self, key, value):

        qry = db.session.query(Configuration).filter(Configuration.key==key)
        results = qry.all()
        if results:
            if results[0].value == value:
                print("The value did not change")
            else:
                print ("The value did change")
                results[0].value = value
                db.session.commit()

        else:
            newitem=Configuration()
            newitem.key=key
            newitem.value=value
            db.session.add(newitem)
            db.session.commit()



