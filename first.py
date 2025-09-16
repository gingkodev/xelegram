# MI PRIMER BOT

# loggeo + telegram
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
# importo tweepy (interfaz para la API de tw) y json, para poder trabajar con el config (que no tuve mejor idea que hacerlo como .json)
import tweepy
import json


# Declare variables before try block
keys = None
api_key = api_key_secret = access_token_id = access_token_secret = bearer_token = telegram_token = telegram_id = None
client = None

# Load config and assign variables with error handling
try:
    with open("config.json", "r") as f:
        keys = json.load(f)
    # keys de twitter
    api_key = keys["api_key"]
    api_key_secret = keys["api_key_secret"]
    access_token_id = keys["access_token_id"]
    access_token_secret = keys["access_token_secret"]
    bearer_token = keys["bearer_token"]
    # key del bot
    telegram_token = keys["tl_bot_token"]
    # mi user id de telegram
    telegram_id = keys["tl_user_id"]
    # instancio cliente de tweepy
    client = tweepy.Client(bearer_token, api_key, api_key_secret, access_token_id, access_token_secret)
except FileNotFoundError:
    print("Config file 'config.json' not found! Bot will not start.")
    exit(1)
except json.JSONDecodeError:
    print("Config file is not valid JSON! Bot will not start.")
    exit(1)
except KeyError as e:
    print(f"Missing key in config: {e}. Bot will not start.")
    exit(1)
except Exception as e:
    print(f"Unexpected error loading config or initializing Tweepy: {e}")
    exit(1)

# def fx: respuesta al comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="bienvenido a twitter gordo!"
    )
# este responde lo que le digo
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=context._user_id)

# esta tuitea
async def tweet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.message.message_id) 
    # solo twittea si soy yo el que le digo que twitee
    if context._user_id != telegram_id:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="MMM VOS NO SOS EL JEFE!!!" + context._user_id + " VS " + context._user_id)
        return
    # trycatcheo el tweet, revisar awaits
    try:
        client.create_tweet(text=update.message.text)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="bien tuiteado, boludito")
    except tweepy.TweepyException as e:
        print(e)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="no pudiste pa! paso esto: ")

if __name__ == '__main__':
    # build bot
    application = ApplicationBuilder().token(keys["tl_bot_token"]).build()

    # asigno handleos de funcion a mensajes o comandos que le lleguen al bot
    start_handler = CommandHandler('start', start)
    # echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    tweet_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), tweet)

    # le agrego estos handleos al bot
    application.add_handler(start_handler)
    # application.add_handler(echo_handler)
    application.add_handler(tweet_handler)

    # corro el bot :p
    application.run_polling()



