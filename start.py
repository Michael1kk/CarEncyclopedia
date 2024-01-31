from tkinter import *
from tkinter import messagebox
import main


class Start(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Автоэнциклоппедия')
        self.geometry('600x250+470+300')
        self.resizable(False, False)

        self.menu = Menu(self)
        self.config(menu=self.menu)
        self.menu.add_command(label='Справка',
                              command=lambda: messagebox.showinfo(title='Справка',
                                                                  message='Это автоэнциклопедия, в которой находятся '
                                                                          'сведения о\nсамых знаковых автомобилях '
                                                                          'в истории компании.'))

        Label(self, text='Добро пожаловать в автоэнциклопедию!', font=('Times New Roman', 20, 'bold')).pack(pady=10)
        Button(self, text='Войти', font=('Times New Roman', 28, 'bold'), command=self.enter).pack(pady=20)

    def enter(self):
        self.destroy()
        main.Main().mainloop()


if __name__ == '__main__':
    app = Start()
    app.mainloop()
