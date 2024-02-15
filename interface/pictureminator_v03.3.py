import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import os

class PictureminatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window settings
        self.title('Pictureminator')
        self.geometry('1000x650')  # Adjust the window size as needed
        self.iconbitmap("resources/pictureminator_01.ico")

        # Update window for correct widget positions
        self.update_idletasks()

        # Center frame
        self.center_frame = ctk.CTkFrame(self)  # Adjust the size as needed
        self.center_frame.place(relx=0.5, rely=0.75, anchor='center')

        self.original_image = Image.open("resources/bg_05.png")
        self.bg = ImageTk.PhotoImage(self.original_image)

        self.my_label = ctk.CTkLabel(self.center_frame, text=" ", image=self.bg)
        self.my_label.pack(expand=True, fill='both')

        # Bind the resize event to the resize_image method
        self.my_label.bind("<Configure>", self.resize_image)

        # Variables
        self.sort_folder_path = None

        # Search frame
        self.search_frame = ctk.CTkFrame(self.center_frame)
        self.search_frame.pack(pady=10, fill='x')

        # Path entry and browse button
        self.path_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Folder path...", width=500)
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(10, 10))

        self.browse_button = ctk.CTkButton(self.search_frame, text="Select folder", command=self.select_folder)
        self.browse_button.pack(side="left", padx=(10, 10))

        # Sorting frame
        self.sorting_frame = ctk.CTkFrame(self.center_frame)
        self.sorting_frame.pack(side="left", padx=(10, 10), pady=10)

        # Sorting switches
        self.year_sort_var = ctk.BooleanVar(value=False)
        self.month_sort_var = ctk.BooleanVar(value=False)
        self.no_sort_var = ctk.BooleanVar(value=True)  # Default to "No Sorting"

        self.year_sort_switch = ctk.CTkSwitch(self.sorting_frame, text="Sort by Year", variable=self.year_sort_var, command=lambda: self.update_switches('Year'))
        self.year_sort_switch.pack(side='top', fill='x')

        self.month_sort_switch = ctk.CTkSwitch(self.sorting_frame, text="Sort by Month", variable=self.month_sort_var, command=lambda: self.update_switches('Month'))
        self.month_sort_switch.pack(side='top', fill='x')

        self.no_sort_switch = ctk.CTkSwitch(self.sorting_frame, text="No Sorting", variable=self.no_sort_var, command=lambda: self.update_switches('NoOrder'))
        self.no_sort_switch.pack(side='top', fill='x')

        # Variable for storing sorting option
        self.sort_option = ctk.StringVar(value="")  # Initially empty


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


    def start_sorting(self):
        selected_folder = self.path_entry.get()
        sort_option = self.sort_option.get()
        print(f"Sorting pictures in {selected_folder} with option: {sort_option}")


    # Function to resize the background image
    def resize_image(self, event):
        new_size = (event.width, event.height)
        resized_image = self.original_image.resize(new_size)
        self.bg = ImageTk.PhotoImage(resized_image)  # Keep a reference to the PhotoImage
        self.my_label.configure(image=self.bg)
        self.my_label.image = self.bg  # Update the image attribute of the label


# Run the application
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = PictureminatorApp()
    app.mainloop()
