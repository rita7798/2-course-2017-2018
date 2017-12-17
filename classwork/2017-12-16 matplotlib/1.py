import matplotlib.pyplot as plt
import csv


def making_dictionary():
    d = {}
    with open('nanai-vowels.csv') as csvfile:
        filereader = csv.reader(csvfile, delimiter=';')
        for i in filereader:
            if i[2] in d:
                if i[3] in d[i[2]]:
                    d[i[2]][i[3]].append([float(i[4]), float(i[5])])
                else:
                    d[i[2]][i[3]] = [float(i[4]), float(i[5])]
            else:
                d[i[2]] = {i[3] : [float(i[4]), float(i[5])]}
    return d


def making_x_and_y(d):
    x = []
    y = []
    sum_f1 = 0
    sum_f2 = 0
    for j in d:
        for k in d[j]:
            l = len(d[j][k])
            for m in d[j][k]:
                sum_f1 += d[j][k][0]
                sum_f2 += d[j][k][1]
            avg_1 = sum_f1/l
            avg_2 = sum_f2/l
            x.append(avg_1)
            y.append(avg_2)
    return x,y


def making_graph(x,y):
    markers = ['o', 'o', 'o', '^', '^','^']
    for x, y, m in zip(x, y, markers):
        plt.scatter([x],[y], marker=m, s=100)
    plt.title("Средние значения формант")
    plt.xlabel("f1")
    plt.ylabel("f2")
    plt.savefig('plot.png')


def main():
    d = making_dictionary()
    x,y = making_x_and_y(d)
    making_graph(x,y)


if __name__ == "__main__":
    main()
