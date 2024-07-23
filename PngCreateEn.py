import tkinter as tk
from tkinter import colorchooser, filedialog
import PIL.Image
import PIL.ImageTk

class DrawingApp:
    def __init__(self, master):
        self.master = master
        master.title("PngCreate (English)")

        self.canvas_width = 600
        self.canvas_height = 400
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        self.color = "black"
        self.brush_size = 5
        self.is_drawing = False
        self.x1, self.y1 = None, None

        self.color_button = tk.Button(master, text="Color", command=self.choose_color)
        self.color_button.pack(side="left")

        self.brush_size_button = tk.Button(master, text="Brush size", command=self.change_brush_size)
        self.brush_size_button.pack(side="left")

        self.eraser_button = tk.Button(master, text="Eraser", command=self.use_eraser)
        self.eraser_button.pack(side="left")

        self.save_button = tk.Button(master, text="Save", command=self.save_image)
        self.save_button.pack(side="left")

        self.open_button = tk.Button(master, text="Open", command=self.open_image)
        self.open_button.pack(side="left")

        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)
        self.canvas.bind("<Button-1>", self.start_drawing)

    def choose_color(self):
        color = colorchooser.askcolor(title="Choose color")[1]
        if color:
            self.color = color

    def change_brush_size(self):
        new_size = int(tk.simpledialog.askstring("Brush size", "Write Brush Size:", initialvalue=str(self.brush_size)))
        if new_size > 0:
            self.brush_size = new_size

    def use_eraser(self):
        self.color = "white"

    def draw(self, event):
        if self.is_drawing:
            self.x2, self.y2 = event.x, event.y
            self.canvas.create_line(self.x1, self.y1, self.x2, self.y2, width=self.brush_size, fill=self.color, capstyle="round")
            self.x1, self.y1 = self.x2, self.y2

    def start_drawing(self, event):
        self.is_drawing = True
        self.x1, self.y1 = event.x, event.y

    def stop_drawing(self, event):
        self.is_drawing = False

    def save_image(self):
        filename = filedialog.asksaveasfilename(defaultextension=".png")
        if filename:
            self.canvas.postscript(file=filename, colormode='color')
            image = PIL.Image.open(filename)
            image.save(filename)

    def open_image(self):
        filename = filedialog.askopenfilename(filetypes=[('Image files', '*.png;*.jpg;*.jpeg')])
        if filename:
            try:
                image = PIL.Image.open(filename)
                image = image.resize((self.canvas_width, self.canvas_height))
                photo = PIL.ImageTk.PhotoImage(image)
                self.canvas.delete('all')
                self.canvas.create_image(0, 0, anchor='nw', image=photo)
                self.canvas.image = photo  # Удерживаем ссылку на изображение, чтобы оно не удалилось
            except FileNotFoundError:
                tk.messagebox.showerror("Error", "File not founded")

root = tk.Tk()
app = DrawingApp(root)
root.mainloop()