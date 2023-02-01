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
class Record:
    def __init__(self):
        self.documento = None
        self.nombresApellidos = None
        self.fechaNac = None
        self.celular = None
        self.correo = None
        self.direccion = None

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
    # itembtn3 = types.KeyboardButton('/mecanico')
    
    markup.add(itembtn1, itembtn2)
    
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