# Import required libraries
import tkinter as tk                           # Main GUI library
from tkinter import colorchooser, ttk, filedialog  # Additional GUI components
from PIL import Image, ImageGrab              # Image handling library
import io                                     # Input/output operations

class PaintApp:
    def __init__(self, root):
        self.root = root                      # Store main window reference
        self.root.title(" Paint")             # Set window title
        
        # Initialize drawing properties
        self.current_color = "black"          # Default drawing color
        self.brush_size = 2                   # Default brush thickness
        self.drawing = False                  # Track if user is currently drawing
        self.eraser_mode = False              # Track if eraser is active
        self.previous_color = self.current_color  # Store color before eraser
        self.drawing_shape = None             # Track active shape tool
        self.undo_stack = []                  # Store drawing actions for undo
        
        # Create main application frame
        self.main_frame = ttk.Frame(self.root, padding="5")
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Set up UI components
        self.create_toolbar()                 # Create top toolbar
        self.setup_canvas()                   # Setup drawing canvas
        self.configure_grid()                 # Configure grid layout

    def create_toolbar(self):
        # Create main toolbar frame
        toolbar = ttk.Frame(self.main_frame)
        toolbar.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
        
        # Create drawing tools section
        tools_frame = ttk.LabelFrame(toolbar, text="Drawing Tools", padding="5")
        tools_frame.pack(side="left", padx=5)
        
        # Add brush and eraser buttons
        self.brush_btn = ttk.Button(tools_frame, text="Brush Tool", 
                                  command=self.use_brush, 
                                  style="Toggled.TButton")
        self.brush_btn.pack(side="left", padx=2)
        
        self.eraser_btn = ttk.Button(tools_frame, text="Eraser Tool", 
                                    command=self.use_eraser)
        self.eraser_btn.pack(side="left", padx=2)
        
        # Create color selection section
        color_frame = ttk.LabelFrame(toolbar, text="Color Options", padding="5")
        color_frame.pack(side="left", padx=5)
        
        # Add color picker and preview
        color_btn = ttk.Button(color_frame, text="Select Color", 
                              command=self.choose_color)
        color_btn.pack(side="left", padx=2)
        
        self.color_preview = tk.Canvas(color_frame, width=30, height=30, 
                                     bg=self.current_color)
        self.color_preview.pack(side="left", padx=2)
        
        # Create brush size control section
        size_frame = ttk.LabelFrame(toolbar, text="Brush Size", padding="5")
        size_frame.pack(side="left", padx=5)

        # Add brush size slider
        self.brush_slider = ttk.Scale(size_frame, from_=1, to=50, 
                                    orient="horizontal", length=200, 
                                    value=2,
                                    command=self.update_brush_size)
        self.brush_slider.pack(side="left", padx=2)

        # Create shape tools section
        shape_frame = ttk.LabelFrame(toolbar, text="Shape Tools", padding="5")
        shape_frame.pack(side="left", padx=5)

        # Add shape buttons
        ttk.Button(shape_frame, text="Rectangle", 
                  command=self.use_rectangle).pack(side="left", padx=2)
        ttk.Button(shape_frame, text="Oval", 
                  command=self.use_oval).pack(side="left", padx=2)
        ttk.Button(shape_frame, text="Line", 
                  command=self.use_line).pack(side="left", padx=2)

        # Create canvas operations section
        operations_frame = ttk.LabelFrame(toolbar, text="Canvas Operations", 
                                        padding="5")
        operations_frame.pack(side="right", padx=5)
        
        # Add canvas operation buttons
        ttk.Button(operations_frame, text="Clear All", 
                  command=self.clear_canvas).pack(side="left", padx=2)
        ttk.Button(operations_frame, text="Save Image", 
                  command=self.save_canvas).pack(side="left", padx=2)
        ttk.Button(operations_frame, text="Undo", 
                  command=self.undo).pack(side="left", padx=2)
        
        # Configure button styles
        style = ttk.Style()
        style.configure("Toggled.TButton", background="lightblue")

    def setup_canvas(self):
        # Create main drawing canvas
        self.canvas = tk.Canvas(
            self.main_frame,
            width=800,
            height=600,
            bg="white",
            cursor="crosshair"
        )
        self.canvas.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        
        # Bind mouse events for drawing
        self.canvas.bind("<Button-1>", self.start_drawing)      # Mouse click
        self.canvas.bind("<B1-Motion>", self.draw)             # Mouse drag
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing) # Mouse release

    def configure_grid(self):
        # Configure grid weights for proper resizing
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

    # Drawing tool functions
    def use_brush(self):
        # Activate brush tool
        self.eraser_mode = False
        self.drawing_shape = None
        self.current_color = self.previous_color
        self.color_preview.configure(bg=self.current_color)
        self.brush_btn.configure(style="Toggled.TButton")
        self.eraser_btn.configure(style="TButton")
        self.canvas.configure(cursor="crosshair")

    def use_eraser(self):
        # Activate eraser tool
        self.eraser_mode = True
        self.drawing_shape = None
        self.previous_color = self.current_color
        self.current_color = "white"
        self.color_preview.configure(bg=self.current_color)
        self.eraser_btn.configure(style="Toggled.TButton")
        self.brush_btn.configure(style="TButton")
        self.canvas.configure(cursor="circle")

    def choose_color(self):
        # Open color picker dialog
        if not self.eraser_mode:
            try:
                color = colorchooser.askcolor(color=self.current_color)[1]
                if color:
                    self.current_color = color
                    self.previous_color = color
                    self.color_preview.configure(bg=color)
            except Exception as e:
                print(f"Error selecting color: {e}")

    def update_brush_size(self, size):
        # Update brush thickness
        self.brush_size = float(size)

# Shape tool functions
    def use_rectangle(self):
        self.drawing_shape = "rectangle"
        self.canvas.configure(cursor="crosshair")

    def use_oval(self):
        self.drawing_shape = "oval"
        self.canvas.configure(cursor="crosshair")

    def use_line(self):
        self.drawing_shape = "line"
        self.canvas.configure(cursor="crosshair")


    # Drawing event handlers
    def start_drawing(self, event):
        # Initialize drawing
        self.drawing = True
        self.last_x = event.x
        self.last_y = event.y
        if self.drawing_shape:
            self.shape_id = None

    def draw(self, event):
        # Handle drawing motion
        if self.drawing:
            x, y = event.x, event.y
            if self.drawing_shape:
                # Draw shapes (preview while dragging)
                if self.shape_id:
                    self.canvas.delete(self.shape_id)
                if self.drawing_shape == "rectangle":
                    self.shape_id = self.canvas.create_rectangle(
                        self.last_x, self.last_y, x, y,
                        outline=self.current_color, width=self.brush_size
                    )
                elif self.drawing_shape == "oval":
                    self.shape_id = self.canvas.create_oval(
                        self.last_x, self.last_y, x, y,
                        outline=self.current_color, width=self.brush_size
                    )
                elif self.drawing_shape == "line":
                    self.shape_id = self.canvas.create_line(
                        self.last_x, self.last_y, x, y,
                        fill=self.current_color, width=self.brush_size
                    )
            else:
                # Free-hand drawing
                line = self.canvas.create_line(
                    self.last_x, self.last_y, x, y,
                    width=self.brush_size, fill=self.current_color,
                    capstyle=tk.ROUND, smooth=True
                )
                self.undo_stack.append(line)
                self.last_x = x
                self.last_y = y

    def stop_drawing(self, event):
        # Finalize drawing
        self.drawing = False
        if self.drawing_shape and self.shape_id:
            self.undo_stack.append(self.shape_id)
            self.shape_id = None

    # Canvas operation functions
    def clear_canvas(self):
        # Clear entire canvas
        try:
            self.canvas.delete("all")
            self.undo_stack.clear()
        except Exception as e:
            print(f"Error clearing canvas: {e}")

    def save_canvas(self):
        # Save canvas as image file
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".jpeg",
                filetypes=[("JPEG files", "*.jpeg")]
            )
            if file_path:
                self.canvas.update()
                x = self.root.winfo_rootx() + self.canvas.winfo_x()
                y = self.root.winfo_rooty() + self.canvas.winfo_y()
                width = self.canvas.winfo_width()
                height = self.canvas.winfo_height()
                image = ImageGrab.grab(bbox=(x, y, x + width, y + height))
                image.save(file_path)
        except Exception as e:
            print(f"Error saving canvas: {e}")

    def undo(self):
        # Undo last drawing action
        if self.undo_stack:
            try:
                last_action = self.undo_stack.pop()
                self.canvas.delete(last_action)
            except Exception as e:
                print(f"Error during undo: {e}")

# Application entry point
def main():
    root = tk.Tk()                # Create main window
    app = PaintApp(root)          # Initialize paint application
    root.mainloop()               # Start event loop

main()