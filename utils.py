"""
utils.py
"""
def create_dir(base_dir: str):
    """
    create base_dir if not exist
    """
    import os
    try:
        os.makedirs(base_dir)
    except OSError:
        if not os.path.isdir(base_dir):
            raise
    return True