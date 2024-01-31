from tkinter import *
import webbrowser
import pickle


def cars(name):
    global count
    count = 0

    def callback(event=None):
        global count
        webbrowser.open_new(links[name.lower()][count])

    with open('links.pkl', 'rb') as file1, open('titles.pkl', 'rb') as file2, open('photos.pkl', 'rb') as file3:
        unpickler1 = pickle.Unpickler(file1)
        unpickler2 = pickle.Unpickler(file2)
        unpickler3 = pickle.Unpickler(file3)
        links = unpickler1.load()
        titles = unpickler2.load()
        photos = unpickler3.load()

    article = Toplevel()
    article.title(name.title() if len(name) > 3 else name.upper())
    article.geometry('800x500')
    article.resizable(False, False)

    headline = Label(article, text=f'Самый {titles.get(name)[count]} автомобиль',
                     font=('Times New Roman', 30, 'bold'))
    headline.pack()

    def left():
        global count
        if count == 0:
            return
        else:
            count -= 1
            headline['text'] = f'Самый {titles,get(name)[count]} автомобиль'
            model['text'] = f'{name.upper() if len(name) == 3 else name.title()}\n' \
                            f'{photos.get(name.lower())[count + 1][6:-4]}'
            car.configure(image='')
            ph = PhotoImage(file=photos.get(name.lower())[count + 1])
            car.configure(image=ph)
            car.image = ph

    def right():
        global count
        if count == len(photos.get(name)[1:]) - 1:
            return
        else:
            count += 1
            headline['text'] = f'Самый {titles.get(name)[count]} автомобиль'
            model['text'] = f'{name.upper() if len(name) == 3 else name.title()}\n' \
                            f'{photos.get(name.lower())[count + 1][6:-4]}'
            car.configure(image='')
            ph = PhotoImage(file=photos.get(name.lower())[count + 1])
            car.configure(image=ph)
            car.image = ph

    left_arrow = Button(article, text='<', font=('Times New Roman', 20), bd=0, command=left)
    left_arrow.pack(side=LEFT)

    photo = PhotoImage(file=photos.get(name.lower())[count + 1])
    car = Label(article, image=photo)
    car.pack(side=LEFT, padx=30)

    right_arrow = Button(article, text='>', font=('Times New Roman', 20), bd=0, command=right)
    right_arrow.pack(side=RIGHT)

    model = Label(article, font=('Times New Roman', 28, 'bold'),
                  text=f'{name.upper() if len(name) == 3 else name.title()}\n'
                       f'{photos.get(name.lower())[count + 1][6:-4]}')
    model.bind('<Button-1>', callback)
    model.pack(pady=150)

    article.mainloop()
