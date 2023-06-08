import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageDraw

class ImageViewer:
    def __init__(self, window):
        self.window = window
        self.window.title("Image Viewer")
        self.window.wm_attributes('-zoomed', True)

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
        self.window_width, self.window_height = self.window.winfo_width(), self.window.winfo_height()
        self.display_image = self.image.resize((self.window_width, self.window_height), Image.ANTIALIAS)
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
            # calculate ratio between original image size and window size
            x_ratio = self.original_image.width / self.window_width
            y_ratio = self.original_image.height / self.window_height

            # scale the event x, y coordinates to match the original image
            scaled_last_x = int(self.last_x * x_ratio)
            scaled_last_y = int(self.last_y * y_ratio)
            scaled_event_x = int(event.x * x_ratio)
            scaled_event_y = int(event.y * y_ratio)

            draw = ImageDraw.Draw(self.image)
            draw.line([(scaled_last_x, scaled_last_y), (scaled_event_x, scaled_event_y)], fill="black", width=5)

            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y, fill="black", width=5)

            self.last_x = event.x
            self.last_y = event.y

    def stop_drawing(self, event):
        self.drawing = False

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x600")
    ImageViewer(root)
    root.mainloop()
