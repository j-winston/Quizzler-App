import random

import requests
from question_model import Question
from random import shuffle

PARAMS = {
    "amount": 10,
    # category 9 is `any category`
    "category": 9,
    "difficulty": "easy",
    "type": "boolean"
}

trivia_data = requests.get(url="https://opentdb.com/api.php", params=PARAMS)
question_data = trivia_data.json()["results"]


class TriviaData:
    def __init__(self, params):
        self.params = params

        self.trivia_data = requests.get(url="https://opentdb.com/api.php", params=self.params)
        self.question_data = self.trivia_data.json()["results"]
        self.question_bank = []

    def generate_questions(self):
        question_bank = []
        for question in self.question_data:
            question_text = question["question"]
            question_answer = question["correct_answer"]
            new_question = Question(question_text, question_answer)
            question_bank.append(new_question)

        random.shuffle(question_bank)
        return question_bank

