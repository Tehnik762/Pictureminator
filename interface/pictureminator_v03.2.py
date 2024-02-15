import tkinter as tk
from tkinter import filedialog, IntVar
import pictureminator_sort
import pictureminator_sort
import PIL.Image
import PIL.ImageTk
import PIL.ImageOps

class PictureminatorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window settings
        self.title("Pictureminator - Main Window")
        self.geometry('1000x650')
        self.iconbitmap("E:/Working_here/interface/resources/pictureminator_01.ico")


        # Load and display background image
        self.original_image = PIL.Image.open("E:/Working_here/interface/resources/bg_022.png")
        self.original_image = PIL.ImageOps.exif_transpose(self.original_image)
        self.bg_photo = tk.PhotoImage(self.original_image)
        self.background_label = tk.Label(self, image=self.bg_photo)
        self.background_label.pack(relx=0.5, rely=0.5, anchor="center")


        # Search frame and entry
        self.search_frame = tk.Frame(self)
        self.search_frame.pack(pady=10)

        self.folder_path_var = tk.StringVar()
        self.path_entry = tk.Entry(
            self.search_frame,
            width=50,
        )
        self.path_entry.pack(side="left", fill="x", expand=True)

        self.browse_button = tk.Button(self.search_frame, text="Browse", command=self.select_folder)
        self.browse_button.pack(side="left")

        # Label for input guidance (replace with appropriate text)
        self.input_label = tk.Label(self.search_frame, text="Enter folder path:")
        self.input_label.pack(side="left")

        # Sorting options
        self.sorting_frame = tk.Frame(self)
        self.sorting_frame.pack(pady=10)

        self.sorting_option_var = IntVar(value=0)

        self.year_sort_switch = tk.Radiobutton(
            self.sorting_frame, text="Sort by Year", variable=self.sorting_option_var, value=1
        )
        self.year_sort_switch.pack(side="top")

        self.month_sort_switch = tk.Radiobutton(
            self.sorting_frame, text="Sort by Month", variable=self.sorting_option_var, value=2
        )
        self.month_sort_switch.pack(side="top")

        self.no_sort_switch = tk.Radiobutton(
            self.sorting_frame, text="No Sorting", variable=self.sorting_option_var, value=0
        )
        self.no_sort_switch.pack(side="top")

        # Start sorting button
        self.start_sort_button = tk.Button(self, text="Start Sorting", command=self.start_sorting)
        self.start_sort_button.pack(pady=20)

        # Run the main loop
        self.mainloop()

    def select_folder(self):
        selected_folder_path = filedialog.askdirectory()
        if selected_folder_path:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, selected_folder_path)
            print("Folder selected:", selected_folder_path)
        else:
            print("No folder selected.")

    def start_sorting(self):
        selected_folder = self.path_entry.get()
        if not selected_folder:
            raise ValueError("Please select a folder to sort.")

        sort_option = self.sorting_option_var.get()

        # Integrate with pictureminator_sort.py function calls based on your sort options
        print(f"Sorting pictures in {selected_folder} with option: {sort_option}")

        # Add sorting functionality using appropriate calls to pictureminator_sort.py functions
        # Handle results and provide feedback to the user

# Replace "pictureminator_sort.py" with the actual path to your module

if __name__ == "__main__":
    app = PictureminatorApp()
    app.mainloop()
