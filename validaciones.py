'''
Encargado de validar tipos de datos
@author Néstor Geovanny Triana Tobar <nestor.trianat@autonoma.edu.co>
@author Andrea Martinez Villa <andrea.martinezv@autonoma.eu.co>
@author Estefania Giraldo <estefania.giraldoc@autonoma.edu.co>
'''
import re


'''
Valida que la cadena es un email
@param string cadena cadena a validar
@return boolean si es email retorna True, de lo contrario False
'''

def es_email(cadena):
    return True if re.search(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$', cadena) != None else False


'''
Valida que la cadena es una placa
@param string cadena cadena a validar
@return boolean si es el formato de placa retorna True, de lo contrario False
'''

def es_placa(cadena):
    return True if re.match(r'^[A-Z]{3}[\s-][0-9]{3}$', cadena) != None else False

'''
Valida que la cadena solo contiene números
@param string cadena cadena a validar
@return boolean si contiene solo números retorna True, de lo contrario False
'''
def contiene_solo_numeros(cadena):
    return True if re.match(r'^([\s\d]+)$', cadena) != None else False

'''
Valida que la cadena solo contiene 10 números
@param string cadena cadena a validar
@return boolean si contiene solo números retorna True, de lo contrario False
'''
def es_celular(cadena):
    return True if re.match(r'^([0-9]{10})$', cadena) != None else False

