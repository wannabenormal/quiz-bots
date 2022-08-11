import random

from environs import Env
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import redis

from parse_questions import parse_questions


def new_question_handler(event, vk_api, questions, keyboard, db_connection):
    question, _ = random.choice(list(questions.items()))
    db_connection.set(event.user_id, question)

    vk_api.messages.send(
        user_id=event.user_id,
        message=question,
        random_id=random.randint(1, 1000),
        keyboard=keyboard.get_keyboard()
    )


def user_message_handler(event, vk_api, questions, keyboard, db_connection):
    question = db_connection.get(event.user_id)

    if not question:
        vk_api.messages.send(
            user_id=event.user_id,
            message='Привет! Я бот для викторин!',
            random_id=random.randint(1, 1000),
            keyboard=keyboard.get_keyboard()
        )

        return

    answer = questions.get(question).split('.')[0].split('(')[0].strip()
    user_answer = event.text.strip()

    if answer == user_answer:
        vk_api.messages.send(
            user_id=event.user_id,
            message='Правильно!',
            random_id=random.randint(1, 1000),
            keyboard=keyboard.get_keyboard()
        )
    else:
        vk_api.messages.send(
            user_id=event.user_id,
            message='Неверно... Попробуешь еще раз?',
            random_id=random.randint(1, 1000),
            keyboard=keyboard.get_keyboard()
        )


def giveup_handler(event, vk_api, questions, keyboard, db_connection):
    question = db_connection.get(event.user_id)
    answer = questions.get(question).split('.')[0].split('(')[0].strip()

    vk_api.messages.send(
        user_id=event.user_id,
        message=f'Правильный ответ: {answer}',
        random_id=random.randint(1, 1000),
        keyboard=keyboard.get_keyboard()
    )

    new_question_handler(event, vk_api, questions, keyboard, db_connection)


if __name__ == "__main__":
    env = Env()
    env.read_env()
    vk_token = env.str('VK_TOKEN')

    questions = parse_questions()

    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

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

    keyboard = VkKeyboard()
    keyboard.add_button('Новый вопрос')
    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.text == 'Новый вопрос' or event.text == 'Начать':
                new_question_handler(event, vk_api, questions, keyboard, redis_connection)
            elif event.text == 'Сдаться':
                giveup_handler(event, vk_api, questions, keyboard, redis_connection)
            else:
                user_message_handler(event, vk_api, questions, keyboard, redis_connection)
