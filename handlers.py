import os
from db import *  # Импортируем все функции и классы из модуля db
from voice import *  # Импортируем все функции и классы из модуля voice

def start(message, bot, conn):
    # Отправляем пользователю приветственное сообщение с инструкциями
    bot.send_message(message.chat.id, 'Напишите мне сообщение, и я его озвучу.\nИспользуйте команду /setvoice для выбора голоса и /setrate для изменения скорости.')

def set_voice(message, bot, conn, voices):
    # Формируем список доступных голосов
    voice_list = "\n".join([f"{i + 1}: {v.name}" for i, v in enumerate(voices)])
    # Отправляем текущее название голоса пользователю
    bot.send_message(message.chat.id, f'Текущий голос: {voices[get_user_settings(conn, message.chat.id)[0]].name}')
    # Отправляем список доступных голосов и запрашиваем номер голоса
    bot.send_message(message.chat.id, f'Доступные голоса:\n\n{voice_list}\n\nВведите номер голоса, который хотите использовать.')
    # Регистрируем следующий шаг, который будет обработан функцией change_voice
    bot.register_next_step_handler(message, lambda m: change_voice(m, bot, conn, voices))

def change_voice(message, bot, conn, voices):
    # Получаем ID выбранного голоса от пользователя
    voice_id = int(message.text)
    # Получаем текущую скорость речи пользователя
    rate = get_user_settings(conn, message.chat.id)[1]
    # Сохраняем настройки пользователя (выбранный голос и скорость)
    save_user_settings(conn, message.chat.id, voice_id, rate)
    # Подтверждаем изменение голоса пользователю
    bot.send_message(message.chat.id, f'Голос изменен на: {voices[voice_id - 1].name}')

def set_rate(message, bot, conn):
    # Отправляем пользователю текущую скорость речи
    bot.send_message(message.chat.id, f'Текущая скорость речи: {get_user_settings(conn, message.chat.id)[1]}')
    # Запрашиваем новую скорость речи у пользователя
    bot.send_message(message.chat.id, 'Введите желаемую скорость (например, 150 для медленного, 200 для нормального, 300 для быстрого):')
    # Регистрируем следующий шаг, который будет обработан функцией change_rate
    bot.register_next_step_handler(message, lambda m: change_rate(m, bot, conn))

def change_rate(message, bot, conn):
    # Получаем новую скорость речи от пользователя
    rate = int(message.text)
    # Получаем текущий ID голоса пользователя
    voice_id = get_user_settings(conn, message.chat.id)[0]
    # Сохраняем новые настройки пользователя (голос и скорость)
    save_user_settings(conn, message.chat.id, voice_id, rate)
    # Подтверждаем изменение скорости пользователю
    bot.send_message(message.chat.id, f'Скорость голоса изменена на: {rate} слов в минуту.')

def voice_over(message, bot, voice, voices, conn):
    # Имя файла для сохранения озвученного текста
    voice_msg = 'v.mp3'
    # Получаем настройки голоса и скорости пользователя
    voice_id, rate = get_user_settings(conn, message.chat.id)
    if voice_id and rate:
        # Устанавливаем выбранный голос и скорость
        voice.setProperty('voice', voices[voice_id-1].id)
        voice.setProperty('rate', rate)

    # Сохраняем текст в аудиофайл
    voice.save_to_file(message.text, voice_msg)
    voice.runAndWait()  # Запускаем синтезатор речи

    # Отправляем пользователю озвученное сообщение
    with open(voice_msg, 'rb') as audio:
        bot.send_voice(message.chat.id, audio)

    # Удаляем временный аудиофайл
    os.remove(voice_msg)
