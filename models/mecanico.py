import database.db as db
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey,func
from sqlalchemy.orm import relationship

class Mecanico(db.Base):
    
    __tablename__ = 'Mecanico'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    documento = Column('documento', String, nullable=False)
    nombre = Column('nombre', String, nullable=False)
    fechanacimiento = Column('fechanacimiento', String, nullable=False)
    celular = Column('celular', String, nullable=False)
    correo = Column('correo', String, nullable=False)
    direccion = Column('direccion', String, nullable=False)
    
    revision = relationship("Revision", back_populates="docMecanico")
    
    
    def __init__(self, documento,nombre,fechanacimiento,celular,correo,direccion):
  
        self.documento = documento
        self.nombre = nombre
        self.fechanacimiento =  fechanacimiento
        self.celular = celular
        self.correo = correo
        self.direccion = direccion
        #self.documentopropietario = documentopropietario
    
    def __repr__(self):
        return f"<Mecanico {self.id}>"
        