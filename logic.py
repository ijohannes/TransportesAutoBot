import database.db as db
from models.propietario import Propietario
from models.vehiculo import Vehiculo
from datetime import datetime
from sqlalchemy import extract

def register_propietario(user_id,documento='',nombre='',celular='',correo='',direccion=''):
    propietario = db.session.query(Propietario).get(user_id)
    db.session.commit()
    if propietario == None:
        propietario = Propietario(user_id, documento, nombre, celular, correo, direccion)
        db.session.add(propietario)
        db.session.commit()
        return True
    return False

def register_vehiculo(modelo, marca, fechaseguro, placa, cantidadpasajero, estado, documentopropietario):
    vehiculo = db.session.query(Vehiculo).filter(Vehiculo.placa==placa).first()
    db.session.commit()
    if vehiculo == None:
        vehiculo = Vehiculo(modelo, marca, fechaseguro, placa, cantidadpasajero, estado, documentopropietario)
        db.session.add(vehiculo)
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