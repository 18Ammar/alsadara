
class MainController():
    def __init__(self,entity:object):
        self.entity = entity
    def create(self,**kwargs):
        record = self.entity(**kwargs)
        record.save()
        return record

    def get_one(self,**kwargs):
        record = self.entity.query.filter_by(**kwargs).first()
        if not record:
            return "the requested {} with the given information {} not found".format(self.entity.__tablename__,",".join(["{}={}".format(k,v) for k,v in kwargs.items()]))
        return record

    