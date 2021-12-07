from objects.dataEntry import DataEntry

# normal class for bank entries
class DataBank(DataEntry):
    CategoryNameC = "Category"
    def __init__(self, *att):
        super().__init__(*att)
        if len(att) == 1 and type(att[0]) is dict:
            self.name = self.getAttr("Volgnummer") + " : " + self.getOther(self.getAttr("Details"))
            self.sender = self.getOther(self.getAttr("Details"))
        self.setAttr("Bedrag", ".".join(self.getAttr("Bedrag").split(',')))

    def getSender(self):
        return self.sender

    # in the form of x.z.t
    def getCategoryName(self):
        return self.getAttr(DataBank.CategoryNameC)

    # parse the details to get the senders name
    def getOther(self, details):
        if details:
            det = details
            if details[0:6] == "NUMMER":
                det = self.deleteFirstNumbers(details[7:])
                det = self.findDatum(det)
            elif details[0:2] == "BE":
                det = self.deleteFirstNumbers(details[3:])
            det = det.split(':')[0]
            return det
        else:
            return ""

    # gives a value that can be used to sort on volgnummer
    def sortVolgnummer(self):
        splt = self.getAttr("Volgnummer").split("-")
        return int(splt[0]) * 10000 + int(splt[1])

    # gives a value that can be used to sort on bedrag
    def sortBedrag(self, name):
        return float(self.getAttr(name))

    def __repr__(self):
        return self.getAttr("Volgnummer") + " : " + self.getAttr("Bedrag") + " : " + self.name + " : " + self.getAttr("Uitvoeringsdatum")

    def __str__(self):
        return self.getAttr("Volgnummer") + " : " + self.getAttr("Bedrag") + " : " + self.name + " : " + self.getAttr("Uitvoeringsdatum")

    def __bool__(self):
        splt = self.getAttr("Volgnummer").split('-')
        return len(splt) == 2 and splt[1] != ""

    # finds tge datum in de details portion
    @staticmethod
    def findDatum(details):
        i = 0
        for s in details:
            if str.isdigit(s):
                a = details[i:i + 2] + details[i + 2] + details[i + 3:i + 5] + details[i + 5] + details[i + 6:i + 10]
                if str.isdigit(details[i:i + 2]) and details[i + 2] == '/' and str.isdigit(details[i + 3:i + 5]) and \
                        details[i + 5] == '/' and str.isdigit(details[i + 6:i + 10]):
                    return details[:i]
            i += 1

    # deletes the first number in details
    @staticmethod
    def deleteFirstNumbers(details):
        i = 0
        for s in details:
            if str.isdigit(s) or str.isspace(s) or s == "X":
                i += 1
            else:
                break
        return details[i:]


# subclass from DataBank for getting items from csv
class CsvDataBank(DataBank):
    def __init__(self, *att):
        super().__init__(*att)
        if len(att) == 2 and type(att[0]) is str and type(att[1]) is str:
            self.create(att[0], att[1])
            self.setAttr(DataBank.CategoryNameC, "")
            self.name = self.getAttr("Volgnummer") + " : " + self.getOther(self.getAttr("Details"))
            self.sender = self.getOther(self.getAttr("Details"))

    # creates the data entry for bank statement. Needs the first line of the csv file and the data line
    def create(self, nameLine, dataLine):
        names = nameLine.split(";")
        data = dataLine.split(";")
        i = 0
        for name in names:
            self.setAttr(self.cleanVar(name), self.cleanText(data[i]))
            i += 1

    @staticmethod
    def cleanVar(text):
        return text.replace('\n', '').replace(' ', '')

    @staticmethod
    def cleanText(text):
        return text.replace('\n', '')


def test():
    n = "Volgnummer;Uitvoeringsdatum;Valutadatum;Bedrag;Valuta rekening;TEGENPARTIJ VAN DE VERRICHTING;Details;Rekeningnummer"
    t1 = "2021-;11/10/2021;11/10/2021;-49.56;EUR;BETALING MET DEBETKAART         ;NUMMER 4871 04XX XXXX 5045 DELHAIZE KEERBER  KEERBERGE 11/10/2021 BANKREFERENTIE : 2110111359116911 VALUTADATUM : 11/10/2021;BE50001582721718"
    t2 = "2021-0075;10/10/2021;10/10/2021;-4.00;EUR;BETALING MET DEBETKAART         ;NUMMER 4871 04XX XXXX 5045 PARKING FP 1      ZAVENTEM 10/10/2021 BANKREFERENTIE : 2110100902573683 VALUTADATUM : 10/10/2021;BE50001582721718"
    t3 = "2021-0074;09/10/2021;09/10/2021;-205.86;EUR;BETALING MET DEBETKAART         ;NUMMER 4871 04XX XXXX 5045 BRUSSELS AIRLINE  ZAVENTEM 09/10/2021 BANKREFERENTIE : 2110091631435778 VALUTADATUM : 09/10/2021;BE50001582721718"

    c1 = CsvDataBank(n, t1)
    c2 = CsvDataBank(n, t2)
    c3 = CsvDataBank(n, t3)

    list = [c1, c2, c3]
    print(list)
    list.sort(key= lambda  x: x.sortBedrag("Bedrag"))
    print(list)
