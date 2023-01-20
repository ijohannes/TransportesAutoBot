#########################################################
import config
import re

from config import bot
from telebot import types
from time import sleep

#########################################################
# Aquí vendrá la implementación de la lógica del bot

bot_data = {}
class Record:
    def __init__(self):
        self.placa = None
        self.tipo = None
        self.modelo = None
        self.marca = None
        self.seguro = None
        self.cantidad = None

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
    itembtn3 = types.KeyboardButton('/mecanico')
    
    markup.add(itembtn1, itembtn2, itembtn3)
    
    bot.send_message(message.chat.id, "Selecciona una opción del menú:", reply_markup=markup)
    
##################### 9.6 Implementación del comando /imc ####################################

@bot.message_handler(commands=['propietario'])
def on_command_propietario(message):
    response = bot.reply_to(message, "Digita la placa del vehículo")
    bot.register_next_step_handler(response, process_placa_step)

######################## 9.6.1 Implementación de process_placa_step #################################

def process_placa_step(message):
    try:
        placa = str(message.text)
        record = Record()
        record.placa = placa
        bot_data[message.chat.id] = record
        response = bot.reply_to(message, 'Digita tipo: Microbus, buseta')
        bot.register_next_step_handler(response, process_tipo_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")


######################## 9.6.1 Implementación de process_placa_step #################################

def process_tipo_step(message):
    try:
        tipo = str(message.text)
        record = Record()
        record.tipo = tipo
        bot_data[message.chat.id] = record
        response = bot.reply_to(message, 'Digita modelo (año)')
        bot.register_next_step_handler(response, process_modelo_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")

######################## 9.6.2 Implementación de process_modelo_step #################################

def process_modelo_step(message):
    try:
        modelo = str(message.text)
        record = Record()
        record.modelo = modelo
        bot_data[message.chat.id] = record
        response = bot.reply_to(message, 'Digita marca')
        bot.register_next_step_handler(response, process_marca_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")

######################## 9.6.2 Implementación de process_marca_step #################################

def process_marca_step(message):
    try:
        marca = str(message.text)
        record = Record()
        record.marca = marca
        bot_data[message.chat.id] = record
        response = bot.reply_to(message, 'Digita seguro: ')
        bot.register_next_step_handler(response, process_seguro_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")

######################## 9.6.2 Implementación de process_seguro_step #################################

def process_seguro_step(message):
    try:
        seguro = str(message.text)
        record = Record()
        record.seguro = seguro
        bot_data[message.chat.id] = record
        response = bot.reply_to(message, 'Digita cantidad puestos: ')
        bot.register_next_step_handler(response, process_cantidad_step)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")

######################## 9.6.2 Implementación de process_cantidad_pasajeros_step #################################

def process_cantidad_step(message):
    try:
        cantidad = str(message.text)
        record = Record()
        record.cantidad = cantidad
        bot_data[message.chat.id] = record
        response = bot.reply_to(message, 'Registro completado: ')
        bot.register_next_step_handler(response, registroPropietario)
    except Exception as e:
        bot.reply_to(message, f"Algo terrible sucedió: {e}")


######################## 9.6.3 Implementación de process_gender_step #################################

# def process_gender_step(message):
#             gender = message.text
#             record = bot_data[message.chat.id]
#             record.gender = gender
#             imc(message)

######################## 9.6.4 Implementación de la función imc #################################

def registroPropietario(message):
    record = bot_data[message.chat.id]
    # registroPropietario = record.tipoVehiculo / pow(record.height, 2)
    answer = f"Registro\nPlaca: {record.placa},\nTipoVehiculo: {record.tipo},\nModelo:{record.modelo},\nMarca:{record.marca}\nSeguro: {record.seguro},\nCantidadPuestos = {record.cantidad}"
    bot.reply_to(message, answer)

######################## 9.7 Implementación del fallback #################################

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