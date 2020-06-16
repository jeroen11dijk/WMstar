import csv

normal5 = []
normal10 = []
normal13 = []
inflated5 = []
inflated10 = []
inflated13 = []

with open('CSV/normal5.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    next(readCSV)
    for row in readCSV:
        normal5.append(int(row[6]) / int(row[5]))

with open('CSV/normal10.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    next(readCSV)
    for row in readCSV:
        normal10.append(int(row[6]) / int(row[5]))

with open('CSV/normal13.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    next(readCSV)
    for row in readCSV:
        normal13.append(int(row[6]) / int(row[5]))

with open('CSV/inflated5.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    next(readCSV)
    for row in readCSV:
        inflated5.append(int(row[6]) / int(row[5]))

with open('CSV/inflated10.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    next(readCSV)
    for row in readCSV:
        inflated10.append(int(row[6]) / int(row[5]))

with open('CSV/inflated13.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    next(readCSV)
    for row in readCSV:
        inflated13.append(int(row[6]) / int(row[5]))

print(sum(normal5) / len(normal5))
print(sum(normal10) / len(normal10))
print(sum(normal13) / len(normal13))
print(sum(inflated5) / len(inflated5))
print(sum(inflated10) / len(inflated10))
print(sum(inflated13) / len(inflated13))