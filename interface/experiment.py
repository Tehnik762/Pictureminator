import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, BooleanVar
from PIL import Image, ImageTk, ImageOps
from PIL.Image import Resampling
import os
import time

class CustomFrameApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("'Pictureminator'")
        self.geometry('1200x650')
        self.iconbitmap(r"E:/Working_here/interface/resources/pictureminator_01.ico")

        # Update window for correct widget positions
        self.update_idletasks()

        self.create_frames()


    def create_frames(self):
        # Create frames
        self.left_frame = tk.Frame(self, bg='white', width=1200 // 3, height=650)
        self.right_frame = tk.Frame(self, bg='dark slate gray', width=1200 // 3 * 2, height=650)

        # Use pack geometry manager to place the frames
        self.left_frame.pack(side='left', fill='y')
        self.right_frame.pack(side='right', fill='both', expand=True)

        # Prevent the frames from resizing to fit their contents
        self.left_frame.pack_propagate(False)
        self.right_frame.pack_propagate(False)

        # Collage Image  
        collage_path = "E:/Working_here/interface/resources/collage-removebg_x50.png"
        self.collage_path = ImageTk.PhotoImage(file=collage_path)
        self.collage = self.canvas.create_image(220, 280, image=self.collage_path)


        # Add content to the frames as needed, for example:
        self.left_label = tk.Label(self.left_frame, text=" ", bg='gray15')
        self.left_label.pack()

        self.right_label = tk.Label(self.right_frame, text=" ", bg='gray15')
        self.right_label.pack()

def main():
    app = CustomFrameApplication()
    app.mainloop()

if __name__ == "__main__":
    main()
