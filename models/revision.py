import database.db as db
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship


class Revision(db.Base):
    
    __tablename__ = 'Revision'
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    nivelliqaceite = Column('nivelliqaceite', String, server_default='', nullable=False)
    nivelliqfrenos = Column('nivelliqfrenos', String, server_default='', nullable=False)
    nivelrefrigerante = Column('nivelrefrigerante', String, server_default='', nullable=False)
    nivelliqdireccion = Column('nivelliqdireccion', String, server_default='', nullable=False)
    descripcion = Column('descripcion', String, server_default='', nullable=False)
    fecharevision = Column('fecharevision', String, server_default='', nullable=False)
    
    vehiculoplaca = Column('vehiculoplaca', String, ForeignKey('Vehiculo.placa', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    docmecanico = Column('docmecanico', String, ForeignKey('Mecanico.documento', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    
    vehiculo_placa = relationship('Vehiculo', back_populates='revision')
    docMecanico = relationship('Mecanico', back_populates='revision')
    
    def __init__(self, nivelliqaceite, nivelliqfrenos, nivelrefrigerante,nivelliqdireccion,descripcion,fecharevision,vehiculoplaca,docmecanico):
        self.nivelliqaceite = nivelliqaceite
        self.nivelliqfrenos = nivelliqfrenos
        self.nivelrefrigerante = nivelrefrigerante
        self.nivelliqdireccion = nivelliqdireccion
        self.descripcion = descripcion
        self.fecharevision = fecharevision
        self.vehiculoplaca = vehiculoplaca
        self.docmecanico = docmecanico
        
        
    def __repr__(self):
        return f"<Revision {self.id}>"