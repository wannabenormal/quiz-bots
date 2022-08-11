import re
import os


def parse_questions():
    questions = {}

    for filename in os.listdir('questions'):
        if not filename.endswith('.txt'):
            continue

        with open(
            os.path.join('questions', filename), 'r', encoding='KOI8-R'
        ) as file:
            file_content = file.read()

        blocks = file_content.split('\n\n')
        question_regex = re.compile(r'^(Вопрос [\d]+:)')
        answer_regex = re.compile(r'^(Ответ:)')

        question = ''
        answer = ''

        for block in blocks:
            is_question = question_regex.match(block)
            is_answer = answer_regex.match(block)

            if is_question:
                question = question_regex.split(block.replace('\n', ' '))[2]

            if is_answer:
                answer = answer_regex.split(block.replace('\n', ' '))[2]

            if question and answer:
                questions[question] = answer

                question = answer = ''

    return questions
