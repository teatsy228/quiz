import tkinter as tk
from tkinter import messagebox
import json
from utils import load_data, save_data
from quiz import QuizSelectionWindow

USER_DB = "users.json"

class AuthWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Авторизация")
        
        self.frame = tk.Frame(self.master)
        self.frame.pack(pady=20)
        
        self.user_listbox = tk.Listbox(self.frame, height=6)
        self.user_listbox.grid(row=0, column=0, columnspan=2, pady=5)
        self.load_users()
        
        tk.Label(self.frame, text="Пароль:").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.frame, show="*")
        self.password_entry.grid(row=1, column=1)
        
        self.login_button = tk.Button(self.frame, text="Войти", command=self.login)
        self.login_button.grid(row=2, column=0, columnspan=2, pady=5)
        
        self.register_button = tk.Button(self.frame, text="Регистрация", command=self.open_register_window)
        self.register_button.grid(row=3, column=0, columnspan=2)
    
    def load_users(self):
        self.user_listbox.delete(0, tk.END)
        users = load_data(USER_DB)
        for user in users:
            self.user_listbox.insert(tk.END, user["username"])
    
    def login(self):
        selected_index = self.user_listbox.curselection()
        if not selected_index:
            messagebox.showerror("Ошибка", "Выберите пользователя")
            return
        
        username = self.user_listbox.get(selected_index[0])
        password = self.password_entry.get()
        
        users = load_data(USER_DB)
        for user in users:
            if user["username"] == username and user["password"] == password:
                messagebox.showinfo("Успех", "Вход выполнен")
                self.master.destroy()
                root = tk.Tk()
                QuizSelectionWindow(root, username)
                return
        
        messagebox.showerror("Ошибка", "Неверный пароль")
    
    def open_register_window(self):
        register_window = tk.Toplevel(self.master)
        register_window.title("Регистрация")
        register_window.geometry("300x300")
        
        tk.Label(register_window, text="Логин:").pack(pady=5)
        username_entry = tk.Entry(register_window)
        username_entry.pack(pady=5)
        
        tk.Label(register_window, text="Пароль:").pack(pady=5)
        password_entry = tk.Entry(register_window, show="*")
        password_entry.pack(pady=5)
        
        def register():
            username = username_entry.get().strip()
            password = password_entry.get().strip()
            
            if not username or not password:
                messagebox.showerror("Ошибка", "Логин и пароль не должны быть пустыми")
                return
            
            users = load_data(USER_DB)
            if any(user["username"] == username for user in users):
                messagebox.showerror("Ошибка", "Логин занят")
                return
            
            new_user = {
                "username": username,
                "password": password
            }
            users.append(new_user)
            save_data(USER_DB, users)
            
            self.load_users()
            messagebox.showinfo("Успех", "Регистрация завершена")
            register_window.destroy()
        
        tk.Button(register_window, text="Зарегистрироваться", command=register).pack(pady=10)
