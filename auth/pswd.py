import tkinter as tk
from tkinter import messagebox

def ask_password():
    result = {'flag': None}

    def on_enter_key_press(event=None):
        PASSWORD = 'sam1409'
        pswd = text_box.get()
        if PASSWORD == pswd:
            result['flag'] = 1
            root.destroy()
        else:
            messagebox.showerror("Error", "Incorrect password")
            result['flag'] = 0
            root.destroy()

    root = tk.Tk()
    root.attributes('-topmost', True)
    root.attributes('-topmost', False)
    root.title("Authentication Window")
    root.geometry("300x300+550+200")
    root['bg'] = "#A7D9F2"
    root.minsize(300, 300)
    root.maxsize(300, 300)

    photo = tk.PhotoImage(file="speechDetector\\auth\\img.png")
    img = tk.Label(root, image=photo)
    img.place(width=300, height=250)

    text_box = tk.Entry(root, show='*')
    text_box.pack(anchor='center', pady=20, ipadx=20, ipady=2, side="bottom")

    text = tk.Label(root, text="Enter the password", justify="center", font=20, background="#A7D9F2")
    text.pack(anchor="center", side="bottom")

    text_box.focus_set()
    text_box.bind("<Return>", on_enter_key_press)

    root.mainloop()
    return result['flag']

if __name__ == '__main__':
    print(ask_password())