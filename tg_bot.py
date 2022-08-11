from functools import partial
import random

import redis
from environs import Env
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup

from parse_questions import parse_questions


def start(bot, update):
    keyboard = [
        [
            'Новый вопрос',
            'Сдаться'
        ],
        [
            'Мой счет'
        ]
    ]
    bot.send_message(
        chat_id=update.effective_chat.id,
        text='Привет! Я бот для викторин!',
        reply_markup=ReplyKeyboardMarkup(keyboard)

    )


def message_handler(bot, update, questions, db_connection):
    response = update.message.text

    if response == 'Новый вопрос':
        question, _ = random.choice(list(questions.items()))
        db_connection.set(update.effective_chat.id, question)
        update.message.reply_text(question)
    else:
        print(db_connection.get(update.effective_chat.id))


if __name__ == '__main__':
    env = Env()
    env.read_env()
    tg_token = env.str('TG_TOKEN')
    redis_host = env.str('REDIS_HOST')
    redis_port = env.str('REDIS_PORT')
    redis_user = env.str('REDIS_USER')
    redis_password = env.str('REDIS_PASSWORD')

    redis_connection = redis.Redis(
        host=redis_host,
        port=redis_port,
        username=redis_user,
        password=redis_password,
        decode_responses=True
    )

    updater = Updater(tg_token)
    dp = updater.dispatcher

    questions = parse_questions()

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(
        Filters.text, partial(
            message_handler,
            questions=questions,
            db_connection=redis_connection
        ))
    )

    updater.start_polling()
    updater.idle()
