# Боты для викторин
Данный код написан исключительно в учебных целях.

## Подготовка:
У вас должен быть установлен `Python` 3 версии.

1. Склонировать репозиторий.
1. Создать бота в [Telegram](https://tlgrm.ru/docs/bots).
1. Создать группу VK и дать ей права на отправку сообщений и использование бота. Получить `API-ключ`.
1. Создать базу данных на [Redis](https://redis.com).
1. Создать в корне проекта `.env`-файл следующего содержимого:
```
export TG_TOKEN='<TELEGRAM TOKEN>'
export REDIS_HOST='<HOST REDIS>'
export REDIS_PORT='<REDIS POST>'
export REDIS_USER='<REDIS USERNAME>'
export REDIS_PASSWORD='<REDIS PASSWORD>'
export VK_TOKEN='<API-ключ VK>'
```
6. Установить зависимости:
```
pip install -r requirements.txt
```

## Telegram Bot
Для запуска телеграм-бота небходимо выполнить следующую команду:
```
python tg_bot.py
```

## VK Bot
Для запуска вк-бота необходимо выполнить следующую команду:
```
python vk_bot.py
```

## Добавление вопросов
Чтобы добавить больше вопросов, необходимо поместить в папку `questions` `txt`-файлы такой же структуры, как и демонстрационные.