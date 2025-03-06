from shared.database import db
from shared.database import generate_uuid
from sqlalchemy.dialects.postgresql import ARRAY, JSON

class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.String(255),primary_key=True,unique=True,nullable=False,default=generate_uuid)
    created_at = db.Column(db.DateTime,nullable=False,default=db.func.now())
    updated_at = db.Column(db.DateTime,nullable=False,default=db.func.now(),onupdate=db.func.now())
    deleted = db.Column(db.Boolean,default=False)
    documents = db.Column(ARRAY(db.String(255)))

    def save(self):
        try:
            result = db.session.add(self)
            db.session.commit()
            return result
        except Exception as e:
            db.session.rollback()
            return str(e)
        
    def delete(self,*args,**kwargs):
        self.deleted = True
        db.session.commit()
    

