import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, BooleanVar
from PIL import Image, ImageTk, ImageOps
from PIL.Image import Resampling
import os
import time


class PictureminatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window settings
        self.title('Pictureminator')
        self.geometry('1200x650')  # Adjust the window size as needed
        self.iconbitmap(r"E:/Working_here/interface/resources/pictureminator_01.ico")

        self.canvas = tk.Canvas(self, width=1920, height=1080)
        self.canvas.place(x=0, y=0)
        self.canvas.configure(bg="gray20")
        # # Update window for correct widget positions
        self.update_idletasks()

        self.canvas.grid(column=1, row=0)
     
        # Function to create a rectangle with rounded corners
        def create_rounded_rect(canvas, x1, y1, x2, y2, radius=25, **kwargs):
                points = [
                    x1+radius, y1,
                    x1+radius, y1,
                    x2-radius, y1,
                    x2-radius, y1,
                    x2, y1,
                    x2, y1+radius,
                    x2, y1+radius,
                    x2, y2-radius,
                    x2, y2-radius,
                    x2, y2,
                    x2-radius, y2,
                    x2-radius, y2,
                    x1+radius, y2,
                    x1+radius, y2,
                    x1, y2,
                    x1, y2-radius,
                    x1, y2-radius,
                    x1, y1+radius,
                    x1, y1+radius,
                    x1, y1
                ]
                return canvas.create_polygon(points, **kwargs, smooth=True)

              
        # # BG Image  
        # bg_path = "E:/Working_here/interface/resources/color_pol.jpg"
        # self.bg_path = ImageTk.PhotoImage(file=bg_path)
        # self.bg = self.canvas.create_image(600, 325, image=self.bg_path)

        self.pictures_bg_01 = create_rounded_rect(self.canvas, 20, 20, 450, 630, radius=20, fill='white')
        self.pictures_bg_02 = create_rounded_rect(self.canvas, 470, 20, 1180, 630, radius=20, fill='grey15')
        
        # Collage Image  
        collage_path = "E:/Working_here/interface/resources/collage-removebg_x50.png"
        self.collage_path = ImageTk.PhotoImage(file=collage_path)
        self.collage = self.canvas.create_image(225, 330, image=self.collage_path)

        # Load and set the robot image
        robot_path = "E:/Working_here/interface/resources/pictureminator_x50.png"
        self.robot = ImageTk.PhotoImage(file=robot_path)
        self.robot_label = self.canvas.create_image(950, 200, image=self.robot, anchor='nw')
        self.canvas.tag_bind(self.robot_label, '<Button-1>', self.start_sorting)


        # self.title_bg = create_rounded_rect(self.canvas, 590, 80, 900, 130, radius=20, fill='black')
        self.title_bg = create_rounded_rect(self.canvas, 470, 85, 1180, 145, radius=0, fill='grey15')

        # self.instructions = tk.Label(self, text="Sorting Pictures <> - <>", font=("Segoe UI", 16))
        self.instructions = self.canvas.create_text(700, 100, text="// Pictureminator!", font=("Segoe UI", 18), fill='Silver', anchor="nw")

        # Variables
        self.sort_folder_path = None

        self.search_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="grey15")
        self.search_frame.place(relx=0.6875, rely=0.8, anchor='center')

        # Path entry and browse button
        self.path_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Select a folder for sorting...", font=("Segoe UI", 14), width=530)
        self.path_entry.pack(side="left", padx=(20, 0), pady=20, expand=True)
        # Select Folder Button
        self.browse_button = ctk.CTkButton(self.search_frame, text="Select folder", font=("Segoe UI", 14), command=self.select_folder)
        self.browse_button.pack(side="left", padx=(0, 20))
        
        
        
        # Flag to indicate sorting status
        self.sorting = False

        # Sorting switches
        self.year_sort_var = tk.BooleanVar(value=False)
        self.month_sort_var = tk.BooleanVar(value=False)
        self.no_sort_var = tk.BooleanVar(value=True)  # Default to "No Sorting"

        self.sorting_frame = ctk.CTkFrame(self, corner_radius=0, fg_color='grey15')
        self.sorting_frame.place(relx=0.6875, rely=0.7145, anchor='center')

        self.year_sort_switch = ctk.CTkSwitch(self.sorting_frame, text="Sort by Year", font=("Segoe UI", 14), variable=self.year_sort_var, command=lambda: self.update_switches('Year'))
        self.year_sort_switch.pack(side='left', padx=(70, 30), pady=(20, 10))

        self.month_sort_switch = ctk.CTkSwitch(self.sorting_frame, text="Sort by Month", font=("Segoe UI", 14), variable=self.month_sort_var, command=lambda: self.update_switches('Month'))
        self.month_sort_switch.pack(side='left', padx=30, pady=(10, 10))

        self.no_sort_switch = ctk.CTkSwitch(self.sorting_frame, text="No Sorting", font=("Segoe UI", 14), variable=self.no_sort_var, command=lambda: self.update_switches('NoOrder'))
        self.no_sort_switch.pack(side='left', padx=(30, 162.5), pady=(10, 10))

        # Variable for storing sorting option
        self.sort_option = tk.StringVar(value="NoOrder")  # Initially set to "NoOrder"


        def close():
            self.destroy()
            self.update()


    def update_switches(self, selected_option):
        # Reset all variables first
        self.year_sort_var.set(False)
        self.month_sort_var.set(False)
        self.no_sort_var.set(False)

        # Then set the selected option to True
        if selected_option == 'Year':
            self.year_sort_var.set(True)
            self.sort_option.set('Year')
        elif selected_option == 'Month':
            self.month_sort_var.set(True)
            self.sort_option.set('Month')
        elif selected_option == 'NoOrder':
            self.no_sort_var.set(True)
            self.sort_option.set('NoOrder')

        # Optional debugging print
        year_on = self.year_sort_var.get()
        month_on = self.month_sort_var.get()
        nosort_on = self.no_sort_var.get()
        print(f"Year: {year_on}, Month: {month_on}, NoOrder: {nosort_on}")


    def select_folder(self):
        folder_path = filedialog.askdirectory()
        self.sort_folder_path = folder_path
        if folder_path:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, folder_path)
        print("Folder select action triggered", self.sort_folder_path)


    def start_sorting(self, event=None):
        selected_folder = self.path_entry.get()
        sort_option = self.sort_option.get()
        
        print(f"Sorting pictures in {selected_folder} with option: {sort_option}")


# Run the application
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = PictureminatorApp()
    app.mainloop()

