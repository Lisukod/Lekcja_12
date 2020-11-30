from sys import argv
from os import listdir
from os.path import exists, isfile, join
import csv, json

src = argv[1]
dst = argv[2]


class Reader:
    def __init__(self, filesource, filedest):
        self.filesource = "./csv_origin/{}".format(filesource)
        self.filedest = "./edited/{}".format(filedest)
        self.csvList = []
        try:
            self.csvFile = open(self.filesource)
        except FileNotFoundError:
            print("Błąd. Podana ścieżka nie istnieje")
            exit()
        except OSError:
            print("Nie można otworzyć pliku: ", self.filesource)
            exit()
        if dst.endswith(".csv"):
            self.gotCSV()
        elif dst.endswith(".pickle") or dst.endswith(".json"):
            self.gotPickleOrJSon()

    def __del__(self):
        try:
            self.csvFile.close()
        except AttributeError:
            pass

    def makeTempList(self):
        csv_reader = csv.reader(self.csvFile)
        for line in csv_reader:
            self.csvList.append(line)

        for change in argv[3:]:
            change = change.split(",")
            Y = int(change[0])
            X = int(change[1])
            value = change[2]
            self.csvList[Y][X] = value

    def gotCSV(self):
        with open(self.filedest, "w") as new_csv:
            csv_writer = csv.writer(new_csv)
            self.makeTempList()
            for line in self.csvList:
                csv_writer.writerow(line)

    def gotPickleOrJSon(self):
        with open(self.filedest, "w") as new_json:
            self.makeTempList()
            json.dump(self.csvList, new_json)


Reader(argv[1], argv[2])
