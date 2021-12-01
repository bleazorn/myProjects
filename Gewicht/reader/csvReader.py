import csv

from objects.weightObj import WeightObj


def getDataFromCsv(csvFile):
    ret = []
    with open(csvFile, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=';', quotechar='|')
        for row in csvreader:
            ele = WeightObj(row)
            ret.append(ele)
    return ret


def writeRowsToCsv(csvFile, weights):
    with open(csvFile, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for w in weights:
            csvwriter.writerow(w.csvRowStr())
