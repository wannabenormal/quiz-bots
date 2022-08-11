from functools import partial
import random

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


def message_handler(bot, update, questions):
    response = update.message.text

    if response == 'Новый вопрос':
        question, _ = random.choice(list(questions.items()))

        update.message.reply_text(question)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    tg_token = env.str('TG_TOKEN')

    updater = Updater(tg_token)
    dp = updater.dispatcher

    questions = parse_questions()

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(
        Filters.text, partial(message_handler, questions=questions))
    )

    updater.start_polling()
    updater.idle()
