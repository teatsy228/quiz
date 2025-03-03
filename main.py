import tkinter as tk
from auth import AuthWindow

def main():
    root = tk.Tk()
    root.title("Викторина")
    root.geometry("400x300")
    
    AuthWindow(root)
    root.mainloop()

if __name__ == "__main__":
    main()
