from objects.dataBank import CsvDataBank

# read csv file and returns a list of entries in a list of csvData class
# par: file is location of csv file
# ret: list of csvData entries of the csv file
def readCSVFile(file, classDataEntry=CsvDataBank):
    csv = open(file, 'r')
    dataFile = []
    nameLine = csv.readline()
    for line in csv:
        csvEntry = readCSVLine(nameLine, line, classDataEntry)
        if csvEntry:
            dataFile.append(csvEntry)
    csv.close()
    return dataFile


# transform a csv line in to csvData type entry
# par: line
# ret: datafile entry
def readCSVLine(nameLine, dataLine, classDataEntry):
    return classDataEntry(nameLine, dataLine)


def writeCSVLine(file, line, index):
    with open(file, 'w') as w:
        w.write(line)


def checkRightCVSLine(line, classDataEntry):
    pass
