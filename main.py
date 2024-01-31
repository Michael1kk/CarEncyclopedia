from tkinter import *
from tkinter import messagebox
import develop_car_page
import searching
from car_page import cars
import develop_main
import pickle


class Main(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        x = y = 0
        count = 1
        buttons = []

        self.title('Автоэнциклопедия')
        self.geometry('833x450+350+150')
        self.resizable(False, False)

        self.scrollbar = Scrollbar(self, orient='vertical')
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.c = Canvas(self, scrollregion=(0, 0, 5000, 5000), width=5000, height=5000,
                        yscrollcommand=self.scrollbar.set)
        self.scrollbar['command'] = self.c
        self.c.bind_all('<MouseWheel>', self.mouse)
        self.c.pack()

        self.main_menu = Menu(self)
        self.config(menu=self.main_menu)
        self.main_menu.add_command(label='Поиск', command=searching.search)
        self.main_menu.add_command(label='Режим разработчика', command=lambda z=3: self.enter_develop(z))

        with open('photos.pkl', 'rb') as file:
            unpickler = pickle.Unpickler(file)
            photos = unpickler.load()

        for name in sorted(photos.keys()):
            self.car = PhotoImage(file=photos[name][0])
            self.button = Button(width=270, height=160, text=name.title() if len(name) > 3 else name.upper(),
                                 image=self.car, compound=TOP, bd=0)
            self.button.image = self.car
            self.c.create_window(x, y, anchor=NW, window=self.button)
            buttons.append(self.button)
            x += 270
            if count % 3 == 0:
                x = 0
                y += 166
            count += 1

        for i in range(len(photos.keys())):
            buttons[i]['command'] = lambda z=[*sorted(photos)][i]: cars(z)

    def mouse(self, event):
        self.c.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def enter_develop(self, count):
        def get_text(attempts):
            password = entry_field.get()
            if password == 'Zss_l1KK':
                messagebox.showinfo(title='Вход в режим разработчика',
                                    message='Поздравляю, вы вошли в режим разработчика!\n'
                                            'Теперь вы можете редактировать автоэнциклопедию как\nвам захочется')
                enter.destroy()
                self.title('Режим разработчика')
                self.main_menu.delete(2)
                self.develop_menu = Menu(self.main_menu, tearoff=0)
                self.develop_menu.add_command(label='Добавить автомобильный бренд',
                                              command=lambda: develop_main.Adding().mainloop())
                self.develop_menu.add_command(label='Редактировать статью бренда',
                                              command=lambda: develop_car_page.EditingCarPage().mainloop())
                self.main_menu.add_cascade(label='Режим разработчика',
                                           menu=self.develop_menu)
            else:
                attempts -= 1
                if attempts == 2:
                    messagebox.showerror(message='Неверный пароль!!\nОсталось 2 попытки')
                    enter.destroy()
                    self.enter_develop(attempts)
                elif attempts == 1:
                    messagebox.showerror(message='Неверный пароль!!\nОсталась 1 попытка')
                    enter.destroy()
                    self.enter_develop(attempts)
                elif attempts == 0:
                    messagebox.showerror(message='Неверный пароль!!\nОсталось 0 попыток!')
                    messagebox.showerror(title='Вход в режим разработчика',
                                         message='У вас не осталось попыток ввода пароля!\n'
                                                 'К сожлаению, вы не смогли доказать, что вы разработчик((')
                    enter.destroy()
                    self.main_menu.delete(2)
                    self.main_menu.add_command(label=' ', state='disabled')

        enter = Toplevel()
        enter.title('Ввод пароля')
        enter.geometry('320x150+600+300')
        enter.resizable(False, False)

        Label(enter, text='Введите пароль', font=('Times New Roman', 20, 'bold')).pack(pady=15)
        entry_field = Entry(enter, justify=CENTER, show='*')
        entry_field.pack()
        entry_field.bind('<Return>', lambda event: get_text(count))
        numbers = Label(enter, text=f'У вас осталось {count} попытки' if count > 1 else f'У вас осталась 1 попытка',
                        font=('Times New Roman', 14))
        numbers.pack(side=BOTTOM)

        enter.mainloop()
