from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import pickle
import pymorphy3

f_types = [('Png Files', '*.png')]


class EditingCarPage(Toplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = self.model = self.filename = self.new_title = self.url = ''

        with open('links.pkl', 'rb') as file1, open('titles.pkl', 'rb') as file2, open('photos.pkl',
                                                                                              'rb') as file3:
            unpickler1 = pickle.Unpickler(file1)
            unpickler2 = pickle.Unpickler(file2)
            unpickler3 = pickle.Unpickler(file3)
            self.links = unpickler1.load()
            self.titles = unpickler2.load()
            self.photos = unpickler3.load()

        self.title('Редактирование статьи')
        self.geometry('700x800+420+0')
        self.resizable(False, False)

        Label(self, text='Введите название бренда, статью которого хотите отредактировать',
              font=('Times New Roman', 16, 'bold')).pack(pady=10)
        self.entry = Entry(self, justify=CENTER, width=60)
        self.entry.bind('<Return>', self.return_name)
        self.entry.pack(pady=5)

        Label(self, text='Введите название модели автомобиля', font=('Times New Roman', 16, 'bold')).pack(pady=10)
        self.model_entry = Entry(self, justify=CENTER, width=60)
        self.model_entry.bind('<Return>', self.add_model)
        self.model_entry.pack(pady=5)

        Label(self, text='Введите заголовок страницы, в которой обозревается автомобиль',
              font=('Times New Roman', 16, 'bold')).pack(pady=10)
        self.title_entry = Entry(self, justify=CENTER, width=60)
        self.title_entry.bind('<Return>', self.add_title)
        self.title_entry.pack(pady=5)

        Label(self, text='Вставьте гиперссылку на статью, в которой обозревается автомобиль',
              font=('Times New Roman', 16, 'bold')).pack(pady=10)
        self.url_entry = Entry(self, justify=CENTER, width=90)
        self.url_entry.bind('<Return>', self.add_url)
        self.url_entry.pack(pady=5)

        Label(self, text='Загрузите фотографию автомобиля', font=('Times New Roman', 16, 'bold')).pack(pady=10)
        Button(self, text='Загрузить фото', font=('Times New Roman', 14), command=self.add_photo).pack()

        Button(self, text='Cоздать страницу автомобиля', font=('Times New Roman', 24, 'bold'),
               command=self.combine).pack(side=BOTTOM, pady=30)

    def return_name(self, event=None):
        self.name = self.entry.get().lower()
        if self.name in self.photos.keys():
            messagebox.showinfo(message='Такое название есть в списках, продолжайте!')
            self.lift()
        else:
            messagebox.showerror(message='Такой бренд не был найден!\n'
                                         'Сначала добавьте его, чтобы редактировать его статью')
            self.destroy()

    def add_model(self, event=None):
        if self.name == '':
            messagebox.showerror(title='Ошибка', message='Сначала введите название бренда!')
            self.model_entry.delete(0, END)
        else:
            self.model = ''.join([f'{word.upper()} ' if len(word) <= 3 else f'{word.title()} ' for word in
                                  self.model_entry.get().lower().split(' ')]).strip()
            if f'Logos\\{self.model}.png'.lower() in [path.lower() for path in self.photos.get(self.name)[1:]]:
                messagebox.showerror(message='Такая модель уже есть!\nПожалуйста, введите другую')
                self.model_entry.delete(0, END)
            elif self.model.lower() == self.name:
                messagebox.showerror(message='Название модели и бренда не должно быть одинаковым!')
                self.model_entry.delete(0, END)
            else:
                messagebox.showinfo(message='Название модели успешно сохранено!')
        self.lift()

    def add_title(self, event=None):
        self.new_title = self.title_entry.get().lower()
        if self.model == '':
            messagebox.showerror(title='Ошибка', message='Введите название модели!')
            self.title_entry.delete(0, END)
        elif self.new_title in self.titles:
            messagebox.showerror(message='Такой заголовок уже используется!\nВведите, пожалуйста, другой')
            self.title_entry.delete(0, END)
        else:
            messagebox.showinfo(message='Новый заголовок успешно сохранён!')
        self.lift()

    def add_url(self, event=None):
        self.url = self.url_entry.get()
        if self.model == '':
            messagebox.showerror(title='Ошибка', message='Введите название модели!')
            self.url_entry.delete(0, END)
        elif 'https://' not in self.url:
            messagebox.showerror(message='Вставьте ссылку, а не обычный текст!')
            self.url_entry.delete(0, END)
        elif r''.join(self.url) in self.links.get(self.name):
            messagebox.showerror(message='Такая ссылка уже есть!\nВставьте, пожалуйста, другую')
            self.url_entry.delete(0, END)
        else:
            messagebox.showinfo(message='Ссылка на статью успешно сохранена')
        self.lift()

    def add_photo(self, event=None):
        if self.model == '':
            messagebox.showerror(title='Ошибка', message='Сначала введите название модели!')
            self.lift()
        else:
            self.filename = askopenfilename(filetypes=f_types)
            img = Image.open(self.filename)

            divider = 0
            for i in range(1, 100):
                if img.size[0] // i <= 500 and img.size[1] // i <= 400:
                    divider = i
                    break

            img_resized = img.resize((img.size[0] // divider, img.size[1] // divider))
            img_resized.save(f'Logos\\{self.model}.png', quality=100)
            img = ImageTk.PhotoImage(img_resized, master=self)
            image = Label(self, image=img, justify=CENTER)
            image.image = img
            image.pack(pady=30)
            messagebox.showinfo(title='Сохранение', message='Эмблема бренда успешно загружена!')
            self.lift()

    def combine(self, event=None):
        if self.model == '' or self.filename == '' or self.new_title == '' or self.url == '':
            messagebox.showerror(title='Ошибка', message='Сначала введите все необходимые данные!!')
        else:
            self.photos.get(self.name).append(f'Logos\\{self.model}.png')
            self.titles.get(self.name).append(self.new_title)
            self.links.get(self.name).append(r''.join(self.url))
            
            with open('links.pkl', 'wb') as f1, open('titles.pkl', 'wb') as f2, open('photos.pkl', 'wb') as f3:
                pickle.dump(self.photos, f3)
                pickle.dump(self.links, f1)
                pickle.dump(self.titles, f2)

            messagebox.showinfo(title='Добавление страницы',
                                message='Все данные сохранены.\nПерезапустите приложение, чтобы увидеть изменения!')
            exit()


class AddingCarPage(Toplevel):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.model = self.url = self.filename = ''
        self.image = Label()
        self.count = 0

        with open('links.pkl', 'rb') as file1, open('titles.pkl', 'rb') as file2, open('photos.pkl',
                                                                                              'rb') as file3:
            unpickler1 = pickle.Unpickler(file1)
            unpickler2 = pickle.Unpickler(file2)
            unpickler3 = pickle.Unpickler(file3)
            self.links = unpickler1.load()
            self.titles = unpickler2.load()
            self.photos = unpickler3.load()

        self.title('Создание автомобильной статьи')
        self.geometry('700x600+420+100')
        self.resizable(False, False)

        self.txt = Label(self, text=f'Введите название самого {self.correct_word()} автомобиля',
                         font=('Times New Roman', 20, 'bold'))
        self.txt.pack(pady=10)
        self.model_entry = Entry(self, justify=CENTER, width=60)
        self.model_entry.bind('<Return>', self.add_model)
        self.model_entry.pack(pady=5)

        Label(self, text='Вставьте гиперссылку на статью, в которой обозревается автомобиль',
              font=('Times New Roman', 16, 'bold')).pack(pady=10)
        self.url_entry = Entry(self, justify=CENTER, width=90)
        self.url_entry.bind('<Return>', self.add_url)
        self.url_entry.pack(pady=5)

        Label(self, text='Загрузите фотографию автомобиля', font=('Times New Roman', 16, 'bold')).pack(pady=10)
        Button(self, text='Загрузить фото', font=('Times New Roman', 14), command=self.add_photo).pack()

        Button(self, text='Cоздать страницу автомобиля', font=('Times New Roman', 24, 'bold'),
               command=self.combine).pack(side=BOTTOM, pady=30)

    def add_model(self, event=None):
        self.model = ''.join([f'{word.upper()} ' if len(word) <= 3 else f'{word.title()} ' for word in
                              self.model_entry.get().lower().split(' ')]).strip()
        if self.model.lower() == self.name:
            messagebox.showerror(message='Название модели и бренда не должно быть одинаковым!')
            self.model_entry.delete(0, END)
        else:
            messagebox.showinfo(message='Название модели успешно сохранено!')
        self.lift()

    def add_url(self, event=None):
        self.url = self.url_entry.get()
        if self.model == '':
            messagebox.showerror(title='Ошибка', message='Введите название модели!')
            self.url_entry.delete(0, END)
        elif 'https://' not in self.url:
            messagebox.showerror(message='Вставьте ссылку, а не обычный текст!')
            self.url_entry.delete(0, END)
        else:
            messagebox.showinfo(message='Ссылка на статью успешно сохранена')
        self.lift()

    def add_photo(self, event=None):
        if self.model == '':
            messagebox.showerror(title='Ошибка', message='Сначала введите название модели!')
            self.lift()
        else:
            self.filename = askopenfilename(filetypes=f_types)
            img = Image.open(self.filename)

            divider = 0
            for i in range(1, 100):
                if img.size[0] // i <= 500 and img.size[1] // i <= 400:
                    divider = i
                    break

            img_resized = img.resize((img.size[0] // divider, img.size[1] // divider))
            img_resized.save(f'Logos\\{self.model}.png', quality=100)
            img = ImageTk.PhotoImage(img_resized, master=self)
            self.image = Label(self, image=img, justify=CENTER)
            self.image.image = img
            self.image.pack(pady=30)
            messagebox.showinfo(title='Сохранение', message='Эмблема бренда успешно загружена!')
            self.lift()

    def combine(self, event=None):
        if self.model == '' or self.filename == '' or self.url == '':
            messagebox.showerror(title='Ошибка', message='Сначала введите все необходимые данные!!')
        else:
            self.photos.get(self.name).append(f'Logos\\{self.model}.png')
            self.links.get(self.name).append(r''.join(self.url))
            self.model = self.url = self.filename = ''
            self.model_entry.delete(0, END)
            self.url_entry.delete(0, END)
            self.image.destroy()
            self.count += 1

            if self.count == 5:
                with open('links.pkl', 'wb') as f1, open('photos.pkl', 'wb') as f2:
                    pickle.dump(self.photos, f2)
                    pickle.dump(self.links, f1)

                messagebox.showinfo(title='Добавление статьи',
                                    message='Все данные сохранены.\nПерезапустите приложение, чтобы увидеть изменения!')
                exit()

            self.txt.config(text=f'Введите название самого {self.correct_word()} автомобиля')

    def correct_word(self):
        word = ''
        for choice in pymorphy3.MorphAnalyzer().parse(self.titles.get(self.name)):
            if choice.tag.gender == 'masc' and choice.tag.POS == 'ADJF':
                word = choice.inflect({'gent'})
                break
        return word.word
