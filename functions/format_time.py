def format_seconds(seconds):
    """
    Format seconds into hours, minutes, and remaining seconds and return the result as a string.

    Parameters:
    seconds (int): The total number of seconds to be formatted.

    Returns:
    str: The formatted time string representing hours, minutes, and remaining seconds.
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    remaining_seconds = round(seconds % 60)

    result = ""
    if hours > 0:
        result += f"{hours} hour{'s' if hours > 1 else ''} "
    if minutes > 0:
        result += f"{minutes} minute{'s' if minutes > 1 else ''} "
    if remaining_seconds > 0:
        result += f"{remaining_seconds} second{'s' if remaining_seconds > 1 else ''} "

    return result.strip()