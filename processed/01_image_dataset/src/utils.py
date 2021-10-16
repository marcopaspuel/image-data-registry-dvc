def ensure_dir(directory):
    """
    Creates a directory if it does not exist yet.

    :param directory: path to directory to be created
    :return:
    """
    if not directory.is_dir():
        directory.mkdir()
