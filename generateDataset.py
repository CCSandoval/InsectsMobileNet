import os
from splitDataset import split_data
from utils import createFolder


def generateDataset():
    categories = []
    source = "./Insectos/"
    folders = os.listdir(source)

    if ".DS_Store" in folders:
        os.remove(f"{source}/.DS_store")

    for subfolder in folders:
        if os.path.isdir(source + subfolder):
            categories.append(subfolder)
            
    categories.sort()

    print(f"🎯 Categorías encontradas: {categories}")
    print()

    #Create dataset
    createFolder("./dataset/")
    createFolder("./dataset/train/")
    createFolder("./dataset/test/")
    createFolder("./dataset/validate/")

    for category in categories:
        sourcePath = source + category + "/"
        trainPath = "./dataset/train/" + category + "/" 
        testPath = "./dataset/test/" + category + "/"
        validatePath = "./dataset/validate/" + category + "/"
        print(f"🐞 Categoría: {category}")
        split_data(sourcePath, trainPath, testPath, validatePath, trainSplitSize=.7, testSplitSize=.2)
        print()