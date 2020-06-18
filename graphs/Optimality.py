import csv

normal5 = []
normal10 = []
normal13 = []
normal79 = []
normal80 = []
normal81 = []
normal82 = []
inflated5 = []
inflated10 = []
inflated13 = []
inflated79 = []
inflated80 = []
inflated81 = []
inflated82 = []

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

with open('CSV/normal79.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    next(readCSV)
    for row in readCSV:
        normal79.append(int(row[6]) / int(row[5]))

with open('CSV/normal80.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    next(readCSV)
    for row in readCSV:
        normal80.append(int(row[6]) / int(row[5]))

with open('CSV/normal81.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    next(readCSV)
    for row in readCSV:
        normal81.append(int(row[6]) / int(row[5]))

with open('CSV/normal82.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    next(readCSV)
    for row in readCSV:
        normal82.append(int(row[6]) / int(row[5]))

with open('CSV/inflated79.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    next(readCSV)
    for row in readCSV:
        inflated79.append(int(row[6]) / int(row[5]))

with open('CSV/inflated80.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    next(readCSV)
    for row in readCSV:
        inflated80.append(int(row[6]) / int(row[5]))

with open('CSV/inflated81.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    next(readCSV)
    for row in readCSV:
        inflated81.append(int(row[6]) / int(row[5]))

with open('CSV/inflated82.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    next(readCSV)
    for row in readCSV:
        inflated82.append(int(row[6]) / int(row[5]))

print(max(normal5) * 100, sum(normal5) / len(normal5) * 100)
print(max(normal10) * 100, sum(normal10) / len(normal10) * 100)
print(max(normal13) * 100, sum(normal13) / len(normal13) * 100)
print(max(normal79) * 100, sum(normal79) / len(normal79) * 100)
print(max(normal80) * 100, sum(normal80) / len(normal80) * 100)
print(max(normal81) * 100, sum(normal81) / len(normal81) * 100)
print(max(normal82) * 100, sum(normal82) / len(normal82) * 100)

print(max(inflated5) * 100, sum(inflated5) / len(inflated5) * 100)
print(max(inflated10) * 100, sum(inflated10) / len(inflated10) * 100)
print(max(inflated13) * 100, sum(inflated13) / len(inflated13) * 100)
print(max(inflated79) * 100, sum(inflated79) / len(inflated79) * 100)
print(max(inflated80) * 100, sum(inflated80) / len(inflated80) * 100)
print(max(inflated81) * 100, sum(inflated81) / len(inflated81) * 100)
print(max(inflated82) * 100, sum(inflated82) / len(inflated82) * 100)
