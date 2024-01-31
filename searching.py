from tkinter import *
from tkinter import messagebox
from car_page import cars
import pickle


def search():
    def get_text():
        text = entry.get().lower()
        if text.lower() in photos.keys():
            input_field.destroy()
            cars(text)
        else:
            messagebox.showerror(title='Ошибка!!', message='По вашему запросу автомобиль не был найден!')
            input_field.destroy()
            search()

    input_field = Toplevel()
    input_field.title('Поиск')
    input_field.geometry('300x100+600+300')
    input_field.resizable(False, False)

    Label(input_field, text='Введите название автомобиля', font=('Times New Roman', 14)).pack()

    entry = Entry(input_field, justify=CENTER)
    entry.pack(anchor=N, padx=10, pady=10)
    entry.bind('<Return>', lambda event: get_text())

    with open('photos.pkl', 'rb') as file:
        unpickler = pickle.Unpickler(file)
        photos = unpickler.load()

    input_field.mainloop()
