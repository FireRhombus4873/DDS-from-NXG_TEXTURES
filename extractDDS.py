import pathlib
import argparse
import os

def main():
    parser = argparse.ArgumentParser("extractDDS.py")
    parser.description = "Extracts .DDS files from .NXG_TEXTURES files."
    parser.add_argument("-s", "--silent", action="store_true", help="Run the script in silent mode.")
    parser.add_argument("-S", "--subdirs", action="store_true", help="Extract from all subdirectories.")
    parser.add_argument("directory", nargs="?", default="", help="Directory to extract from (relative to Extracted).")
    args = parser.parse_args()

    if args.silent: silent = True
    if args.subdirs: subDir = True
    if args.directory: dirName = args.directory.replace("/", "\\")

    dirCount = 0
    fileCount = 0

    inputDirectory = ".\\Extracted\\" + dirName + "\\"

    if not subDir:
        subDir = input("Do you want to extract all subdirectories in " + dirName + "? (y/n): ").lower() == 'y'

    if subDir:
        directories = [x[0] for x in os.walk(inputDirectory)]
    else:
        directories = [inputDirectory]

    for directory in directories:
        outputDirectory = ".\\Converted\\" + dirName + "\\" + os.path.relpath(directory, inputDirectory)
        
        textureFiles = getNXGTextureFiles(directory)
        
        if len(textureFiles) == 0:
            continue

        pathlib.Path(outputDirectory).mkdir(parents=True, exist_ok=True)
        dirCount += 1

        for textureFile in textureFiles:
            textureData = readNXGTextureFile(textureFile)

            fileNames = findDDSFileNames(textureData)

            if not silent: print(f"Extracting .DDS files from {os.path.basename(textureFile)}...")

            imagesData = findDDSInTextureData(textureData)

            if len(fileNames) < len(imagesData) and not silent:
                print(f"Found {len(imagesData)} images and {len(fileNames)} filenames, cutting off the empty images.")
            
            imagesData = imagesData[-len(fileNames):]

            for i in range(len(fileNames)):
                with open(os.path.join(outputDirectory, fileNames[i].replace(".nut", "") + ".dds"), "wb") as outputFile:
                    outputFile.write(imagesData[i])
                fileCount += 1

    print("Extraction complete.")
    print(f"Created {dirCount} directories and {fileCount} files.")

def findDDSFileNames(textureData):
    fileNames = []

    nameSignature = b'.nut'
    badFile = b'dummylightmap'

    i = 0
    while i < len(textureData):
        try:
            index = textureData.index(nameSignature, i)
            
            # Search backwards for a path separator or null byte
            startIndex = index - 1
            while startIndex >= 0 and textureData[startIndex:startIndex + 1] not in (b'\\', b'/', b'\x00'):
                startIndex -= 1
            startIndex += 1

            fileNameBytes = textureData[startIndex:index + len(nameSignature)]
            fileName = fileNameBytes.decode('utf-8', errors='ignore').strip('\x00')

            # Extract just the filename (after the last path separator)
            fileName = fileName.split('\\')[-1].split('/')[-1]

            if badFile.decode('utf-8') not in fileName.lower():
                fileNames.append(fileName)

            i = index + len(nameSignature)
        except ValueError:
            break

    return fileNames

def findDDSInTextureData(textureData):
    ddsSignature = b'DDS '
    
    DDSFiles = []
    imagesData = []
    
    i = 0
    while i < len(textureData):
        try:
            index = textureData.index(ddsSignature, i)
            DDSFiles.append(index)
            i = index + 1
        except ValueError:
            break
    
    if not DDSFiles:
        return b''

    for i in range(len(DDSFiles)):
        start = DDSFiles[i]
        end = DDSFiles[i + 1] if i + 1 < len(DDSFiles) else len(textureData)
        imagesData.append(textureData[start:end])

    return imagesData

def readNXGTextureFile(filePath):
    with open(filePath, "rb") as file:
        data = file.read()
    return data

def getNXGTextureFiles(inputDirectory):
    textureFiles = []

    for fileName in os.listdir(inputDirectory):
        if fileName.lower().endswith(".nxg_textures"):
            textureFiles.append(os.path.join(inputDirectory, fileName))

    return textureFiles

if __name__ == "__main__":
    main()