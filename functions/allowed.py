

def is_allowed(name):
    """
    Checks if the given name is allowed based on its file extension.

    Args:
        name (str): The name of the file.

    Returns:
        bool: True if the file extension is allowed, False otherwise.
    """
    pict = ["jpg", "jpeg", "png", "heic", "gif", "bmp"]
    name = name.lower()
    name = name.split(".")[-1]
    return name in pict

def is_video(name):
    """
    Checks if the given name is a video based on its file extension.
    """
    name = name.lower()
    name = name.split(".")[-1]
    return name in ["mp4", "mov", "avi", "mkv"]