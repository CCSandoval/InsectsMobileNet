import os
def createFolder(folderPath):
    pathExists = os.path.exists(folderPath)
    if not pathExists:
        os.mkdir(folderPath)

def fileExists(path):
    if os.path.getsize(path) > 0:
        return True
    else:
        return False