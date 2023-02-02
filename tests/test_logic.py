import unittest
from models.propietario import Propietario
import logic

class TestLogic(unittest.TestCase):
    
    def test_validarDocumento(self):
        self.assertTrue(logic.validarDocumento('123456'),"Documento valido")
        self.assertFalse(logic.validarDocumento('123456abc'),"Documento no valido")
        self.assertFalse(logic.validarDocumento('  '),"Documento vacio")
    
    def test_register_propietario(self):
        self.assertTrue(logic.register_propietario('1020304059','Usuario nuevo', '3216549870', 'usuario.nuevo@correo.com', 'Manizales'), 'Usuario registrado')
        
    def test_register_propietario_doc_duplicado(self):
        self.assertFalse(logic.register_propietario('1020304054','Andrea Martinez', '3526412111', 'andrea.martinez@correo.com', 'Manizales'), 'Usuario con mismo documento')
    
    def test_validarPropietario(self):
        self.assertTrue(logic.validarPropietario('1020304050'),"Usuario existe") 