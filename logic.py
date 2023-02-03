import database.db as db
from models.propietario import Propietario
from models.vehiculo import Vehiculo
from models.mecanico import Mecanico
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

def register_vehiculo(modelo, marca, fechaseguro, placa, cantidadpasajero, estado, documentopropietario):
    vehiculo = db.session.query(Vehiculo).filter(Vehiculo.placa==placa).first()
    db.session.commit()
    if vehiculo == None:
        vehiculo = Vehiculo(modelo, marca, fechaseguro, placa, cantidadpasajero, estado, documentopropietario)
        db.session.add(vehiculo)
        db.session.commit()
        return True
    return False
    
def validarPropietario(user_id,documento):
    propietario = db.session.query(Propietario).filter(Propietario.documento==documento).first()
    db.session.commit()
    if not propietario:
        return None
    return "{propietario.documento}"

def register_Mecanico(docmecanico,nommecanico,fecnacimecanico,celularmecanico,correomecanico,direccionmecanico):
    mecanico = db.session.query(Mecanico).filter(Mecanico.documento==docmecanico).first()
    db.session.commit()
    if mecanico == None:
        mecanico = Mecanico(docmecanico,nommecanico,fecnacimecanico,celularmecanico,correomecanico,direccionmecanico)
        db.session.add(mecanico)
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