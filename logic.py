import database.db as db
from models.propietario import propietario
from models.vehiculo import vehiculo
from datetime import datetime
from sqlalchemy import extract

def register_propietario(user_id):
    propietario = db.session.query(propietario).get(user_id)
    db.session.commit()
    if propietario == None:
        propietario = propietario(user_id, '','','','','','')
        db.session.add(propietario)
        db.session.commit()
        return True
    return False