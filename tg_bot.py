from enum import Enum, auto
from functools import partial
import random

import redis
from environs import Env
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler
)
from telegram import ReplyKeyboardMarkup

from parse_questions import parse_questions


class QuizSteps(Enum):
    waiting = auto()
    question = auto()
    answer = auto()


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

    return QuizSteps.waiting


def handle_solution_attempt(bot, update, questions, db_connection):
    answer = questions.get(
        db_connection.get(update.effective_chat.id)
    ).split('.')[0].split('(')[0].strip()
    user_answer = update.message.text.strip()

    if answer == user_answer:
        update.message.reply_text(
            'Правильно! Для нового вопроса нажми кнопку "Новый вопрос"'
        )

        return QuizSteps.waiting
    else:
        update.message.reply_text('Неправильно... Попробуешь еще раз?')

    return QuizSteps.answer


def handle_new_question_handler(bot, update, questions, db_connection):
    question, _ = random.choice(list(questions.items()))
    db_connection.set(update.effective_chat.id, question)
    update.message.reply_text(question)

    return QuizSteps.answer


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

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('start', start),
            MessageHandler(
                Filters.regex(r'^(Новый вопрос)$'),
                partial(
                    handle_new_question_handler,
                    questions=questions,
                    db_connection=redis_connection
                )
            )
        ],
        states={
            QuizSteps.waiting: [
                MessageHandler(
                    Filters.regex(r'^(Новый вопрос)$'),
                    partial(
                        handle_new_question_handler,
                        questions=questions,
                        db_connection=redis_connection
                    )
                )
            ],
            QuizSteps.question: [
                MessageHandler(
                    Filters.regex(r'^(Новый вопрос)$'),
                    partial(
                        handle_new_question_handler,
                        questions=questions,
                        db_connection=redis_connection
                    )
                )
            ],
            QuizSteps.answer: [
                MessageHandler(
                    Filters.text, partial(
                        handle_solution_attempt,
                        questions=questions,
                        db_connection=redis_connection
                    )
                )
            ]
        },
        fallbacks=[]
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()
