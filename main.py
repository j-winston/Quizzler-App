import data
from data import TriviaData
from quiz_brain import QuizBrain
from ui import QuizInterface

# default trivia parameters
initial_params = {
            "amount": 10,
            # category 9 is `any category`
            "category": 9,
            "difficulty": "easy",
            "type": "boolean"
        }
# fetches the initial trivia questions from open trivia api
trivia = TriviaData(initial_params)
# returns a list of shuffled `Question` objects, each object has question/answer
question_bank = trivia.generate_questions()
# performs answer checking, retrieving new questions, tracking number of questions
quiz = QuizBrain(question_bank)
# pass the brain to the quiz interface so gui elements can access it
quiz_ui = QuizInterface(quiz, data.PARAMS)








