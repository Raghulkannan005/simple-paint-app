import tkinter as tk
from tkinter import colorchooser, ttk, filedialog, simpledialog
from PIL import Image, ImageTk, ImageGrab
import io

class PaintApp:
    def __init__(self, root):
        # Initialize the main window
        self.root = root
        self.root.title("Simple Paint")
        
        # Initialize drawing properties
        self.current_color = "black"  # Default brush color
        self.brush_size = 2          # Default brush size
        self.drawing = False         # Track if user is currently drawing
        self.eraser_mode = False     # Track if eraser is active
        self.previous_color = self.current_color  # Store color before using eraser
        self.drawing_shape = None    # Track the current shape being drawn
        
        # Initialize undo stacks
        self.undo_stack = []
        
        # Create main container frame with padding
        self.main_frame = ttk.Frame(self.root, padding="5")
        self.main_frame.grid(row=0, column=0, sticky="nsew")  # Make frame expand in all directions
        
        # Create toolbar with buttons and controls
        self.create_toolbar()
        
        # Create the drawing canvas
        self.canvas = tk.Canvas(
            self.main_frame,
            width=800,
            height=600,
            bg="white",
            cursor="crosshair"  # Show crosshair cursor for precise drawing
        )
        self.canvas.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Bind mouse events for drawing
        self.canvas.bind("<Button-1>", self.start_drawing)        # Mouse click
        self.canvas.bind("<B1-Motion>", self.draw)               # Mouse drag
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing) # Mouse release
        
        # Configure grid weights to make canvas resizable
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

    def create_toolbar(self):
        # Create toolbar container
        toolbar = ttk.Frame(self.main_frame)
        toolbar.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Create tools section (brush and eraser)
        tools_frame = ttk.LabelFrame(toolbar, text="Tools", padding="5")
        tools_frame.pack(side="left", padx=5)
        
        # Add brush button
        self.brush_btn = ttk.Button(
            tools_frame,
            text="Brush",
            command=self.use_brush,
            style="Toggled.TButton"  # Special style for active state
        )
        self.brush_btn.pack(side="left", padx=2)
        
        # Add eraser button
        self.eraser_btn = ttk.Button(
            tools_frame,
            text="Eraser",
            command=self.use_eraser
        )
        self.eraser_btn.pack(side="left", padx=2)
        
        # Add color chooser button and preview
        color_btn = ttk.Button(toolbar, text="Choose Color", command=self.choose_color)
        color_btn.pack(side="left", padx=5)
        
        # Color preview canvas
        self.color_preview = tk.Canvas(
            toolbar,
            width=30,
            height=30,
            bg=self.current_color
        )
        self.color_preview.pack(side="left", padx=5)
        
        # Add brush size slider
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
        
        # Add shape buttons
        shape_frame = ttk.LabelFrame(toolbar, text="Shapes", padding="5")
        shape_frame.pack(side="left", padx=5)
        
        rect_btn = ttk.Button(shape_frame, text="Rectangle", command=self.use_rectangle)
        rect_btn.pack(side="left", padx=2)
        
        oval_btn = ttk.Button(shape_frame, text="Oval", command=self.use_oval)
        oval_btn.pack(side="left", padx=2)
        
        line_btn = ttk.Button(shape_frame, text="Line", command=self.use_line)
        line_btn.pack(side="left", padx=2)
        
        # Add canvas operation buttons (clear, save, undo)
        clear_btn = ttk.Button(toolbar, text="Clear Canvas", command=self.clear_canvas)
        clear_btn.pack(side="right", padx=5)
        
        save_btn = ttk.Button(toolbar, text="Save", command=self.save_canvas)
        save_btn.pack(side="right", padx=5)
        
        undo_btn = ttk.Button(toolbar, text="Undo", command=self.undo)
        undo_btn.pack(side="right", padx=5)
        
        # Configure special button style for toggled state
        style = ttk.Style()
        style.configure("Toggled.TButton", background="lightblue")

    def use_brush(self):
        # Switch to brush mode
        self.eraser_mode = False
        self.drawing_shape = None
        self.current_color = self.previous_color  # Restore previous color
        self.color_preview.configure(bg=self.current_color)
        # Update button styles to show active tool
        self.brush_btn.configure(style="Toggled.TButton")
        self.eraser_btn.configure(style="TButton")
        self.canvas.configure(cursor="crosshair")

    def use_eraser(self):
        # Switch to eraser mode
        self.eraser_mode = True
        self.drawing_shape = None
        self.previous_color = self.current_color  # Store current color
        self.current_color = "white"  # Set eraser color to white
        self.color_preview.configure(bg=self.current_color)
        # Update button styles to show active tool
        self.eraser_btn.configure(style="Toggled.TButton")
        self.brush_btn.configure(style="TButton")
        self.canvas.configure(cursor="circle")

    def choose_color(self):
        # Open color picker dialog if not in eraser mode
        if not self.eraser_mode:
            color = colorchooser.askcolor(color=self.current_color)[1]
            if color:
                self.current_color = color
                self.previous_color = color
                self.color_preview.configure(bg=color)

    def update_brush_size(self, size):
        # Update brush size from slider value
        self.brush_size = float(size)

    def use_rectangle(self):
        # Switch to rectangle drawing mode
        self.drawing_shape = "rectangle"
        self.canvas.configure(cursor="crosshair")

    def use_oval(self):
        # Switch to oval drawing mode
        self.drawing_shape = "oval"
        self.canvas.configure(cursor="crosshair")

    def use_line(self):
        # Switch to line drawing mode
        self.drawing_shape = "line"
        self.canvas.configure(cursor="crosshair")

    def start_drawing(self, event):
        # Begin drawing and store initial coordinates
        self.drawing = True
        self.last_x = event.x
        self.last_y = event.y
        if self.drawing_shape:
            self.shape_id = None
            if self.drawing_shape == "text":
                self.add_text(event)

    def draw(self, event):
        # Create line segments while dragging mouse
        if self.drawing:
            x, y = event.x, event.y
            if self.drawing_shape == "rectangle":
                if self.shape_id:
                    self.canvas.delete(self.shape_id)
                self.shape_id = self.canvas.create_rectangle(self.last_x, self.last_y, x, y, outline=self.current_color, width=self.brush_size)
            elif self.drawing_shape == "oval":
                if self.shape_id:
                    self.canvas.delete(self.shape_id)
                self.shape_id = self.canvas.create_oval(self.last_x, self.last_y, x, y, outline=self.current_color, width=self.brush_size)
            elif self.drawing_shape == "line":
                if self.shape_id:
                    self.canvas.delete(self.shape_id)
                self.shape_id = self.canvas.create_line(self.last_x, self.last_y, x, y, fill=self.current_color, width=self.brush_size)
            else:
                line = self.canvas.create_line(self.last_x, self.last_y, x, y, width=self.brush_size, fill=self.current_color, capstyle=tk.ROUND, smooth=True)
                self.undo_stack.append(line)
                self.last_x = x
                self.last_y = y

    def stop_drawing(self, event):
        # End drawing operation
        self.drawing = False
        if self.drawing_shape and self.shape_id:
            self.undo_stack.append(self.shape_id)
            self.shape_id = None

    def clear_canvas(self):
        # Remove all drawings from canvas
        self.canvas.delete("all")
        # Clear undo stacks
        self.undo_stack.clear()

    def save_canvas(self):
        # Save canvas as PNG file
        file_path = filedialog.asksaveasfilename(defaultextension=".jpeg", filetypes=[("JPEG files", "*.jpeg")])
        if file_path:
            self.canvas.update()
            # Calculate canvas position and size
            x = self.root.winfo_rootx() + self.canvas.winfo_x()
            y = self.root.winfo_rooty() + self.canvas.winfo_y()
            width = self.canvas.winfo_width()
            height = self.canvas.winfo_height()
            # Capture and save screenshot of canvas area
            image = ImageGrab.grab(bbox=(x, y, x + width, y + height))
            image.save(file_path)

    def undo(self):
        # Undo the last action
        if self.undo_stack:
            last_action = self.undo_stack.pop()
            self.canvas.delete(last_action)

    def get_canvas_image(self):
        # Convert canvas content to PhotoImage format
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