import customtkinter as ctk
from tkinter import filedialog, BooleanVar
from PIL import Image, ImageTk
import os


class PictureminatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('Pictureminator')
        self.geometry('900x550')  # Adjust the window size as needed

        # Create a frame to center all content
        self.center_frame = ctk.CTkFrame(self)
        self.center_frame.place(relx=0.35, rely=0.5, anchor='center')  # Use place geometry manager for centering

        # Create a new frame for the search bar and checkbox
        self.search_frame = ctk.CTkFrame(self.center_frame)
        self.search_frame.pack(fill='x', expand=True)

        # Place the entry and button in the search frame instead of center frame
        self.path_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Select folder...")
        self.path_entry.pack(side="left", fill="x", expand=True)

        # Load the image using Pillow and resize it for the button
        try:
            self.search_icon_path = "E:/Git&GitHub/Pictureminator/interface/resources/res_search_icon_00.png"
            image = Image.open(self.search_icon_path)
            self.search_icon = ImageTk.PhotoImage(image.resize((30, 30), Image.BICUBIC))

            # Create the button with the correct image object
            self.browse_button = ctk.CTkButton(self.center_frame, text="Image Folder", image=self.search_icon, command=self.select_folder)
            self.browse_button.image = self.search_icon  # keep a reference!
            self.browse_button.pack(side="right", padx=10)
        except IOError as e:
            print(f"Unable to load image at path {self.search_icon_path}. Error: {e}")

        # Create a new frame for the sorting switches under the search bar
        self.sorting_frame = ctk.CTkFrame(self.center_frame)
        self.sorting_frame.pack(fill='x', pady=10)

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
        #Set all switch variables to False first
        
        self.year_sort_var.set(year_onf)
        self.month_sort_var.set(month_onf)
        self.no_sort_var.set(nosort_onf)

        year_onf = self.year_sort_var.get()
        month_onf = self.month_sort_var.get()
        nosort_onf = self.no_sort_var.get()

        # Toggle the state of the selected switch
        if selected_option == 'Year':
            if self.year_sort_var.get() == self.year_sort_var.set(True):  # If it was already on, just toggle it off
                self.year_sort_var.set(False)
            else:  # If it was off, turn it on and the others off
                self.year_sort_var.set(True)
                self.no_sort_var.set(False)
        elif selected_option == 'Month':
            if self.month_sort_var.get():  # If it was already on, just toggle it off
                self.month_sort_var.set(False)
            else:  # If it was off, turn it on and the others off
                self.month_sort_var.set(True)
                self.no_sort_var.set(False)
        elif selected_option == 'NoOrder':
            # If 'No Sorting' is turned on, turn off the other two switches
            if self.no_sort_var.get():  # If it was already on, just toggle it off
                self.no_sort_var.set(False)
            else:  # If it was off, turn it on and the others off
                self.no_sort_var.set(True)
                self.year_sort_var.set(False)
                self.month_sort_var.set(False)


    def select_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.path_entry.delete(0, "end")
            self.path_entry.insert(0, folder_path)


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
