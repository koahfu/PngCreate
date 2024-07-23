import tkinter as tk
from tkinter import colorchooser, filedialog
import PIL.Image
import PIL.ImageTk

class DrawingApp:
    def __init__(self, master):
        self.master = master
        master.title("PngCreate - Графический редактор")

        # Размер холста для рисования
        self.canvas_width = 600
        self.canvas_height = 400
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        # Начальные настройки
        self.color = "black"
        self.brush_size = 5
        self.is_drawing = False
        self.x1, self.y1 = None, None

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
            self.canvas.create_line(self.x1, self.y1, self.x2, self.y2, width=self.brush_size, fill=self.color, capstyle="round")
            self.x1, self.y1 = self.x2, self.y2

    # Функция начала рисования
    def start_drawing(self, event):
        self.is_drawing = True
        self.x1, self.y1 = event.x, event.y

    # Функция окончания рисования
    def stop_drawing(self, event):
        self.is_drawing = False

    # Функция сохранения изображения
    def save_image(self):
        filename = filedialog.asksaveasfilename(defaultextension=".png")
        if filename:
            self.canvas.postscript(file=filename, colormode='color')
            image = PIL.Image.open(filename)
            image.save(filename)

    # Функция открытия изображения
    def open_image(self):
        filename = filedialog.askopenfilename(filetypes=[('Image files', '*.png;*.jpg;*.jpeg')])
        if filename:
            try:
                image = PIL.Image.open(filename)
                # Изменяем размер изображения на размер холста
                image = image.resize((self.canvas_width, self.canvas_height))
                photo = PIL.ImageTk.PhotoImage(image)
                self.canvas.delete('all')
                self.canvas.create_image(0, 0, anchor='nw', image=photo)
                self.canvas.image = photo  # Удерживаем ссылку на изображение, чтобы оно не удалилось
            except FileNotFoundError:
                tk.messagebox.showerror("Ошибка", "Файл не найден")

root = tk.Tk()
app = DrawingApp(root)
root.mainloop()