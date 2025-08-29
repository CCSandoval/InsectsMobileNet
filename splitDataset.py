import os
import shutil
import random
from utils import createFolder, fileExists

def copyFiles(sourcePath, destinationPath, fileSet):
    createFolder(destinationPath)
    for filename in fileSet:
        thisFile = sourcePath + filename
        destination = destinationPath + filename
        shutil.copyfile(thisFile, destination)

def split_data(sourcePath, trainPath, testPath, validatePath, trainSplitSize, testSplitSize):
    files = []

    for filename in os.listdir(sourcePath):
        filePath = sourcePath + "/" +filename
        if fileExists(filePath):
            files.append(filename)
        else:
            print(filename + " is empty")

    randomizedSet = random.sample(files, len(files))

    trainingLength = round(len(files) * trainSplitSize)
    testLength = round(len(files) * testSplitSize)

    trainingSet = randomizedSet[0:trainingLength]
    testSet = randomizedSet[trainingLength:(trainingLength+testLength)]
    validateSet = randomizedSet[(trainingLength+testLength):]

    #copy train images
    copyFiles(sourcePath, trainPath, fileSet=trainingSet)
    print(f"📄 {len(trainingSet)} archivos copiados para entrenamiento")
    #copy test images
    copyFiles(sourcePath, testPath, fileSet=testSet)
    print(f"📄 {len(testSet)} archivos copiados para testing")

    #copy validation images
    copyFiles(sourcePath, validatePath, fileSet=validateSet)
    print(f"📄 {len(validateSet)} archivos copiados para validación")