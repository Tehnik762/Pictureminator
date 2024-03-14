# Pictureminator

Pictureminator is a program developed as part of the Data Science course at WBS CODING SCHOOL.

![Pictureminator](https://github.com/Tehnik762/Pictureminator/blob/master/pictureminator.jpg?raw=true)

## Overview
The main idea of the program is to use pre-trained models to classify incoming photos into groups such as documents, screenshots, video files, duplicates, and photos of average or superior quality.

## Installation
To install, clone the repository and execute `pip install -r requirements.txt` for all required packages.

## Usage
After installing all packages, you can run the program using the following command:

```
python pictureminator.py /path/to/folder
```


Where `/path/to/folder` is the full path to the folder containing the photos to be sorted.

After sorting, several folders will be created where the final photos will be organized.

Additionally, you can pass a parameter `year` or `month` after the folder name in the command line. In the first case, the photos will be sorted by the year of creation, and in the second case, the months of creation will be added within the years.

## Development Stage
The program is currently in the development stage.

We invite everyone interested to participate in the development.

If you wish to enhance our models, you can place your photos in the `images` folder, extract features using `scan_images.py`, and train the models using Jupyter Notebooks.

We would appreciate it if you open corresponding issues in the respective section.

---
Feel free to contribute to Pictureminator and make it better! 📸✨
