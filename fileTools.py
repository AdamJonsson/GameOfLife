def checkIfFileExist(filePath):
    """
        Check if a file exist.
        :param filePath: The file path.
        :return: True if the file exist, false if not.
    """
    pass

def saveFileContent(filePath, content):
    """
        Save content to a file.
        :param filePath: The file path.
        :param content: The content to save.
        :return: True if content is save, false if not.
    """
    pass

def cleanString(string):
    cleanString = string.strip()
    cleanString = cleanString.replace('\n', ' ').replace('\r', '')
    return cleanString