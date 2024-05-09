# Pictureminator

Pictureminator is a program developed as part of the Data Science course at WBS CODING SCHOOL.

![Pictureminator](https://github.com/Tehnik762/Pictureminator/blob/master/pictureminator.jpg?raw=true)

## Overview
The main idea of the program is to use pre-trained models to classify incoming photos into groups such as documents, screenshots, video files, duplicates, and photos of average or superior quality.

## Installation
To install, clone the repository and execute `pip install -r requirements.txt` for all required packages.

If you are having issues installing **`dlib`** library, you might need to follow this steps:

-- install **Visual Studio Community** (free version: https://visualstudio.microsoft.com/free-developer-offers/)

-- from **Visual Studio Installer** - select and install **Desktop development with C++**

-- download and install **CMake** from here: https://cmake.org/download/

-- reinstall **`dlib`** library in your environment


## Usage
After installing all packages, you can run the program using the following command:

```
python pictureminator.py /path/to/folder
```


Where `/path/to/folder` is the full path to the folder containing the photos to be sorted.

After sorting, several folders will be created where the final photos will be organized.

Additionally, you can pass a parameter `year` or `month` after the folder name in the command line. In the first case, the photos will be sorted by the year of creation, and in the second case, the months of creation will be added within the years.

## GUI
In the interface folder there is a file called Pictureminator_GUI.py - it is the first interface build in order to have an nice-looking and easier to use user experience.
After running

```
python Pictureminator_GUI.py
```

a GUI will appear. The user must now only select (or paste) in the search bar the link to the folder with the pictures that needs sorting, and select the sorting type that is prefered:

`Monthly Sorting` - which sorts the pictures based on year and month,

`Year Sorting` - only based on year, and

`No sorting` - which is obvious, no type of sorting based of the date of the picture.


**--- Curently we are working on connecting the GUI with the back-sorting program. When finished this line will be deleted ---**


## Development Stage
The program is currently in the development stage.

We invite everyone interested to participate in the development.

If you wish to enhance our models, you can place your photos in the `images` folder, extract features using `scan_images.py`, and train the models using Jupyter Notebooks.

We would appreciate it if you open corresponding issues in the respective section.

---
Feel free to contribute to Pictureminator and make it better! 📸✨
