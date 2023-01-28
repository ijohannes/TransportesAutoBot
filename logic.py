import database.db as db
from models.propietario import Propietario
from models.vehiculo import Vehiculo
from datetime import datetime
from sqlalchemy import extract

def register_propietario(user_id,documento='',nombre='',fechaNacimiento='',celular='',correo='',direccion=''):
    propietario = db.session.query(propietario).get(user_id)
    db.session.commit()
    if propietario == None:
        propietario = propietario(user_id, documento,nombre,fechaNacimiento,celular,correo,direccion)
        db.session.add(propietario)
        db.session.commit()
        return True
    return False

def get_welcome_message(bot_data):
    response = (
                f"Hola, soy *{bot_data.first_name}* "
                f"también conocido como *{bot_data.username}*.\n\n"
                "¡Estoy aquí para ayudarte en tu proceso!"
                )
    return response