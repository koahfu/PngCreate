import tkinter as tk
from tkinter import colorchooser, filedialog
import PIL.Image
import PIL.ImageTk
from PIL import ImageGrab  
from PIL import ImageSequence

class DrawingApp:
    def __init__(self, master):
        self.master = master
        master.title("PngCreate v1.1 beta")

        # Размер холста для рисования
        self.canvas_width = 600
        self.canvas_height = 400
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg="white")

        # Начальные настройки
        self.frame = tk.Frame(master)
        self.color = "black"
        self.brush_size = 5
        self.is_drawing = False
        self.x1, self.y1 = None, None
        self.frames = [self.canvas]  # Список для хранения кадров
        self.current_frame = 0  # Индекс текущего кадра

        # Кнопки инструментов
        self.color_button = tk.Button(master, text="Цвет", command=self.choose_color)
        self.color_button.pack(side="left")

        self.brush_size_button = tk.Button(master, text="Размер кисти", command=self.change_brush_size)
        self.brush_size_button.pack(side="left")

        self.eraser_button = tk.Button(master, text="Ластик", command=self.use_eraser)
        self.eraser_button.pack(side="left")

        self.save_button = tk.Button(master, text="Сохранить", command=self.save_image)
        self.save_button.pack(side="left")

        self.open_button = tk.Button(master, text="Открыть", command=self.open_image)
        self.open_button.pack(side="left")

        self.new_frame_button = tk.Button(master, text="Новая картинка", command=self.new_frame)
        self.new_frame_button.pack(side="left")

        self.delete_frame_button = tk.Button(master, text="Удалить картинку", command=self.delete_frame)
        self.delete_frame_button.pack(side="left")

        # Кнопки переключения кадров
        self.prev_frame_button = tk.Button(master, text="<<", command=self.prev_frame)
        self.prev_frame_button.pack(side="left")

        self.next_frame_button = tk.Button(master, text=">>", command=self.next_frame)
        self.next_frame_button.pack(side="left")

        # Связываем события мыши с функциями рисования
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)
        self.canvas.bind("<Button-1>", self.start_drawing)

    # Функция выбора цвета
    def choose_color(self):
        color = colorchooser.askcolor(title="Выбор цвета")[1]
        if color:
            self.color = color

    # Функция изменения размера кисти
    def change_brush_size(self):
        new_size = int(tk.simpledialog.askstring("Размер кисти", "Введите размер кисти:", initialvalue=str(self.brush_size)))
        if new_size > 0:
            self.brush_size = new_size

    # Функция использования ластика
    def use_eraser(self):
        self.color = "white"

    # Функция рисования
    def draw(self, event):
        if self.is_drawing:
            self.x2, self.y2 = event.x, event.y
            event.widget.create_line(self.x1, self.y1, self.x2, self.y2, width=self.brush_size, fill=self.color, capstyle="round")
            self.x1, self.y1 = self.x2, self.y2

    # Функция начала рисования
    def start_drawing(self, event):
        self.is_drawing = True
        self.x1, self.y1 = event.x, event.y

    # Функция окончания рисования
    def stop_drawing(self, event):
        self.is_drawing = False

    # Функция сохранения изображения
    # Функция сохранения изображения
    def save_image(self):
        filename = filedialog.asksaveasfilename(defaultextension=".png")
        if filename:
            if len(self.frames) > 1:
                # Сохранение в формате GIF (НЕ РАБОТАЕТ!)
                frames = []
                for frame in self.frames:
                    # Получаем изображение из холста с помощью ImageGrab
                    image = ImageGrab.grab(bbox=(frame.winfo_rootx(), frame.winfo_rooty(),
                                                 frame.winfo_rootx() + frame.winfo_width(),
                                                 frame.winfo_rooty() + frame.winfo_height()))
                    # Добавляем изображение в список кадров
                    frames.append(image)

                # Сохраняем кадры в формате GIF
                frames[0].save(filename, save_all=True, append_images=frames[1:], optimize=False, duration=200, loop=0)

            else:
                # Сохранение в формате PNG или JPG
                self.frames[self.current_frame].postscript(file=filename, colormode='color')
                image = PIL.Image.open(filename)

                # Определяем формат по расширению файла
                if filename.endswith(".jpg") or filename.endswith(".jpeg"):
                    image.save(filename, "JPEG")
                else:
                    image.save(filename, "PNG")


    # Функция открытия изображения
    def open_image(self):
        filename = filedialog.askopenfilename(filetypes=[('Image files', '*.png;*.jpg;*.jpeg;*.gif')])
        if filename:
            try:
                # Загружаем изображение
                image = PIL.Image.open(filename)

                # Проверяем, является ли изображение GIF
                if image.format == 'GIF':
                    # Очищаем существующие кадры
                    for frame in self.frames[1:]:
                        frame.destroy()
                    self.frames = [self.canvas]

                    # Добавляем кадры из GIF
                    for frame in ImageSequence.Iterator(image):
                        frame = frame.convert("RGB")  # Преобразуем в RGB, если нужно
                        frame = frame.resize((self.canvas_width, self.canvas_height))
                        photo = PIL.ImageTk.PhotoImage(frame)
                        new_canvas = tk.Canvas(self.master, width=self.canvas_width, height=self.canvas_height, bg="white")
                        new_canvas.pack()
                        new_canvas.create_image(0, 0, anchor='nw', image=photo)
                        new_canvas.image = photo  # Сохраняем ссылку
                        self.frames.append(new_canvas)

                    # Обновляем текущий кадр
                    self.current_frame = 0
                    self.show_current_frame()

                else:
                    # Открытие обычного изображения (PNG, JPG)
                    image = image.resize((self.canvas_width, self.canvas_height))
                    photo = PIL.ImageTk.PhotoImage(image)
                    self.frames[self.current_frame].delete('all')
                    self.frames[self.current_frame].create_image(0, 0, anchor='nw', image=photo)
                    self.frames[self.current_frame].image = photo
            except FileNotFoundError:
                tk.messagebox.showerror("Ошибка", "Файл не найден")

    def new_frame(self):
        # Создаем новый холст для кадра
        new_canvas = tk.Canvas(self.master, width=self.canvas_width, height=self.canvas_height, bg="white")
        new_canvas.pack()
        new_canvas.pack_propagate(False) # Добавлено

        # Добавляем новый кадр в список
        self.frames.append(new_canvas)

        # Связываем события мыши с функциями рисования для нового кадра
        new_canvas.bind("<B1-Motion>", self.draw)
        new_canvas.bind("<ButtonRelease-1>", self.stop_drawing)
        new_canvas.bind("<Button-1>", self.start_drawing)

    # Функция отображения текущего кадра
    def show_current_frame(self):
        for i, frame in enumerate(self.frames):
            if i == self.current_frame:
                frame.pack()
            else:
                frame.pack_forget()

    # Функция удаления кадра
    def delete_frame(self):
        if len(self.frames) > 1:
            # Удаляем последний кадр из списка
            frame_to_delete = self.frames.pop()

            # Удаляем холст из интерфейса
            frame_to_delete.destroy()
        else:
            tk.messagebox.showwarning("Предупреждение", "Нельзя удалить, так как холста нету!")

    # Функция переключения на предыдущий кадр
    def prev_frame(self):
        if self.current_frame > 0:
            self.current_frame -= 1
            self.show_current_frame()

    # Функция переключения на следующий кадр
    def next_frame(self):
        if self.current_frame < len(self.frames) - 1:
            self.current_frame += 1
            self.show_current_frame()

root = tk.Tk()
app = DrawingApp(root)
root.mainloop()