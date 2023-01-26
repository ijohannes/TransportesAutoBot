import database.db as db
from sqlalchemy import Column, Integer, String, Float, Date
from sqlalchemy.orm import relationship

class Account(db.Base):
    __tablename__ = 'Propietario'
    
    id = Column('id', String(15), primary_key=True, nullable=False)
    nombre = Column('nombre', String, server_default='', nullable=False)
    documento = Column('documento', String, server_default='', nullable=False)
    fechanacimiento = Column('fechanacimiento', Date, server_default='', nullable=False)
    celular = Column('celular', String, server_default='', nullable=False)
    direccion = Column('direccion', String, server_default='', nullable=False)
    vehiculo = relationship('Vehiculo', back_populates='documentos')
    
    def __init__(self, id, balance=0):
        self.id = id
        self.balance = balance
    
    def __repr__(self):
        return f"<Propietario {self.id}>"