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

print(max(normal5) * 100, sum(normal5) / len(normal5) * 100)
print(max(normal10) * 100, sum(normal10) / len(normal10) * 100)
print(max(normal13) * 100, sum(normal13) / len(normal13) * 100)
print(max(inflated5) * 100, sum(inflated5) / len(inflated5) * 100)
print(max(inflated10) * 100, sum(inflated10) / len(inflated10) * 100)
print(max(inflated13) * 100, sum(inflated13) / len(inflated13) * 100)
