import tkinter as tk
from tkinter import colorchooser, filedialog
import PIL.Image
import PIL.ImageTk
from PIL import ImageGrab  
from PIL import ImageSequence

class DrawingApp:
    def __init__(self, master):
        self.master = master
        master.title("PngCreate v1.1 beta (English)")

        self.canvas_width = 600
        self.canvas_height = 400
        self.canvas = tk.Canvas(master, width=self.canvas_width, height=self.canvas_height, bg="white")

        self.frame = tk.Frame(master)
        self.color = "black"
        self.brush_size = 5
        self.is_drawing = False
        self.x1, self.y1 = None, None
        self.frames = [self.canvas] 
        self.current_frame = 0 

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

        self.new_frame_button = tk.Button(master, text="New picture", command=self.new_frame)
        self.new_frame_button.pack(side="left")

        self.delete_frame_button = tk.Button(master, text="Delete picture", command=self.delete_frame)
        self.delete_frame_button.pack(side="left")

        self.prev_frame_button = tk.Button(master, text="<<", command=self.prev_frame)
        self.prev_frame_button.pack(side="left")

        self.next_frame_button = tk.Button(master, text=">>", command=self.next_frame)
        self.next_frame_button.pack(side="left")

        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)
        self.canvas.bind("<Button-1>", self.start_drawing)

    def choose_color(self):
        color = colorchooser.askcolor(title="Color chooser")[1]
        if color:
            self.color = color

    def change_brush_size(self):
        new_size = int(tk.simpledialog.askstring("Brush size", "Write Brush size:", initialvalue=str(self.brush_size)))
        if new_size > 0:
            self.brush_size = new_size

    def use_eraser(self):
        self.color = "white"

    def draw(self, event):
        if self.is_drawing:
            self.x2, self.y2 = event.x, event.y
            event.widget.create_line(self.x1, self.y1, self.x2, self.y2, width=self.brush_size, fill=self.color, capstyle="round")
            self.x1, self.y1 = self.x2, self.y2

    def start_drawing(self, event):
        self.is_drawing = True
        self.x1, self.y1 = event.x, event.y

    def stop_drawing(self, event):
        self.is_drawing = False

    def save_image(self):
        filename = filedialog.asksaveasfilename(defaultextension=".png")
        if filename:
            if len(self.frames) > 1:

                frames = []
                for frame in self.frames:

                    image = ImageGrab.grab(bbox=(frame.winfo_rootx(), frame.winfo_rooty(),
                                                 frame.winfo_rootx() + frame.winfo_width(),
                                                 frame.winfo_rooty() + frame.winfo_height()))

                    frames.append(image)


                frames[0].save(filename, save_all=True, append_images=frames[1:], optimize=False, duration=200, loop=0)

            else:

                self.frames[self.current_frame].postscript(file=filename, colormode='color')

                if filename.endswith(".jpg") or filename.endswith(".jpeg"):
                    image.save(filename, "JPEG")
                else:
                    image.save(filename, "PNG")

    def open_image(self):
        filename = filedialog.askopenfilename(filetypes=[('Image files', '*.png;*.jpg;*.jpeg;*.gif')])
        if filename:
            try:

                image = PIL.Image.open(filename)

                if image.format == 'GIF':

                    for frame in self.frames[1:]:
                        frame.destroy()
                    self.frames = [self.canvas]

                    for frame in ImageSequence.Iterator(image):
                        frame = frame.convert("RGB")  
                        frame = frame.resize((self.canvas_width, self.canvas_height))
                        photo = PIL.ImageTk.PhotoImage(frame)
                        new_canvas = tk.Canvas(self.master, width=self.canvas_width, height=self.canvas_height, bg="white")
                        new_canvas.pack()
                        new_canvas.create_image(0, 0, anchor='nw', image=photo)
                        new_canvas.image = photo
                        self.frames.append(new_canvas)

                    self.current_frame = 0
                    self.show_current_frame()

                else:

                    image = image.resize((self.canvas_width, self.canvas_height))
                    photo = PIL.ImageTk.PhotoImage(image)
                    self.frames[self.current_frame].delete('all')
                    self.frames[self.current_frame].create_image(0, 0, anchor='nw', image=photo)
                    self.frames[self.current_frame].image = photo
            except FileNotFoundError:
                tk.messagebox.showerror("Error", "File not founded")

    def new_frame(self):

        new_canvas = tk.Canvas(self.master, width=self.canvas_width, height=self.canvas_height, bg="white")
        new_canvas.pack()
        new_canvas.pack_propagate(False)

        self.frames.append(new_canvas)

        new_canvas.bind("<B1-Motion>", self.draw)
        new_canvas.bind("<ButtonRelease-1>", self.stop_drawing)
        new_canvas.bind("<Button-1>", self.start_drawing)

    def show_current_frame(self):
        for i, frame in enumerate(self.frames):
            if i == self.current_frame:
                frame.pack()
            else:
                frame.pack_forget()

    def delete_frame(self):
        if len(self.frames) > 1:

            frame_to_delete = self.frames.pop()

            frame_to_delete.destroy()
        else:
            tk.messagebox.showwarning("Warning", "Cannot be deleted because there is no canvas!")

    def prev_frame(self):
        if self.current_frame > 0:
            self.current_frame -= 1
            self.show_current_frame()

    def next_frame(self):
        if self.current_frame < len(self.frames) - 1:
            self.current_frame += 1
            self.show_current_frame()

root = tk.Tk()
app = DrawingApp(root)
root.mainloop()