import database.db as db
import validaciones
from models.propietario import Propietario
from models.vehiculo import Vehiculo
from datetime import datetime
from sqlalchemy import extract
import validaciones

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
    
def validarPropietario(documento):
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

def validarDocumento(documento):
    documento = validaciones.contiene_solo_numeros(documento)
    return documento













def register_revision(aceite,frenos,refrigerante,direccion,descripcion,fechaRevision,placa,docMecanico):
    revision = db.session.query(Propietario).filter(Propietario.documento==documento).first()
    db.session.commit()
    if propietario == None:
        propietario = Propietario(documento, nombre, celular, correo, direccion)
        db.session.add(propietario)
        db.session.commit()
        return True
    return False