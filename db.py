import sqlite3  # Импортируем библиотеку для работы с SQLite
from sqlite3 import Error  # Импортируем класс для обработки ошибок SQLite
from config import DB_FILE  # Импортируем путь к файлу базы данных из конфигурации
import logging  # Импортируем библиотеку для логирования

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем подключение к БД
def create_connection():
    conn = None  # Инициализируем переменную для хранения соединения
    try:
        # Устанавливаем соединение с базой данных, отключая проверку потоков
        conn = sqlite3.connect(DB_FILE, check_same_thread=False)
        logger.info(f'SQLite version: {sqlite3.version}')  # Выводим версию SQLite
    except Error as e:
        logger.error(f'Ошибка при подключении к базе данных: {e}')  # Логируем ошибку

    return conn  # Возвращаем объект соединения (может быть None)

# Создаем таблицу users, если она не существует
def create_table(conn):
    try:
        # SQL-запрос для создания таблицы users с тремя полями
        sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY,  -- ID Пользователя
                                        voice_id integer DEFAULT 0,  -- Идентификатор голоса
                                        rate integer DEFAULT 200   -- Скорость речи
                                    ); """

        c = conn.cursor()  # Создаем курсор для выполнения SQL-запросов
        c.execute(sql_create_users_table)  # Выполняем запрос на создание таблицы
    except Error as e:
        logger.error(f'Ошибка при создании таблицы: {e}')  # Логируем ошибку

# Сохранение пользовательских настроек
def save_user_settings(conn, user_id, voice_id, rate):
    try:
        # SQL-запрос для вставки или замены записи в таблице users
        sql = ''' INSERT OR REPLACE INTO users(id, voice_id, rate) VALUES(?,?,?) '''
        
        cur = conn.cursor()  # Создаем курсор для выполнения SQL-запросов
        cur.execute(sql, (user_id, int(voice_id)-1, rate))  # Выполняем запрос с передачей параметров
        conn.commit()  # Применяем изменения в базе данных
    except Error as e:
        logger.error(f'Ошибка при сохранении настроек пользователя: {e}')  # Логируем ошибку

# Получение пользовательских настроек
def get_user_settings(conn, user_id):
    try:
        cur = conn.cursor()  # Создаем курсор для выполнения SQL-запросов
        # Выполняем запрос для получения настроек пользователя по его идентификатору
        cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
        row = cur.fetchone()  # Получаем первую строку результата запроса

        if row:  # Если пользователь найден
            return row[1], row[2]  # Возвращаем voice_id и rate
        else:
            logger.info(f'Пользователь с id {user_id} не найден.')  # Логируем, что пользователь не найден
            return None, None  # Если пользователь не найден, возвращаем None
    except Error as e:
        logger.error(f'Ошибка при получении настроек пользователя: {e}')  # Логируем ошибку

# Закрываем подключение к БД
def close_connection(conn):
    if conn:
        try:
            conn.close()
            logger.info('Соединение с базой данных закрыто.')
        except Error as e:
            logger.error(f'Ошибка при закрытии соединения: {e}')  # Логируем ошибку
