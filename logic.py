import database.db as db
from models.propietario import Propietario
from models.vehiculo import Vehiculo
from datetime import datetime
from sqlalchemy import extract

def register_propietario(documento,nombre,celular,correo,direccion):
    propietario = db.session.query(Propietario).filter(Propietario.documento==documento).first()
    db.session.commit()
    if propietario == None:
        propietario = Propietario(documento, nombre, celular, correo, direccion)
        db.session.add(propietario)
        db.session.commit()
        return True
    return False

def validarPropietario(user_id,documento):
    propietario = db.session.query(Propietario).filter(Propietario.documento==documento).first()
    db.session.commit()
    if not propietario:
        return None
    return "{propietario.documento}"

def get_welcome_message(bot_data):
    response = (
                f"Hola, soy *{bot_data.first_name}* "
                f"también conocido como *{bot_data.username}*.\n\n"
                "¡Estoy aquí para ayudarte en tu proceso!"
                )
    return response