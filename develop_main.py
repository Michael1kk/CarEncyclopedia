from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import develop_car_page
import pickle
import os


class Adding(Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = ''
        self.filename = ''

        self.title('Добавить автомобильный бренд')
        self.geometry('600x600+460+100')
        self.resizable(False, False)

        Label(self, text='Введите название бренда', font=('Times New Roman', 20, 'bold')).pack(pady=10)
        self.entry = Entry(self, justify=CENTER, width=60)
        self.entry.bind('<Return>', self.add_name)
        self.entry.pack(pady=10)

        Label(self, text='Загрузите эмблему бренда', font=('Times New Roman', 20, 'bold')).pack(pady=15)
        Button(self, text='Загрузить фото', font=('Times New Roman', 14), command=self.add_photo).pack()

        Button(self, text='Cоздать статью бренда', font=('Times New Roman', 24, 'bold'),
               command=self.combine).pack(side=BOTTOM, pady=30)

    def add_name(self, event=None):
        self.name = self.entry.get().lower()
        if not self.name.isalpha():
            messagebox.showerror(title='Ошибка', message='Название не должно состоять из цифр и других символов\n'
                                                         'Введите правильное название!!')
            self.entry.delete(0, END)
        else:
            messagebox.showinfo(message='Название бренда успешно сохранено!')
            self.lift()

    def add_photo(self, event=None):
        if self.name == '':
            messagebox.showerror(title='Ошибка', message='Сначала введите название бренда!!')
            self.entry.delete(0, END)
        else:
            f_types = [('Png Files', '*.png')]
            self.filename = askopenfilename(filetypes=f_types)
            self.lift()
            img = Image.open(self.filename)

            divider = 0
            for i in range(1, 100):
                if img.size[0] // i <= 200 and img.size[1] // i <= 200:
                    divider = i
                    break

            img_resized = img.resize((img.size[0] // divider, img.size[1] // divider))
            img_resized.save(f'Logos\\{self.name}.png', quality=100)
            img = ImageTk.PhotoImage(img_resized, master=self)
            image = Label(self, image=img, justify=CENTER)
            image.image = img
            image.pack(pady=30)
            messagebox.showinfo(title='Сохранение', message='Эмблема бренда успешно загружена!')
            self.lift()

    def combine(self, event=None):
        if self.name == '' or self.filename == '':
            messagebox.showerror(title='Ошибка', message='Сначала введите все необходимые данные!!')
        else:
            if os.path.getsize('photos.pkl') > 0:
                with open('photos.pkl', 'rb') as file1, open('links.pkl', 'rb') as file2:
                    unpickler1 = pickle.Unpickler(file1)
                    unpickler2 = pickle.Unpickler(file2)
                    ph = unpickler1.load()
                    url = unpickler2.load()
            else:
                messagebox.showerror(message='Произошла какая-то ошибка.\nПопробуйте ещё раз')

            ph.setdefault(self.name, []).insert(0, f'Logos\\{self.name}.png')
            url.setdefault(self.name, [])
            with open('photos.pkl', 'wb') as file1, open('links.pkl', 'wb') as file2:
                pickle.dump(ph, file1)
                pickle.dump(url, file2)
            messagebox.showinfo(title='Создание бренда', message='Все данные сохранены!\nПерейдём к созданию статьи')
            self.destroy()
            develop_car_page.AddingCarPage(self.name).mainloop()
