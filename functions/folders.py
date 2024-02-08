import os

def create(base):
    """
    Creates directories for 'screenshots', 'documents', 'duplicates', and 'good' inside the given base directory if they do not already exist.

    Parameters:
    - base: The base directory in which the subdirectories will be created.

    Returns:
    - None.
    """
    values = ["screenshots", "documents", "duplicates", "good", "not_good"]
    if os.path.exists(base):
        for v in values:
            if not os.path.exists(f"{base}/{v}"):
                os.mkdir(f"{base}/{v}")
