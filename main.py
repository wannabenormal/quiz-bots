import re

if __name__ == '__main__':
    with open('questions/aaron17.txt', 'r', encoding='KOI8-R') as file:
        file_content = file.read()
        blocks = file_content.split('\n\n')
        question_regex = re.compile(r'^(Вопрос [\d]:)')
        answer_regex = re.compile(r'^(Ответ:)')

        questions = {}

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

        print(questions)
