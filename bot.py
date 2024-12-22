import telebot
import pyttsx3
import config
import handlers
from db import create_connection, create_table
from voice import get_voices
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация
logger.info('Инициализация...')
voice = pyttsx3.init()
voices = get_voices()

# Создание соединения с базой данных
conn = create_connection()
if conn:
    create_table(conn)
else:
    logger.error("Не удалось создать соединение с базой данных.")
    exit(1)  # Завершаем работу, если соединение не удалось

bot = telebot.TeleBot(config.TOKEN)

# Регистрация обработчиков
@bot.message_handler(commands=["start"])
def start(message):
    handlers.start(message, bot, conn)
    logger.info(f'Начата работа с пользователем: {message.chat.id}')

@bot.message_handler(commands=["setvoice"])
def set_voice(message):
    handlers.set_voice(message, bot, conn, voices)

@bot.message_handler(func=lambda message: message.text.isdigit() and 0 < int(message.text) <= len(voices))
def change_voice(message):
    handlers.change_voice(message, bot, conn, voices)

@bot.message_handler(commands=["setrate"])
def set_rate(message):
    handlers.set_rate(message, bot, conn)

@bot.message_handler(func=lambda message: message.text.isdigit() and int(message.text) > 0)
def change_rate(message):
    handlers.change_rate(message, bot, conn)

@bot.message_handler(content_types=['text'])
def voice_over(message):
    handlers.voice_over(message, bot, voice, voices, conn)

# Запуск бота
logger.info('Запуск бота...')
if __name__ == "__main__":
    logger.info('Бот запущен')
    try:
        # Бесконечный цикл для приема сообщений
        while True:
            try:
                bot.polling(none_stop=True, interval=0)
            except Exception as e:
                logger.error(f'Ошибка в polling: {e}')
    except KeyboardInterrupt:
        # Останавливаем работу бота при нажатии Ctrl+C
        logger.info("Бот остановлен")
        bot.stop_polling()
    finally:
        if conn:
            conn.close()  # Закрываем соединение с БД при завершении работы
            logger.info("Соединение с базой данных закрыто.")
