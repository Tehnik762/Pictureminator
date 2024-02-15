import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, BooleanVar
from PIL import Image, ImageTk, ImageOps
from PIL.Image import Resampling
import os


class PictureminatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Variables defining:
        self.sort_folder_path = None

        # Window settings
        self.title('Pictureminator')
        self.geometry('1000x650')  # Adjust the window size as needed
        self.iconbitmap("E:/Working_here/interface/resources/pictureminator_01.ico")
        
        # Make sure to call update_idletasks to ensure all widgets have been drawn and have valid positions
        self.update_idletasks() 

        # Create the center_frame with a specific width and height
        self.center_frame = ctk.CTkFrame(self)  # Adjust the size as needed
        self.center_frame.place(relx=0.5, rely=0.75, anchor='center')

        # Load the original image and keep a reference to it
        self.original_image = Image.open("E:/Working_here/interface/resources/bg_022.png")
        self.bg_photo = ImageTk.PhotoImage(self.original_image)

        self.my_label = ctk.CTkLabel(self, text=' ', image=self.bg_photo)
        self.my_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Bind the resize event to resize_image method
        self.bind('<Configure>', self.resize_image)

        # Load the transparent image
        self.transparent_image = Image.open("E:/Working_here/interface/resources/pictureminator.png")
        self.transparent_photo = ImageTk.PhotoImage(self.transparent_image)

        # Calculate the position for the image label
        # Assuming self.center_frame is the frame where the search bar and other controls are located
        # self.image_label_x = self.center_frame.winfo_x() - 20  # Adjust the value as needed
        # self.image_label_y = self.center_frame.winfo_y() - 5  # Adjust the value as needed

        # Create a label for the transparent image and place it on the right above the search bar, a little to the left
        self.transparent_label = ctk.CTkLabel(self, text=" ", image=self.transparent_photo)
        self.transparent_label.place(x=500, y=300, relwidth=1, relheight=1)#(x=self.image_label_x, y=self.image_label_y)

        # Variables defining:
        self.sort_folder_path = None

        # Create a new frame for the search bar and checkbox
        self.search_frame = ctk.CTkFrame(self.center_frame)
        self.search_frame.pack(pady=10, fill='x')

        # Place the entry and button in the search frame instead of center frame
        self.path_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Folder path...", width=500)
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(10, 10))  # Add padding to separate entry and button

        self.browse_button = ctk.CTkButton(self.search_frame, text="Select folder", command=self.select_folder)
        self.browse_button.pack(side="left", padx=(10, 10))  # Adjust side to "left" and pack inside search_frame
        
        # Create a new frame for the sorting switches under the search bar
        self.sorting_frame = ctk.CTkFrame(self.center_frame)
        self.sorting_frame.pack(side="left", padx=(10, 10), pady=10)

        # Correctly bind the switches to their respective BooleanVar instances
        self.year_sort_var = ctk.BooleanVar(value=False)
        self.month_sort_var = ctk.BooleanVar(value=False)
        self.no_sort_var = ctk.BooleanVar(value=True)  # Default to true if no sorting is the default

        # Create switches for each sorting option and bind them to BooleanVars
        self.year_sort_switch = ctk.CTkSwitch(self.sorting_frame, text="Sort by Year", variable=self.year_sort_var, command=lambda: self.update_switches('Year'))
        self.year_sort_switch.pack(side='top', fill='x')

        self.month_sort_switch = ctk.CTkSwitch(self.sorting_frame, text="Sort by Month", variable=self.month_sort_var, command=lambda: self.update_switches('Month'))
        self.month_sort_switch.pack(side='top', fill='x')

        self.no_sort_switch = ctk.CTkSwitch(self.sorting_frame, text="No Sorting", variable=self.no_sort_var, command=lambda: self.update_switches('NoOrder'))
        self.no_sort_switch.pack(side='top', fill='x')
        

    def update_switches(self, selected_option):
        # Reset all variables first
        self.year_sort_var.set(False)
        self.month_sort_var.set(False)
        self.no_sort_var.set(False)

        # Then set the selected option to True
        if selected_option == 'Year':
            self.year_sort_var.set(True)
        elif selected_option == 'Month':
            self.month_sort_var.set(True)
        elif selected_option == 'NoOrder':
            self.no_sort_var.set(True)  # Assuming you want to set this to True for NoOrder

        # Optionally print the current state for debugging
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


    def start_sorting(self):
        selected_folder = self.path_entry.get()
        sort_option = self.sort_option.get()
        print(f"Sorting pictures in {selected_folder} with option: {sort_option}")


    def resize_image(self, event):
        # Reload the original image to avoid degradation over multiple resizes
        self.original_image = Image.open("E:/Working_here/interface/resources/bg_022.png")
        new_size = (event.width, event.height)
        resized_image = self.original_image.resize(new_size, Resampling.LANCZOS)
        self.bg_photo = ImageTk.PhotoImage(resized_image)
        self.my_label.configure(image=self.bg_photo)
        # Keep a reference to the new photo image to prevent garbage collection
        self.my_label.image = self.bg_photo


# Run the application
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = PictureminatorApp()
    app.mainloop()
