from environs import Env
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup


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


def echo(bot, update):
    update.message.reply_text(update.message.text)


if __name__ == '__main__':
    env = Env()
    env.read_env()
    tg_token = env.str('TG_TOKEN')

    updater = Updater(tg_token)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(MessageHandler(Filters.text, echo))

    updater.start_polling()
    updater.idle()
