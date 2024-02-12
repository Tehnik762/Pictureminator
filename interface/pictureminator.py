import customtkinter as ctk
from tkinter import filedialog, StringVar, Tk
from PIL import Image, ImageTk


# class PictureminatorApp(ctk.CTk):
#     def __init__(self):
#         super().__init__()

#         self.title('Pictureminator')
#         self.geometry('900x550')  # Adjust the window size as needed

#         # Create a frame to center all content
#         self.center_frame = ctk.CTkFrame(self)
#         self.center_frame.place(relx=0.35, rely=0.5, anchor='center')  # Use place geometry manager for centering

#         # Create a new frame for the search bar and checkbox
#         self.search_frame = ctk.CTkFrame(self.center_frame)
#         self.search_frame.pack(fill='x', expand=True)

#         # Place the entry and button in the search frame instead of center frame
#         self.path_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Select folder...")
#         self.path_entry.pack(side="left", fill="x", expand=True)

#         # Load the image using Pillow and resize it for the button
#         try:
#             self.search_icon_path = "E:/Git&GitHub/Pictureminator/interface/resources/res_search_icon_00.png"
#             image = Image.open(self.search_icon_path)
#             self.search_icon = ImageTk.PhotoImage(image.resize((30, 30), Image.BICUBIC))

#             # Create the button with the correct image object
#             self.browse_button = ctk.CTkButton(self.center_frame, text="Image Folder", image=self.search_icon, command=self.select_folder)
#             self.browse_button.image = self.search_icon  # keep a reference!
#             self.browse_button.pack(side="right", padx=10)
#         except IOError as e:
#             print(f"Unable to load image at path {self.search_icon_path}. Error: {e}")

#         # Create a new frame for the sorting switches under the search bar
#         self.sorting_frame = ctk.CTkFrame(self.center_frame)
#         self.sorting_frame.pack(fill='x', pady=10)

#         # Create BooleanVar for each switch
#         self.sort_by_year = ctk.BooleanVar(value=False)
#         self.sort_by_month = ctk.BooleanVar(value=False)
#         self.no_sort = ctk.BooleanVar(value=True)

#         # Create switches for each sorting option
#         self.year_month_sort_switch = ctk.CTkSwitch(self.sorting_frame, text="Sort by Year", variable=self.sort_by_year, command=lambda: self.update_switches('Year'))
#         self.month_sort_switch = ctk.CTkSwitch(self.sorting_frame, text="Sort by Month", variable=self.sort_by_month, command=lambda: self.update_switches('Month'))
#         self.no_sort_switch = ctk.CTkSwitch(self.sorting_frame, text="No Sorting", variable=self.no_sort, command=lambda: self.update_switches('NoOrder'))

#         # Initialize the switches based on the default sort option
#         self.sort_option = StringVar(value="NoOrder")  # Set default sort option as "NoOrder"
#         self.update_switches(self.sort_option.get())

#     def update_switches(self, switch_name):
#         # Update the sorting option based on the selected switch
#         if switch_name == 'Year':
#             self.sort_by_year.set(True)
#             self.no_sort.set(False)
#         elif switch_name == 'Month':
#             self.sort_by_month.set(True)
#             self.no_sort.set(False)
#         elif switch_name == 'NoOrder':
#             self.sort_by_year.set(False)
#             self.sort_by_month.set(False)
#             self.no_sort.set(True)

#     def select_folder(self):
#         folder_path = filedialog.askdirectory()
#         if folder_path:
#             self.path_entry.delete(0, "end")
#             self.path_entry.insert(0, folder_path)


#     def start_sorting(self):
#         selected_folder = self.path_entry.get()
#         sort_option = self.sort_option.get()
#         print(f"Sorting pictures in {selected_folder} with option: {sort_option}")


# # Run the application
# if __name__ == "__main__":
#     ctk.set_appearance_mode("dark")
#     ctk.set_default_color_theme("dark-blue")
#     app = PictureminatorApp()
#     app.mainloop()

import customtkinter as ctk
from tkinter import filedialog, StringVar, Tk
from PIL import Image, ImageTk

class PictureminatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title('Pictureminator')
        self.geometry('900x550')  # Adjust the window size as needed

        # Create a frame to center all content
        self.center_frame = ctk.CTkFrame(self)
        self.center_frame.place(relx=0.5, rely=0.5, anchor='center')  # Center the frame

        # Create a new frame for the search bar
        self.search_frame = ctk.CTkFrame(self.center_frame)
        self.search_frame.pack(fill='x', expand=True)

        self.path_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Select folder...")
        self.path_entry.pack(side="left", fill="x", expand=True)

        # Load the image for the button
        self.search_icon_path = "E:/Git&GitHub/Pictureminator/interface/resources/res_search_icon_00.png"
        image = Image.open(self.search_icon_path)
        image = image.resize((30, 30), Image.ANTIALIAS)
        self.search_icon = ImageTk.PhotoImage(image)

        # Create the button with the image
        self.browse_button = ctk.CTkButton(self.search_frame, image=self.search_icon, command=self.select_folder)
        self.browse_button.pack(side="right", padx=10)

        # Create a new frame for the sorting switches under the search bar
        self.sorting_frame = ctk.CTkFrame(self.center_frame)
        self.sorting_frame.pack(fill='x', pady=10)

        # Create BooleanVar for each switch
        self.sort_by_year = ctk.BooleanVar(value=False)
        self.sort_by_month = ctk.BooleanVar(value=False)
        self.no_sort = ctk.BooleanVar(value=True)

        # Create switches for each sorting option
        self.year_sort_switch = ctk.CTkSwitch(self.sorting_frame, text="Sort by Year", variable=self.sort_by_year, command=lambda: self.update_switches('Year'))
        self.year_sort_switch.pack(side='left', padx=10, pady=10)
        self.month_sort_switch = ctk.CTkSwitch(self.sorting_frame, text="Sort by Month", variable=self.sort_by_month, command=lambda: self.update_switches('Month'))
        self.month_sort_switch.pack(side='left', padx=10, pady=10)
        self.no_sort_switch = ctk.CTkSwitch(self.sorting_frame, text="No Sorting", variable=self.no_sort, command=lambda: self.update_switches('NoOrder'))
        self.no_sort_switch.pack(side='left', padx=10, pady=10)

        # Set the default sorting option
        self.sort_option = StringVar(value="NoOrder")
        self.update_switches(self.sort_option.get())

    # ... rest of your class

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = PictureminatorApp()
    app.mainloop()



