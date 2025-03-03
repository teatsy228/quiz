import tkinter as tk
import random
import json
from tkinter import messagebox
from utils import load_data, save_data

QUIZ_DB = "quizzes.json"
RESULTS_DB = "results.json"

class QuizSelectionWindow:
    def __init__(self, master, username):
        self.master = master
        self.username = username
        self.master.title("Выбор викторины")
        self.master.geometry("400x300")

        self.label = tk.Label(self.master, text="Выберите викторину:")
        self.label.pack(pady=10)

        self.quiz_listbox = tk.Listbox(self.master)
        self.quiz_listbox.pack(pady=10)

        self.start_button = tk.Button(self.master, text="Начать", command=self.start_quiz)
        self.start_button.pack(pady=10)

        self.load_quizzes()

    def load_quizzes(self):
        quizzes = load_data(QUIZ_DB)
        for quiz in quizzes:
            self.quiz_listbox.insert(tk.END, quiz["title"])

    def start_quiz(self):
        selection = self.quiz_listbox.curselection()
        if not selection:
            messagebox.showerror("Ошибка", "Выберите викторину")
            return

        index = selection[0]
        quizzes = load_data(QUIZ_DB)
        selected_quiz = quizzes[index]

        self.master.destroy()
        root = tk.Tk()
        QuizWindow(root, self.username, selected_quiz)

class QuizWindow:
    def __init__(self, master, username, quiz):
        self.master = master
        self.username = username
        self.quiz = quiz
        self.master.title(self.quiz["title"])
        self.master.geometry("400x300")

        self.current_question = 0
        self.score = 0
        self.answers = []

        self.question_label = tk.Label(self.master, text="")
        self.question_label.pack(pady=10)

        self.options_vars = []
        self.options_checkbuttons = []
        for _ in range(4):
            var = tk.IntVar()
            cb = tk.Checkbutton(self.master, variable=var)
            cb.pack(anchor="w")
            self.options_vars.append(var)
            self.options_checkbuttons.append(cb)

        self.next_button = tk.Button(self.master, text="Следующий", command=self.next_question)
        self.next_button.pack(pady=10)

        self.load_question()

    def load_question(self):
        if self.current_question >= len(self.quiz["questions"]):
            self.finish_quiz()
            return

        question = self.quiz["questions"][self.current_question]
        self.question_label.config(text=question["text"])

        for i, option in enumerate(question["options"]):
            self.options_checkbuttons[i].config(text=option, state="normal")
            self.options_vars[i].set(0)

    def next_question(self):
        question = self.quiz["questions"][self.current_question]
        selected_answers = [i for i, var in enumerate(self.options_vars) if var.get()]

        if selected_answers == question["correct_answers"]:
            self.score += 1

        self.current_question += 1
        self.load_question()

    def finish_quiz(self):
        messagebox.showinfo("Результат", f"Ваш результат: {self.score}/20")
        results = load_data(RESULTS_DB)
        results.append({"username": self.username, "quiz_id": self.quiz["quiz_id"], "score": self.score})
        save_data(RESULTS_DB, results)
        self.master.destroy()
