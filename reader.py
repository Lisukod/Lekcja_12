from sys import argv
from os import listdir
from os.path import exists, isfile, join
import csv, json, pickle
from pathlib import Path

src = argv[1]
dst = argv[2]


class Reader:
    def __init__(self, filesource, filedest):
        self.filesource = "./csv_origin/{}".format(filesource)
        self.filedest = "./edited/{}".format(filedest)
        self.csvList = []
        try:
            if Path(self.filesource).suffix == ".pickle":
                self.sourceFile = open(self.filesource, "rb")
            else:
                self.sourceFile = open(self.filesource)
        except FileNotFoundError:
            print("Błąd. Podana ścieżka nie istnieje")
            exit()
        except OSError:
            print("Nie można otworzyć pliku: ", self.filesource)
            exit()
        if Path(self.filedest).suffix == ".csv":
            self.toCSV()
        elif Path(self.filedest).suffix == ".json":
            self.toJSon()
        elif Path(self.filedest).suffix == ".pickle":
            self.toPickle()

    def __del__(self):
        try:
            self.sourceFile.close()
        except AttributeError:
            pass

    def makeTempList(self):
        if Path(self.filesource).suffix == ".csv":
            file_reader = csv.reader(self.sourceFile)
        elif Path(self.filesource).suffix == ".json":
            file_reader = json.load(self.sourceFile)
        elif Path(self.filesource).suffix == ".pickle":
            file_reader = pickle.load(self.sourceFile)
        for line in file_reader:
            self.csvList.append(line)

        for change in argv[3:]:
            change = change.split(",")
            Y = int(change[0])
            X = int(change[1])
            value = change[2]
            self.csvList[Y][X] = value

    def toCSV(self):
        with open(self.filedest, "w") as new_csv:
            csv_writer = csv.writer(new_csv)
            self.makeTempList()
            for line in self.csvList:
                csv_writer.writerow(line)

    def toJSon(self):
        with open(self.filedest, "w") as new_json:
            self.makeTempList()
            json.dump(self.csvList, new_json)

    def toPickle(self):
        with open(self.filedest, "wb") as new_pickle:
            self.makeTempList()
            pickle.dump(self.csvList, new_pickle)


Reader(argv[1], argv[2])
