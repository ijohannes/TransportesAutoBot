# TransportesAutoBot

## Introducción


Básicamente, le permite a cada usuario (propietario, mecánico) que interactúe con el bot, agregar información básica tanto del propietario como de sus vehículos, y el mecánico registra las revisiones a los vehículos.
Los datos de las tareas se almacenan en base de datos SQLite con ayuda del ORM SQLAlquemy así se da permanencia a los datos.

Para esto, utiliza comandos y órdenes además de un _middleware_ para garantizar que el usuario ya ejecutó el comando `/start` en su sesión.

Finalmente se utiliza _pooling_ para acceder al servicio de Telegram y obtener los mensajes que se hayan recibido.

## Preliminares

Para probar el bot con el servicio de Telegram, se requiere antes haber [creado uno propio con @BotFather](https://core.telegram.org/bots#creating-a-new-bot).

Para hacer esto, en pocas palabras se deben realizar los siguientes pasos.

 1. Contactar a [@BotFather](https://t.me/botfather).
 2. Ejecutar el comando `/newbot`.
 3. Proveer un nombre descriptivo para el nuevo bot.
 4. Proveer un nombre de usuario (unico, sin espacios y terminado en `bot`) para el nuevo bot.
 5. Tomar nota del `token` que envía de retorno @BotFather.

## Instalación

Una vez descargado el código fuente del bot, se deben instalar las librerías necesarias para su funcionamiento.

```
$ pip3 install -r requirements.txt
```

Crear un nuevo archivo `.env` y editar en él el valor de `TELEGRAM_TOKEN` con el indicado por @BotFather en la sección anterior.

```
$ cp .env-example .env

$ vi .env

TELEGRAM_TOKEN = "xxxxx"
```

## Ejecución

Para ejecutar el bot sólo es necesario ejecutar el siguiente comando.

```
$ python3 autobot.py
```

Si se desea que se reinicie automáticamente ante alguna excepción o cambios en el código fuente, lo cual es muy útil durante el desarrollo, se puede utilizar `nodemon`.

```
$ nodemon --exec python3 bot.py
```

## Manual de usuario

El bot soporta los siguientes comandos y órdenes.

| Órden | Descripción |
| --- | --- |
| `/start` | Inicia correctamente la sesión del usuario |
| `/help` | Este mensaje de ayuda |

## Recursos

 1. pyTelegramBot  
    [https://github.com/eternnoir/pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)
 1. Bots: An introduction for developers  
    [https://core.telegram.org/bots](https://core.telegram.org/bots)
 1. Telegram Bot API  
    [https://core.telegram.org/bots/api](https://core.telegram.org/bots/api)
 1. Unicode® Emoji Charts  
    [http://www.unicode.org/emoji/charts/](http://www.unicode.org/emoji/charts/)
 1. Markdown Cheatsheet  
    [https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet)
 1. re — Regular expression operations  
    [https://docs.python.org/3/library/re.html](https://docs.python.org/3/library/re.html)
 1. Ejemplos de expresiones regulares  
    [https://support.google.com/a/answer/1371417?hl=es](https://support.google.com/a/answer/1371417?hl=es)
 2. RegExLib.com  
    [https://regexlib.com/](https://regexlib.com/)
