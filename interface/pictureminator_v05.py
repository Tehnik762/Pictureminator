import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk

# Initialize the main window using customtkinter
root = ctk.CTk()
root.title('Pictureminator')
root.geometry('900x550')
root.iconbitmap("E:/Working_here/interface/resources/pictureminator_01.ico")

# Function to resize the background image
def resize_image(event):
    new_size = (event.width, event.height)
    resized_image = original_image.resize(new_size)
    photo = ImageTk.PhotoImage(resized_image)
    my_label.config(image=photo)
    my_label.image = photo

original_image = Image.open("E:/Working_here/interface/resources/bg_05.png")
bg = ImageTk.PhotoImage(original_image)

my_label = ctk.CTkLabel(root, image=bg)
my_label.place(x=0, y=0, relwidth=1, relheight=1)

# Function to update switch variables
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

# Function to handle folder selection
def select_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        path_entry.set_text(folder_path)  # Use set_text for ctk.CTkEntry

# Function to start sorting based on selected options
def start_sorting():
    selected_folder = path_entry.get()  # Assuming path_entry is a ctk.CTkEntry
    # Implement sorting logic here

center_frame = ctk.CTkFrame(root)
center_frame.place(relx=0.5, rely=0.65, anchor='center')

search_frame = ctk.CTkFrame(center_frame)
search_frame.pack(pady=10, fill='x')

path_entry = ctk.CTkEntry(search_frame, placeholder_text="Folder path...", width=500)
path_entry.pack(side="left", fill="x", expand=True, padx=(10, 10))

browse_button = ctk.CTkButton(search_frame, text="Select folder", command=lambda: select_folder())
browse_button.pack(side="left", padx=(0, 10))

sorting_frame = ctk.CTkFrame(center_frame)
sorting_frame.pack(fill='x', pady=10)

year_sort_var = ctk.BooleanVar(value=False)
month_sort_var = ctk.BooleanVar(value=False)
no_sort_var = ctk.BooleanVar(value=True)

year_sort_switch = ctk.CTkSwitch(sorting_frame, text="Sort by Year", variable=year_sort_var, command=lambda: update_switches('Year'))
year_sort_switch.pack(side='top', padx=(10, 10))

month_sort_switch = ctk.CTkSwitch(sorting_frame, text="Sort by Month", variable=month_sort_var, command=lambda: update_switches('Month'))
month_sort_switch.pack(side='top', padx=(10, 10))

no_sort_switch = ctk.CTkSwitch(sorting_frame, text="No Sorting", variable=no_sort_var, command=lambda: update_switches('NoOrder'))
no_sort_switch.pack(side='top', padx=(0, 10))

root.bind('<Configure>', resize_image)
ctk.set_appearance_mode("dark")  # Set the appearance mode globally
ctk.set_default_color_theme("dark-blue")  # Set the color theme globally

root.mainloop()
