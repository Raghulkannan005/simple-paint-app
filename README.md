# Simple Paint Application

## Overview

The Simple Paint Application is a basic drawing tool built using Python and Tkinter. It allows users to draw on a canvas using different brush sizes and colors, as well as save and load their drawings.

## Features

- **Brush Tool**: Draw on the canvas with adjustable brush sizes.
- **Eraser Tool**: Erase parts of the drawing.
- **Color Picker**: Choose different colors for the brush.
- **Save**: Save the current drawing as a PNG file.
- **Load**: Load a previously saved PNG file onto the canvas.
- **Clear Canvas**: Clear the entire canvas.

## Requirements

- Python 3.x
- Pillow library

## Installation

1. **Clone the repository**:

    ```sh
    git clone https://github.com/yourusername/paint-app.git
    cd paint-app
    ```

2. **Install the required dependencies**:

    ```sh
    pip install pillow
    ```

## Usage

1. **Run the application**:

    ```sh
    python paint-app.py
    ```

2. **Drawing**:
    - Select the brush tool to start drawing.
    - Adjust the brush size using the slider.
    - Choose a color using the color picker.

3. **Erasing**:
    - Select the eraser tool to erase parts of the drawing.

4. **Saving and Loading**:
    - Click the "Save" button to save the current drawing as a PNG file.
    - Click the "Load" button to load a previously saved PNG file onto the canvas.

5. **Clearing the Canvas**:
    - Click the "Clear Canvas" button to clear the entire canvas.

## Acknowledgements

- This application uses the [Tkinter](https://docs.python.org/3/library/tkinter.html) library for the GUI.
- The [Pillow](https://python-pillow.org/) library is used for image processing.
