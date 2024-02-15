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
        # self.geometry('+%d+%d'%(1200,650))
        self.geometry('1200x650')  # Adjust the window size as needed
        self.iconbitmap(r"E:/Working_here/interface/resources/pictureminator_01.ico")

        # Update window for correct widget positions
        self.update_idletasks()

        # Center frame
        self.center_frame_bg = ctk.CTkFrame(self)  # Adjust the size as needed
        self.center_frame_bg.place(relx=0.5, rely=0.5, anchor='center')


        # Load and display the background image
        try:
            self.original_image = Image.open(r"E:/Working_here/interface/resources/bg_0212.png")
            # self.bg_photo = ImageTk.PhotoImage(self.original_image)
            self.bg_photo = ctk.CTkImage(light_image=self.original_image, size=(1200, 800))
            self.bg_label = ctk.CTkLabel(self, text=" ", image=self.bg_photo)  # Notice the parent is 'self', not 'self.center_frame'
            self.bg_label.pack(side='top', fill='both', expand=True)  # Pack it first so it's at the bottom
        except Exception as e:
            print(f"Failed to load background image: {e}")
            self.original_image = None
            # self.bg_photo = None
            # self.my_label.place(x=0, y=0, relwidth=1, relheight=1)

        # self.original_image = Image.open("E:/Working_here/interface/resources/bg_022.png")
        # self.bg_photo = ImageTk.PhotoImage(self.original_image)

        # self.my_label = ctk.CTkLabel(self.center_frame, text=" ", image=self.bg_photo)
        # self.my_label.pack(expand=True, fill='both')
        

        # Variables
        self.sort_folder_path = None


        # Title frame
        self.title_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="transparent")
        self.title_frame.place(relx=0.375, rely=0.30, anchor='center')

        #Title
        self.title = ctk.CTkLabel(self.title_frame, text="Pictureminator! Sorting pictures", font=("Segoe UI", 24), fg_color="transparent", text_color="white")
        self.title.pack(side="top", padx=15, pady=(15, 15))


        # Search frame
        # self.search_frame = ctk.CTkFrame(self.center_frame)
        # self.search_frame.pack(padx=(0, 0), pady=(10, 10))
        self.search_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="transparent")
        self.search_frame.place(relx=0.5, rely=0.8, anchor='center')

        # Path entry and browse button
        self.path_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Select a folder for sorting...", font=("Segoe UI", 14), width=500)
        self.path_entry.pack(side="left", fill="x", expand=True)
        # Select Folder Button
        self.browse_button = ctk.CTkButton(self.search_frame, text="Select folder", font=("Segoe UI", 14), command=self.select_folder)
        self.browse_button.pack(side="left")


        # Sorting frame left
        # self.sorting_frame = ctk.CTkFrame(self.center_frame)
        # self.sorting_frame.pack(side="left", padx=(0, 0), pady=0)
        self.timer_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="transparent")
        self.timer_frame.place(relx=0.5, rely=0.70, anchor='center')
        # Timer label
        self.timer_label = ctk.CTkLabel(self.timer_frame, text="00:00:00", font=("Segoe UI", 32))
        self.timer_label.pack(side="right", padx=(10), pady=(10))


        # Sorting frame right
        self.robot_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="transparent")
        self.robot_frame.place(relx=0.68, rely=0.40, anchor='center')
        # self.sorting_frame_right = ctk.CTkFrame(self, corner_radius=20, fg_color="transparent")
        # self.sorting_frame_right.place(relx=0.7, rely=0.70, anchor='center')
        # Load the image (adjust the path to where your image is located)
        self.robot_image_path = Image.open(r"E:/Working_here/interface/resources/pictureminator_x50.png")
        self.robot_image = ImageTk.PhotoImage(self.robot_image_path)
        # Create an image label widget to display the robot image
        self.image_label = ctk.CTkLabel(self.robot_frame, text=" ", image=self.robot_image, bg_color="transparent")
        self.image_label.pack(side="left", padx=0, pady=0)

        # Center frame
        self.center_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="transparent")
        self.center_frame.place(relx=0.75, rely=0.72, anchor='center')

        # Sorting frame right
        self.sorting_frame_right = ctk.CTkFrame(self.center_frame)
        self.sorting_frame_right.pack(side="right", padx=(0, 0), pady=(0, 0))
        # Button to start sorting
        self.start_button = ctk.CTkButton(self.sorting_frame_right, text="Start Sorting", font=("Segoe UI", 14), command=self.start_sorting)
        self.start_button.pack(side='left', padx=0, pady=0, fill='x')

        # # Progress bar
        # self.progress_bar = ctk.CTkProgressBar(self.progress_frame, width=660)
        # self.progress_bar.pack(side="top", fill="x", padx=10, pady=10)
        # self.progress_bar.set(0)

        # # Load the image (adjust the path to where your image is located)
        # self.robot_image_path = Image.open(r"E:/Working_here/interface/resources/pictureminator_x75.png")
        # self.robot_image = ImageTk.PhotoImage(self.robot_image_path)

        # # Create an image label widget to display the robot image
        # self.image_label = ctk.CTkLabel(self.sorting_frame_right, text=" ", image=self.robot_image)
        # self.image_label.pack(side="left", padx=(25, 35), pady=10)

        # Flag to indicate sorting status
        self.sorting = False

        # Sorting switches
        self.year_sort_var = tk.BooleanVar(value=False)
        self.month_sort_var = tk.BooleanVar(value=False)
        self.no_sort_var = tk.BooleanVar(value=True)  # Default to "No Sorting"

        self.sorting_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="transparent")
        self.sorting_frame.place(relx=0.25, rely=0.68, anchor='center')

        self.year_sort_switch = ctk.CTkSwitch(self.sorting_frame, text="Sort by Year", font=("Segoe UI", 14), variable=self.year_sort_var, command=lambda: self.update_switches('Year'))
        self.year_sort_switch.pack(side='top', padx=3, pady=(10, 3))

        self.month_sort_switch = ctk.CTkSwitch(self.sorting_frame, text="Sort by Month", font=("Segoe UI", 14), variable=self.month_sort_var, command=lambda: self.update_switches('Month'))
        self.month_sort_switch.pack(side='top', padx=3, pady=3)

        self.no_sort_switch = ctk.CTkSwitch(self.sorting_frame, text="No Sorting", font=("Segoe UI", 14), variable=self.no_sort_var, command=lambda: self.update_switches('NoOrder'))
        self.no_sort_switch.pack(side='top', padx=3, pady=(3, 10))

        # Variable for storing sorting option
        self.sort_option = tk.StringVar(value="NoOrder")  # Initially set to "NoOrder"


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


    def start_timer(self):
            self.start_time = time.time()
            self.update_timer()


    def update_timer(self):
        if self.sorting:
            elapsed_time = time.time() - self.start_time
            minutes, seconds = divmod(int(elapsed_time), 60)
            hours, minutes = divmod(minutes, 60)
            self.timer_label.config(text=f"{hours:02d}:{minutes:02d}:{seconds:02d}")
            self.after(1000, self.update_timer)  # Schedule this method to be called every 1000 milliseconds


    def start_sorting(self):
        selected_folder = self.path_entry.get()
        sort_option = self.sort_option.get()
        
        print(f"Sorting pictures in {selected_folder} with option: {sort_option}")


# Run the application
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = PictureminatorApp()
    app.mainloop()

