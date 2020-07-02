import matplotlib.pyplot as plt
import csv

x_16165 = []
y_16165 = []

with open('CSV/16165inflated.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x_16165.append(int(row[0]))
        y_16165.append(int(row[1]))

x_161610 = []
y_161610 = []

with open('CSV/161610inflated.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x_161610.append(int(row[0]))
        y_161610.append(int(row[1]))

x_161613 = []
y_161613 = []

with open('CSV/161613inflated.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x_161613.append(int(row[0]))
        y_161613.append(int(row[1]))

x_32325 = []
y_32325 = []

with open('CSV/32325inflated.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x_32325.append(int(row[0]))
        y_32325.append(int(row[1]))

x_323210 = []
y_323210 = []

with open('CSV/323210inflated.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x_323210.append(int(row[0]))
        y_323210.append(int(row[1]))

x_323213 = []
y_323213 = []

with open('CSV/323213inflated.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x_323213.append(int(row[0]))
        y_323213.append(int(row[1]))

x_64645 = []
y_64645 = []

with open('CSV/64645inflated.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x_64645.append(int(row[0]))
        y_64645.append(int(row[1]))

x_646410 = []
y_646410 = []

with open('CSV/646410inflated.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x_646410.append(int(row[0]))
        y_646410.append(int(row[1]))

x_646413 = []
y_646413 = []

with open('CSV/646413inflated.csv', 'r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x_646413.append(int(row[0]))
        y_646413.append(int(row[1]))

plt.plot(x_16165, y_16165, label='16x16 5WP')
plt.plot(x_161610, y_161610, label='16x16 10WP')
plt.plot(x_161613, y_161613, label='16x16 13WP')
plt.plot(x_32325, y_32325, label='32x32 5WP')
plt.plot(x_323210, y_323210, label='32x32 10WP')
plt.plot(x_323213, y_323213, label='32x32 13WP')
plt.plot(x_64645, y_64645, label='64x64 5WP')
plt.plot(x_646410, y_646410, label='64x64 10WP')
plt.plot(x_646413, y_646413, label='64x64 13WP')
plt.xlabel('Number of agents')
plt.ylabel('Successful runs')
plt.title('WM* inflated')
plt.legend()
plt.tight_layout()
plt.ylim(bottom=0)
plt.savefig(fname="WMstarInflated")