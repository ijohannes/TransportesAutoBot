########################importar librerias#################################

from config import bot
import config
from time import sleep
from telebot import types
import re
import logic
import database.db as db
import validaciones

#########################################################

if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)

#########################################################
# Aquí vendrá la implementación de la lógica del bot AutoBot

bot_data_propietario = {}
bot_data_vehiculo = {}
bot_data_revision = {}
bot_data_mecanico = {}
class Record:
    def __init__(self):
        self.documento = None
        self.nombresApellidos = None
        self.celular = None
        self.correo = None
        self.direccion = None
        self.placa = None
        self.modelo = None
        self.marca = None
        self.fechaseguro= None
        self.docpropietario = None
        self.cantpasajero = None
        self.nivelLiqAceite = None
        self.nivelLiqFrenos = None
        self.nivelRefrigerante = None
        self.nivelLiqDireccion = None
        self.descripcion = None
        self.fechaRevision = None
        self.placaRevision = None
        self.docMecanico = None
        
        self.docmecanico = None
        self.nommecanico = None
        self.fecnacimecanico = None
        self.celularmecanico = None
        self.correomecanico = None


# Enable saving next step handlers to file "./.handlers-saves/step.save".
# Delay=2 means that after any change in next step handlers (e.g. calling register_next_step_handler())
# saving will hapen after delay 2 seconds.
bot.enable_save_next_step_handlers(delay=2)
# Load next_step_handlers from save file (default "./.handlers-saves/step.save")
# WARNING It will work only if enable_save_next_step_handlers was called!
bot.load_next_step_handlers()

@bot.message_handler(commands=['start'])
def on_command_start(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    m = bot.send_message(
        message.chat.id,
        "\U0001F916 Bienvenido al bot de Transportes AutoBot",
        parse_mode="Markdown")
    on_command_menu(message)
    
    
@bot.message_handler(commands=['help'])
def on_command_help(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    response = ("Estos son los comandos y órdenes disponibles:\n"
        "\n"
        "*/start* - Inicia la interacción con el bot\n"
        "*/help* - Muestra este mensaje de ayuda\n"
        "*/menu* - Inicia el proceso de registro de un vehículo de un propietario\n"
    )
    bot.send_message(
        message.chat.id,
        response,
        parse_mode="Markdown")
    
######################### COMANDO MENU ################################

@bot.message_handler(commands=['menu'])
def on_command_menu(message):
    # Using the ReplyKeyboardMarkup class
    # It's constructor can take the following optional arguments:
    # - resize_keyboard: True/False (default False)
    # - one_time_keyboard: True/False (default False)
    # - selective: True/False (default False)
    # - row_width: integer (default 3)
    # row_width is used in combination with the add() function.
    # It defines how many buttons are fit on each row before continuing on the next row.
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    itembtn1 = types.KeyboardButton('/propietario')
    itembtn2 = types.KeyboardButton('/help')    
    itembtn3 = types.KeyboardButton('/vehiculo')
    itembtn4 = types.KeyboardButton('/revision')
    itembtn5 = types.KeyboardButton('/mecanico')
    
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4, itembtn5)
    
    bot.send_message(message.chat.id, "Selecciona una opción del menú:", reply_markup=markup)
    
##################### Implementación del comando /propietario ####################################

@bot.message_handler(commands=['propietario'])
def on_command_propietario(message):
    response = bot.reply_to(message, "Digita tu documento")
    bot.register_next_step_handler(response, process_documento_step)

######################## Implementación de process_documento_step #################################
def process_documento_step(message):
    try:
        documento = str(message.text)
        if validaciones.contiene_solo_numeros(documento):
            record = Record()
            record.documento = documento
            validarPropietario = logic.validarPropietario(0,record.documento)
            if validarPropietario != None:
                response = bot.reply_to(message, "El propietario de documento ${documento} ya existe")
                bot.register_next_step_handler(response, on_command_menu(message))
            if validarPropietario == None:
                bot_data_propietario[message.chat.id] = record
                response = bot.reply_to(message, 'Digite sus nombres y apellidos')
                bot.register_next_step_handler(response, process_nomapel_step)
        else:
            bot.send_message(
            message.chat.id, "El número de documento solo debe contener números \U00002639. Te vuelvo a preguntar")
            response = bot.reply_to(message, "Digita tu documento")
            bot.register_next_step_handler(response, process_documento_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")


######################## Implementación de process_nomapel_step #################################
def process_nomapel_step(message):
    try:
        nombresApellidos = str(message.text)
        record = bot_data_propietario[message.chat.id]
        record.nombresApellidos = nombresApellidos
        # response = bot.reply_to(message, 'Digite su fecha de nacimiento yyyy-mm-dd')
        response = bot.reply_to(message, 'Digite su celular')
        bot.register_next_step_handler(response, process_celular_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")

######################## Implementación de process_fechanac_step #################################
# def process_fechanac_step(message):
#     try:
#         fechaNac = str(message.text)
#         record = bot_data_propietario[message.chat.id]
#         record.fechaNac = fechaNac
#         response = bot.reply_to(message, 'Digite su celular')
#         bot.register_next_step_handler(response, process_celular_step)
#     except Exception as e:
#         bot.reply_to(message, f"Algo terrible sucedió: {e}")

######################## Implementación de process_celular_step #################################
def process_celular_step(message):
    try:
        celular = str(message.text)
        if validaciones.es_celular(celular):
            record = bot_data_propietario[message.chat.id]
            record.celular = celular
            response = bot.reply_to(message, 'Digite su correo')
            bot.register_next_step_handler(response, process_correo_step)
        else:
            bot.send_message(
            message.chat.id, "El número de celular solo debe contener 10 digitos y solo números \U00002639. Te vuelvo a preguntar")
            response = bot.reply_to(message, "Digite su celular")
            bot.register_next_step_handler(response, process_celular_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")
        
######################## Implementación de process_correo_step #################################
def process_correo_step(message):
    try:
        correo = str(message.text)
        if validaciones.es_email(correo):
            record = bot_data_propietario[message.chat.id]
            record.correo = correo
            response = bot.reply_to(message, 'Digite su direccion')
            bot.register_next_step_handler(response, process_direccion_step)
        else:
            bot.send_message(
            message.chat.id, "El formato de correo no es valido \U00002639. Te vuelvo a preguntar")
            response = bot.reply_to(message, "Digite su correo")
            bot.register_next_step_handler(response, process_correo_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")

######################## Implementación de process_direccion_step #################################
def process_direccion_step(message):
    try:
        direccion = str(message.text)
        record = bot_data_propietario[message.chat.id]
        record.direccion = direccion
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Guardar')
        response = bot.reply_to(message, 'Guardar ', reply_markup=markup)
        bot.register_next_step_handler(response, process_info_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")

######################## Implementación de mostrar datos #################################
def process_info_step(message):
    guardar = message.text
    record = bot_data_propietario[message.chat.id]
    datos(message)

def datos(message):
    record = bot_data_propietario[message.chat.id]
    datosPropietario = f"Datos = Documento: {record.documento},\nNombres y apellidos: {record.nombresApellidos},\nCelular: {record.celular},\nCorreo: {record.correo},\nDirección: {record.direccion}"
    bot.reply_to(message, datosPropietario)
    control = logic.register_propietario(record.documento,record.nombresApellidos,record.celular,record.correo,record.direccion)

###############implementacion del comando vehiculo ####################
@bot.message_handler(commands=['vehiculo'])
def on_command_vehiculo(message):
    response = bot.reply_to(message, "Digite la placa del vehiculo")
    bot.register_next_step_handler(response, process_placa_step)

def process_placa_step(message):
    try:
        placa = str(message.text)
        record = Record()
        record.placa = placa
        if validaciones.es_placa(placa):
            bot_data_vehiculo[message.chat.id] = record
            response = bot.reply_to(message, 'Digite el modelo')
            bot.register_next_step_handler(response, process_modelo_step)
        else:
            bot.send_message(
            message.chat.id, "La placa debe ser en formato AAA123")
            response = bot.reply_to(message, "Digite la placa del vehiculo")
            bot.register_next_step_handler(response, process_placa_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")

def process_modelo_step(message):
    try:
        modelo = str(message.text)
        record = bot_data_vehiculo[message.chat.id]
        record.modelo = modelo
        response = bot.reply_to(message, 'Digite la marca')
        bot.register_next_step_handler(response, process_marca_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")

def process_marca_step(message):
    try:
        marca = str(message.text)
        record = bot_data_vehiculo[message.chat.id]
        record.marca = marca
        response = bot.reply_to(message, 'Digite fecha del seguro')
        bot.register_next_step_handler(response, process_fechaseguro_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")

def process_fechaseguro_step(message):
    try:
        fechaseguro = str(message.text)
        record = bot_data_vehiculo[message.chat.id]
        record.fechaseguro = fechaseguro
        response = bot.reply_to(message, 'Digite documento del propietario')
        bot.register_next_step_handler(response, process_docpropietario_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")

def process_docpropietario_step(message):
    try:
        docpropietario = str(message.text)
        record = bot_data_vehiculo[message.chat.id]
        record.docpropietario = docpropietario
        if validaciones.contiene_solo_numeros(docpropietario):
            validarDocpropietario = logic.validarPropietario(0,record.docpropietario)
            if validarDocpropietario != None:
                response = bot.reply_to(message, 'Digite cantidad de pasajeros')
                bot.register_next_step_handler(response, process_cantidad_step)
            if validarDocpropietario == None:
                bot_data_propietario[message.chat.id] = record
                response = bot.reply_to(message, 'el propietario no existe')
                bot.register_next_step_handler(response, on_command_propietario)
        else:
            bot.send_message(
            message.chat.id, "El número de documento solo debe contener números \U00002639. Te vuelvo a preguntar")
            response = bot.reply_to(message, "Digita tu documento")
            bot.register_next_step_handler(response, process_documento_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")
    """try:
        docpropietario = str(message.text)
        record = bot_data_vehiculo[message.chat.id]
        record.docpropietario = docpropietario
        response = bot.reply_to(message, 'Digite cantidad de pasajeros')
        bot.register_next_step_handler(response, process_cantidad_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")"""

def process_cantidad_step(message):
    try:
        cantpasajero = str(message.text)
        record = bot_data_vehiculo[message.chat.id]
        record.cantpasajero = cantpasajero
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Guardar')
        response = bot.reply_to(message, 'Guardar ', reply_markup=markup)
        bot.register_next_step_handler(response, process_infovehiculo_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")

def process_infovehiculo_step(message):
    guardar = message.text
    record = bot_data_vehiculo[message.chat.id]
    datosvehiculo(message)

def datosvehiculo(message):
    record = bot_data_vehiculo[message.chat.id]
    datosVehiculo = f"Datos = id: {message.from_user.id} placa: {record.placa},\nmodelo: {record.modelo},\marca: {record.marca},\docu propietario: {record.docpropietario}"
    bot.reply_to(message, datosVehiculo)
    control = logic.register_vehiculo(record.modelo,record.marca, record.fechaseguro, record.placa, record.cantpasajero, 1, record.docpropietario)

###############implementacion del comando mecanico ####################
@bot.message_handler(commands=['mecanico'])
def on_command_vehiculo(message):
    response = bot.reply_to(message, "Digite el documento del mencanico")
    bot.register_next_step_handler(response, process_docmecanico_step)

def process_docmecanico_step(message):
    try:
        docmecanico = str(message.text)
        if validaciones.contiene_solo_numeros(docmecanico):
            record = Record()
            record.docmecanico = docmecanico
            bot_data_mecanico[message.chat.id] = record
            response = bot.reply_to(message, 'Digite nombres y apellidos')
            bot.register_next_step_handler(response, process_nomapemecanico_step)
        else:
            bot.send_message(
            message.chat.id, "El número de documento solo debe contener números \U00002639. Te vuelvo a preguntar")
            response = bot.reply_to(message, "Digite el documento del mencanico")
            bot.register_next_step_handler(response, process_docmecanico_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")


def process_nomapemecanico_step(message):
    try:
        nommecanico = str(message.text)
        record = bot_data_mecanico[message.chat.id]
        record.nommecanico = nommecanico
        response = bot.reply_to(message, 'Digite la fecha de nacimieto')
        bot.register_next_step_handler(response, process_fecnacimecanico_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")

def process_fecnacimecanico_step(message):
    try:
        fecnacimecanico = str(message.text)
        record = bot_data_mecanico[message.chat.id]
        record.fecnacimecanico = fecnacimecanico
        response = bot.reply_to(message, 'Digite celular')
        bot.register_next_step_handler(response, process_celularmecanico_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")

def process_celularmecanico_step(message):
    try:
        celularmecanico = str(message.text)
        if validaciones.es_celular(celularmecanico):
            record = bot_data_mecanico[message.chat.id]
            record.celularmecanico = celularmecanico
            response = bot.reply_to(message, 'Digite su correo')
            bot.register_next_step_handler(response, process_correomecanico_step)
        else:
            bot.send_message(
            message.chat.id, "El número de celular solo debe contener 10 digitos y solo números \U00002639. Te vuelvo a preguntar")
            response = bot.reply_to(message, "Digite su celular")
            bot.register_next_step_handler(response, process_celularmecanico_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")
        
def process_correomecanico_step(message):
    try:
        correomecanico = str(message.text)
        if validaciones.es_email(correomecanico):
            record = bot_data_mecanico[message.chat.id]
            record.correomecanico = correomecanico
            response = bot.reply_to(message, 'Digite su direccion')
            bot.register_next_step_handler(response, process_direccionmecanico_step)
        else:
            bot.send_message(
            message.chat.id, "El formato de correo no es valido \U00002639. Te vuelvo a preguntar")
            response = bot.reply_to(message, "Digite correo")
            bot.register_next_step_handler(response, process_correomecanico_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")

def process_direccionmecanico_step(message):
    try:
        direccionmecanico = str(message.text)
        record = bot_data_mecanico[message.chat.id]
        record.direccionmecanico = direccionmecanico
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        markup.add('Guardar')
        response = bot.reply_to(message, 'Guardar ', reply_markup=markup)
        bot.register_next_step_handler(response, process_infomecanico_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")


def process_infomecanico_step(message):
    guardar = message.text
    record = bot_data_mecanico[message.chat.id]
    datosmecanico(message)

def datosmecanico(message):
    record = bot_data_mecanico[message.chat.id]
    datosMecanico = f"Datos = id: {message.from_user.id} doc mecanico: {record.docmecanico},\n nombre: {record.nommecanico},\nfecha nacimiento: {record.fecnacimecanico},\celular: {record.celularmecanico},\correo: {record.correomecanico},\direccion: {record.direccionmecanico}"
    bot.reply_to(message, datosMecanico)
    control = logic.register_Mecanico(record.docmecanico,record.nommecanico,record.fecnacimecanico,record.celularmecanico,record.correomecanico,record.direccionmecanico)


##################### Implementación del comando /revision ####################################

@bot.message_handler(commands=['revision'])
def on_command_revision(message):
    try:
        markup = types.ForceReply
        markup = types.ReplyKeyboardMarkup(
            one_time_keyboard=True, 
            input_field_placeholder="Pulsa un botón",
            resize_keyboard=True
        )
        markup.add('Alto', 'Bajo')
        response = bot.reply_to(message, 'Nivel de aceite', reply_markup=markup)
        bot.register_next_step_handler(response, process_nivelLiqAceite_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")


def process_nivelLiqAceite_step(message):
    try:
        nivelLiqAceite = message.text
        record = Record()
        record.nivelLiqAceite = nivelLiqAceite
        bot_data_revision[message.chat.id] = record
        markup = types.ReplyKeyboardMarkup(
            one_time_keyboard=True, 
            input_field_placeholder="Pulsa un botón",
            resize_keyboard=True
        )
        markup.add('Bajo', 'Lleno')
        response = bot.reply_to(message, 'Nivel líquido de frenos', reply_markup=markup)
        bot.register_next_step_handler(response, process_liquidoFrenos_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")

def process_liquidoFrenos_step(message):
    try:
        nivelLiqFrenos = message.text
        record = bot_data_revision[message.chat.id]
        record.nivelLiqFrenos = nivelLiqFrenos
        markup = types.ReplyKeyboardMarkup(
            one_time_keyboard=True, 
            input_field_placeholder="Pulsa un botón",
            resize_keyboard=True
        )
        markup.add('Mínimo', 'Máximo')
        response = bot.reply_to(message, 'Nivel de refrigerante', reply_markup=markup)
        bot.register_next_step_handler(response, process_nivelRefrigerante_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")

def process_nivelRefrigerante_step(message):
    try:
        nivelRefrigerante = message.text
        record = bot_data_revision[message.chat.id]
        record.nivelRefrigerante = nivelRefrigerante
        markup = types.ReplyKeyboardMarkup(
            one_time_keyboard=True, 
            input_field_placeholder="Pulsa un botón",
            resize_keyboard=True
        )
        markup.add('Mínimo', 'Máximo')
        response = bot.reply_to(message, 'Nivel líquido de dirección', reply_markup=markup)
        bot.register_next_step_handler(response, process_nivelLiqDireccion_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")
        
def process_nivelLiqDireccion_step(message):
    try:
        nivelLiqDireccion = message.text
        record = bot_data_revision[message.chat.id]
        record.nivelLiqDireccion = nivelLiqDireccion
        markup = types.ReplyKeyboardMarkup(
            one_time_keyboard=True, 
            input_field_placeholder="Pulsa un botón",
            resize_keyboard=True
        )
        response = bot.reply_to(message, 'Descripción')
        bot.register_next_step_handler(response, process_descripcion_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")

def process_descripcion_step(message):
    try:
        descripcion = str(message.text)
        record = bot_data_revision[message.chat.id]
        record.descripcion = descripcion
        response = bot.reply_to(message, 'Digite Fecha Revisión yyyy-mm-dd')
        bot.register_next_step_handler(response, process_fechaRevision_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")

def process_fechaRevision_step(message):
    try:
        fechaRevision = str(message.text)
        record = bot_data_revision[message.chat.id]
        record.fechaRevision = fechaRevision
        response = bot.reply_to(message, 'Digite Placa AAA-123')
        bot.register_next_step_handler(response, process_placaRevision_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")

def process_placaRevision_step(message):
    try:
        placaRevision = str(message.text)
        if validaciones.es_placa(placaRevision):
            record = bot_data_revision[message.chat.id]
            record.placaRevision = placaRevision
            response = bot.reply_to(message, 'Digite cédula del mecánico')
            bot.register_next_step_handler(response, process_docMecanico_step)
        else:
            bot.send_message(
            message.chat.id, "El formato de placa no es valido \U00002639. Te vuelvo a preguntar")
            response = bot.reply_to(message, "Digite Placa ABC-123")
            bot.register_next_step_handler(response, process_placaRevision_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")


def process_docMecanico_step(message):
    try:
        docMecanico = str(message.text)
        if validaciones.contiene_solo_numeros(docMecanico):
            record = bot_data_revision[message.chat.id]
            record.docMecanico = docMecanico
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.add('Guardar')
            response = bot.reply_to(message, 'Guardar ', reply_markup=markup)
            bot.register_next_step_handler(response, process_guardarRevision_step)
        else:
            bot.send_message(
            message.chat.id, "El documento debe contener solo números \U00002639. Te vuelvo a preguntar")
            response = bot.reply_to(message, "Digite cédula del mecánico")
            bot.register_next_step_handler(response, process_docMecanico_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")

def process_guardarRevision_step(message):
    guardar = message.text
    record = bot_data_revision[message.chat.id]
    datos(message)

def datos(message):
    record = bot_data_revision[message.chat.id]
    datosRevision = f"Datos = Nivel L. Aceite: {record.nivelLiqAceite},\nNivel L. Frenos: {record.nivelLiqFrenos},\nRefrigerante: {record.nivelRefrigerante},\nNivel L. Dirección: {record.nivelLiqDireccion},\nDescripción: {record.descripcion},\nFecha Revision: {record.fechaRevision},\nPlaca: {record.placaRevision},\nMecánico: {record.docMecanico}"
    bot.reply_to(message, datosRevision)
    control = logic.register_revision(record.nivelLiqAceite,record.nivelLiqFrenos,record.nivelRefrigerante,record.nivelLiqDireccion,record.descripcion,record.nivelfechaRevision,record.docMecanico)

######################## Implementación del fallback #################################

@bot.message_handler(func=lambda message: True)
def on_fallback(message):
    bot.send_chat_action(message.chat.id, 'typing')
    sleep(1)
    bot.reply_to(
        message,
        "\U0001F63F Ups, no entendí lo que me dijiste.")

#########################################################
if __name__ == '__main__':
    bot.infinity_polling()
#########################################################