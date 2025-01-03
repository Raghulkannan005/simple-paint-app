import tkinter as tk
from tkinter import colorchooser, ttk, filedialog
from PIL import Image, ImageDraw, ImageTk, ImageGrab
import io

class PaintApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Paint")
        self.current_color = "black"
        self.brush_size = 2
        self.drawing = False
        self.eraser_mode = False
        self.previous_color = self.current_color
        self.main_frame = ttk.Frame(self.root, padding="5")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.create_toolbar()
        self.canvas = tk.Canvas(
            self.main_frame,
            width=800,
            height=600,
            bg="white",
            cursor="crosshair"
        )
        self.canvas.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

    def create_toolbar(self):
        toolbar = ttk.Frame(self.main_frame)
        toolbar.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        tools_frame = ttk.LabelFrame(toolbar, text="Tools", padding="5")
        tools_frame.pack(side="left", padx=5)
        self.brush_btn = ttk.Button(
            tools_frame,
            text="Brush",
            command=self.use_brush,
            style="Toggled.TButton"
        )
        self.brush_btn.pack(side="left", padx=2)
        self.eraser_btn = ttk.Button(
            tools_frame,
            text="Eraser",
            command=self.use_eraser
        )
        self.eraser_btn.pack(side="left", padx=2)
        color_btn = ttk.Button(
            toolbar,
            text="Choose Color",
            command=self.choose_color
        )
        color_btn.pack(side="left", padx=5)
        self.color_preview = tk.Canvas(
            toolbar,
            width=30,
            height=30,
            bg=self.current_color
        )
        self.color_preview.pack(side="left", padx=5)
        ttk.Label(toolbar, text="Size:").pack(side="left", padx=5)
        self.brush_slider = ttk.Scale(
            toolbar,
            from_=1,
            to=50,
            orient="horizontal",
            length=200,
            value=2,
            command=self.update_brush_size
        )
        self.brush_slider.pack(side="left", padx=5)
        clear_btn = ttk.Button(
            toolbar,
            text="Clear Canvas",
            command=self.clear_canvas
        )
        clear_btn.pack(side="right", padx=5)
        save_btn = ttk.Button(
            toolbar,
            text="Save",
            command=self.save_canvas
        )
        save_btn.pack(side="right", padx=5)
        load_btn = ttk.Button(
            toolbar,
            text="Load",
            command=self.load_canvas
        )
        load_btn.pack(side="right", padx=5)
        style = ttk.Style()
        style.configure("Toggled.TButton", background="lightblue")

    def use_brush(self):
        self.eraser_mode = False
        self.current_color = self.previous_color
        self.color_preview.configure(bg=self.current_color)
        self.brush_btn.configure(style="Toggled.TButton")
        self.eraser_btn.configure(style="TButton")
        self.canvas.configure(cursor="crosshair")

    def use_eraser(self):
        self.eraser_mode = True
        self.previous_color = self.current_color
        self.current_color = "white"
        self.color_preview.configure(bg=self.current_color)
        self.eraser_btn.configure(style="Toggled.TButton")
        self.brush_btn.configure(style="TButton")
        self.canvas.configure(cursor="circle")

    def choose_color(self):
        if not self.eraser_mode:
            color = colorchooser.askcolor(color=self.current_color)[1]
            if color:
                self.current_color = color
                self.previous_color = color
                self.color_preview.configure(bg=color)

    def update_brush_size(self, size):
        self.brush_size = float(size)

    def start_drawing(self, event):
        self.drawing = True
        self.last_x = event.x
        self.last_y = event.y

    def draw(self, event):
        if self.drawing:
            x, y = event.x, event.y
            self.canvas.create_line(
                self.last_x,
                self.last_y,
                x,
                y,
                width=self.brush_size,
                fill=self.current_color,
                capstyle=tk.ROUND,
                smooth=True
            )
            self.last_x = x
            self.last_y = y

    def stop_drawing(self, event):
        self.drawing = False

    def clear_canvas(self):
        self.canvas.delete("all")

    def save_canvas(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.canvas.update()
            x = self.root.winfo_rootx() + self.canvas.winfo_x()
            y = self.root.winfo_rooty() + self.canvas.winfo_y()
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            image = ImageGrab.grab(bbox=(x, y, x + width, y + height))
            image.save(file_path)

    def load_canvas(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
        if file_path:
            image = Image.open(file_path)
            self.canvas.create_image(0, 0, image=ImageTk.PhotoImage(image), anchor="nw")

    def get_canvas_image(self):
        self.canvas.update()
        ps = self.canvas.postscript(colormode='color')
        image = Image.open(io.BytesIO(ps.encode('utf-8')))
        image = image.convert("RGB")
        return ImageTk.PhotoImage(image)

def main():
    root = tk.Tk()
    app = PaintApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()