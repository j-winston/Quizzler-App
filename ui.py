from tkinter import *
import data
import quiz_brain
from quiz_brain import QuizBrain
from data import TriviaData

THEME_COLOR = "#375362"
CANVAS_HEIGHT = 250
CANVAS_WIDTH = 300
QUESTION_FONT = ("Arial", "14", "italic")
SCORE_FONT = ("Arial", "14", "normal")


class QuizInterface:
    def __init__(self, quiz_brain:QuizBrain, params: data.PARAMS):
        # `params` holds category, difficulty, # of questions etc.
        self.params = params
        self.quiz = quiz_brain
        self.root = Tk()
        self.root.title("Quizzler App")
        self.root.config(bg=THEME_COLOR)
        self.canvas = Canvas( width=CANVAS_WIDTH, height=CANVAS_HEIGHT, background="white")
        self.canvas.grid(row=1, column=0, columnspan=2, padx=20, pady=20)

        self.true_button_img = PhotoImage(file="./images/true.png")
        self.true_button = Button(image=self.true_button_img, highlightthickness=0, command=self.input_true)
        self.true_button.grid(column=0, row=2, pady=20, padx=20)

        self.false_button_img = PhotoImage(file="./images/false.png")
        self.false_button = Button(image=self.false_button_img, highlightthickness=0, command=self.input_false)
        self.false_button.grid(column=1, row=2, pady=20, padx=20)

        self.question_text = self.canvas.create_text(150, 125, font=QUESTION_FONT, text="Put question here", width=200)

        self.score_canvas = Canvas(width=100, height=20, background=THEME_COLOR, highlightthickness=0)
        self.score_canvas.grid(column=1, row=0, padx=20, pady=20)
        self.score_text = self.score_canvas.create_text(50, 10, font=SCORE_FONT, text="Score: 0", fill="white")

        # ------------------MENU BAR SETUP---------------

        menubar = Menu(self.root)
        category = Menu(menubar, tearoff=0)
        category.add_command(label="Computer Science", command=lambda: self.select_category("Computer Science"))
        category.add_command(label="Film", command=lambda: self.select_category("Film"))
        category.add_command(label="Video Games", command=lambda: self.select_category("Video Games"))
        menubar.add_cascade(label="Category", menu=category)
        self.root.config(menu=menubar)

        self.get_next_question()

        self.root.mainloop()

    def get_next_question(self):
        # reset background color
        self.canvas.config(bg="white")
        qtext = self.quiz.next_question()
        self.canvas.itemconfig(self.question_text, text=qtext)

    def input_true(self):
        answer, score = self.quiz.check_answer("true")
        self.canvas.itemconfig(self.question_text, text=answer)
        self.score_canvas.itemconfig(self.score_text, text=f"Score:{self.quiz.score}")
        self.color_feedback(answer)

        if self.quiz.still_has_questions():
            after_id = self.canvas.after(1000, self.get_next_question)
        else:
            self.end_game()

    def color_feedback(self, answer: str):
        if answer == "You got it right!":
            self.canvas.config(bg="green")

        elif answer == "That's wrong.":
            self.canvas.config(bg="red")

    def input_false(self):
        answer, score = self.quiz.check_answer("false")
        self.canvas.itemconfig(self.question_text, text=answer)
        self.score_canvas.itemconfig(self.score_text, text=f"Score:{self.quiz.score}")
        self.color_feedback(answer)

        if self.quiz.still_has_questions():
            self.canvas.after(1000, self.get_next_question)
        else:
            self.end_game()

    def end_game(self):
        self.canvas.itemconfig(self.question_text, text="Woo hoo! You did it. No further questions.")
        self.false_button.config(state=DISABLED)
        self.true_button.config(state=DISABLED)
        self.canvas.config(bg="white")

    def select_category(self, category):
        if category == "Computer Science":
            self.params['category'] = 12
        elif category == "Film":
            self.params['category'] = 11
        elif category == "Video Games":
            self.params['category'] = 15
        else:
            print("ERROR: Category doesn't exist")

        self.reset_ui()

    def reset_ui(self):
        # generate a new list of questions based on category
        trivia_object = TriviaData(self.params)
        new_questions = trivia_object.generate_questions()
        # update our question list with new questions
        self.quiz.question_list = new_questions
        self.quiz.question_number = 0
        # refresh screen with new question
        self.get_next_question()
        # reset score
        self.reset_score()
        # reactivate buttons if need be
        self.false_button.config(state=ACTIVE)
        self.true_button.config(state=ACTIVE)

    def reset_score(self):
        self.quiz.score = 0
        self.score_canvas.itemconfig(self.score_text, text=f"Score:{self.quiz.score}")
