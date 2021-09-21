from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder


class BaseCrudProvider:
    def __init__(self, model):
        self.model = model

    def get_all(self, db, order_by_field='status'):
        if not order_by_field or not hasattr(self.model, order_by_field):
            return db.query(self.model).all()
        return db.query(self.model).order_by(getattr(self.model, order_by_field).desc()).all()

    def get_by_id(self, db, obj_id):
        try:
            return db.query(self.model).filter(self.model.id == obj_id).one()
        except Exception as e:
            raise HTTPException(
                status_code=404,
                detail="Object not found",
            )

    def delete_by_id(self, db, obj_id):
        obj = self.get_by_id(db, obj_id)
        db.delete(obj)
        db.commit()
        return obj

    def create(self, db, obj_data):
        try:
            encoded_obj_data = jsonable_encoder(obj_data)
            db_obj = self.model(**encoded_obj_data)
            db.add(db_obj)
            try:
                db.commit()
            except Exception as e:
                db.rollback()
            db.refresh(db_obj)
            return db_obj
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=str(e),
            )

    def update(self, db, obj, data, commit=True):
        encoded_obj_data = jsonable_encoder(data)
        for field in encoded_obj_data:
            if hasattr(obj, field):
                setattr(obj, field, encoded_obj_data[field])
        db.add(obj)
        if commit:
            db.commit()
            db.refresh(obj)
        return obj

    def delete_all(self, db):
        return db.query(self.model).delete()
