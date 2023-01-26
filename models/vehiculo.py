import database.db as db
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey,func
from sqlalchemy.orm import relationship

class Earning(db.Base):

    __tablename__ = 'Vehiculo'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    modelo = Column('modelo', String, nullable=False)
    marca = Column('marca', String, nullable=False)
    fechaseguro = Column('fechaseguro', String, nullable=False)
    placa = Column('placa', String, nullable=False)
    cantidadpasajero = Column('cantidadpasajero', String, nullable=False)
    estado = Column('estado', String, nullable=False)
    documentopropietario = Column('documentopropietario', String, ForeignKey('propietario.documento', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    documentos = relationship("Propietario", back_populates="Vehiculo")
    
    def __init__(self, amount, when, documentopropietario):
        self.amount = amount
        self.when = when
        self.documentopropietario = documentopropietario
    
    def __repr__(self):
        return f"<Vehiculo {self.id}>"
        