import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw

class ImageViewer:
    def __init__(self, window):
        self.window = window
        self.window.title("Image Viewer")

        # Menu
        self.menu = tk.Menu(self.window)
        self.window.config(menu=self.menu)

        # File Menu
        self.file_menu = tk.Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Open", command=self.open_image)
        self.file_menu.add_command(label="Save", command=self.save_image)

        # Canvas to display image
        self.canvas = tk.Canvas(self.window)
        self.canvas.pack(fill="both", expand=True)

        # Drawing setup
        self.drawing = False
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)

        # Resize image when window size changes
        self.window.bind("<Configure>", self.resize_image)

    def open_image(self):
        # Open the file dialog and get the image file path
        self.file_path = filedialog.askopenfilename()

        # Open the image using PIL and convert it to PhotoImage
        self.original_image = Image.open(self.file_path)
        self.image = self.original_image.copy()

        # Trigger a resize to display the image initially
        self.resize_image()

    def resize_image(self, event=None):
        # Resize image to match window size and update canvas
        width, height = self.window.winfo_width(), self.window.winfo_height()
        self.display_image = self.image.resize((width, height), Image.ANTIALIAS)
        self.photo_image = ImageTk.PhotoImage(self.display_image)

        # Clear the canvas and put the image on it
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor='nw', image=self.photo_image)

    def save_image(self):
        # Save the image to the original path
        self.image.save(self.file_path)

    def draw(self, event):
        if not self.drawing:
            self.drawing = True
            self.last_x = event.x
            self.last_y = event.y
        else:
            draw = ImageDraw.Draw(self.image)
            draw.line([(self.last_x, self.last_y), (event.x, event.y)], fill="black", width=5)
            self.display_draw = ImageDraw.Draw(self.display_image)
            self.display_draw.line([(self.last_x, self.last_y), (event.x, event.y)], fill="black", width=5)
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill="black", width=5)
            self.last_x = event.x
            self.last_y = event.y

    def stop_drawing(self, event):
        self.drawing = False

if __name__ == "__main__":
    root = tk.Tk()
    ImageViewer(root)
    root.mainloop()
