import customtkinter as ctk
from tkinter import *
from PIL import Image, ImageTk
import os
from tkinter import PhotoImage


def resize_image(event):
    new_size = (event.width, event.height)
    resized_image = original_image.resize(new_size)
    photo = ImageTk.PhotoImage(resized_image)
    my_label.config(image=photo)
    my_label.image = photo

root = ctk.CTk()

# Window settings
root.title('Pictureminator')
root.geometry('900x550')
root.iconbitmap("E:/Working_here/interface/resources/pictureminator_01.ico")

original_image = Image.open("E:/Working_here/interface/resources/bg_05.png")
bg = ImageTk.PhotoImage(original_image)

my_label = Label(root, image=bg)
my_label.place(x=0, y=0, relwidth=1, relheight=1)


def update_switches(selected_option):
    # Assuming 'selected_option' is one of 'year_sort_var', 'month_sort_var', 'no_sort_var'
    if selected_option == 'year_sort_var':
        year_sort_var.set(not year_sort_var.get())
    elif selected_option == 'month_sort_var':
        month_sort_var.set(not month_sort_var.get())
    elif selected_option == 'no_sort_var':
        no_sort_var.set(not no_sort_var.get())
        if no_sort_var.get():  # If NoOrder is selected, reset others
            year_sort_var.set(False)
            month_sort_var.set(False)

    year_on = year_sort_var.get()
    month_on = month_sort_var.get()
    nosort_on = no_sort_var.get()

    # Optionally print the current state for debugging
    print(f"Year: {year_on}, Month: {month_on}, NoOrder: {nosort_on}")


def select_folder(root):
    folder_path = filedialog.askdirectory()
    sort_folder_path = folder_path
    if folder_path:
        path_entry.delete(0, "end")
        path_entry.insert(0, folder_path)
    print("Folder select action triggered", sort_folder_path)


def start_sorting(root):
    selected_folder = path_entry.get()
    sort_option = sort_option.get()
    print(f"Sorting pictures in {selected_folder} with option: {sort_option}")


# Variables defining:
sort_folder_path = None

# Create the center_frame with a specific width and height
center_frame = ctk.CTkFrame(root)  # Adjust the size as needed
center_frame.place(relx=0.5, rely=0.65, anchor='center')

# Create a new frame for the search bar and checkbox
search_frame = ctk.CTkFrame(center_frame)
search_frame.pack(pady=10, fill='x') #padx=50, 

# Place the entry and button in the search frame instead of center frame
path_entry = ctk.CTkEntry(search_frame, placeholder_text="Folder path...", width=500)
path_entry.pack(side="left", fill="x", expand=True, padx=(10, 10))  # Add padding to separate entry and button

browse_button = ctk.CTkButton(search_frame, text="Select folder", command=select_folder(root))
browse_button.pack(side="left", padx=(0, 10))  # Adjust side to "left" and pack inside search_frame

# Create a new frame for the sorting switches under the search bar
sorting_frame = ctk.CTkFrame(center_frame)
sorting_frame.pack(fill='x', pady=10)

# Correctly bind the switches to their respective BooleanVar instances
year_sort_var = ctk.BooleanVar(value=False)
month_sort_var = ctk.BooleanVar(value=False)
no_sort_var = ctk.BooleanVar(value=True)  # Default to true if no sorting is the default

# label.pack(side="left")
# switch.pack(side="left")


# Create switches for each sorting option and bind them to BooleanVars
year_sort_switch = ctk.CTkSwitch(sorting_frame, text="Sort by Year", variable=year_sort_var, command=lambda: update_switches('Year'))
year_sort_switch.pack(side='top', fill='x')

month_sort_switch = ctk.CTkSwitch(sorting_frame, text="Sort by Month", variable=month_sort_var, command=lambda: update_switches('Month'))
month_sort_switch.pack(side='top', fill='x')

no_sort_switch = ctk.CTkSwitch(sorting_frame, text="No Sorting", variable=no_sort_var, command=lambda: update_switches('NoOrder'))
no_sort_switch.pack(side='top', fill='x')

# label.grid(row=0, column=0, sticky="e")
# switch.grid(row=0, column=1, sticky="w")





root.bind('<Configure>', resize_image)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")
root.mainloop()
