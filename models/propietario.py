import database.db as db
from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import relationship
from datetime import datetime

class Propietario(db.Base):
    __tablename__ = 'Propietario'
    
    id = Column('id', String(15), primary_key=True, nullable=False)
    documento = Column('documento', String, server_default='', nullable=False)
    nombre = Column('nombre', String, server_default='', nullable=False)
    # fechanacimiento = Column('fechanacimiento', Date, server_default='', nullable=False)
    celular = Column('celular', String, server_default='', nullable=False)
    correo = Column('correo', String, server_default='', nullable=False)
    direccion = Column('direccion', String, server_default='', nullable=False)
    vehiculo = relationship('Vehiculo', back_populates='propietario')
    
    def __init__(self, id, documento='', nombre='', celular='',correo='',direccion=''):
        self.id = id
        self.documento = documento
        self.nombre = nombre
        # self.fechanacimiento = datetime.strptime(fechanacimiento, '%m/%d/%y')
        self.celular = celular
        self.correo = correo
        self.direccion = direccion
        
    def __repr__(self):
        return f"<Propietario {self.id}>"