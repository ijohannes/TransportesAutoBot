import database.db as db
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey,func
from sqlalchemy.orm import relationship

class Vehiculo(db.Base):
    
    __tablename__ = 'Vehiculo'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    modelo = Column('modelo', String, nullable=False)
    marca = Column('marca', String, nullable=False)
    fechaseguro = Column('fechaseguro', String, nullable=False)
    placa = Column('placa', String, nullable=False)
    cantidadpasajero = Column('cantidadpasajero', String, nullable=False)
    estado = Column('estado', String, nullable=False)
    
    documentopropietario = Column('documentopropietario', String, ForeignKey('Propietario.documento', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    
    propietario = relationship("Propietario", back_populates="vehiculo")
    revision = relationship("Revision", back_populates="vehiculo_placa")
    
    def __init__(self, modelo, marca, fechaseguro, placa, cantidadpasajero, estado, documentopropietario):
  
        self.modelo = modelo
        self.marca = marca
        self.fechaseguro =  fechaseguro
        self.placa = placa
        self.cantidadpasajero = cantidadpasajero
        self.estado = estado
        self.documentopropietario = documentopropietario
    
    def __repr__(self):
        return f"<Vehiculo {self.id}>"
        