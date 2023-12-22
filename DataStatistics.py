import os

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
# from matplotlib import ticker

if __name__=="__main__":

    # with open(f"{os.getcwd()}//gathered_data//labels_jarilo4_copy.txt","r") as file:
    with open(f"{os.getcwd()}//gathered_data//labels_herta_space_station.txt","r") as file:
        lines = file.readlines()

        new_lines = [line.replace("\n", "") for line in lines]

    print(new_lines)
    new_lines[3] = "antibaryon"
    dict1, dict2 = {}, {}
    for i, name in enumerate(new_lines):
        dict1[name] = i
        dict2[i] = name

    print("break")
    count = np.zeros(len(new_lines))
    print(count)

    files = os.listdir(f"{os.getcwd()}//gathered_data//train_data//labels//train")
    print(len(files))

    for z, fileName in enumerate(files):
        with open(f"{os.getcwd()}//gathered_data//train_data//labels//train//{fileName}", "r") as file:
            lines = file.readlines()
            for line in lines:
                splited = line.split(" ")
                count[int(splited[0])] += 1

    cmap = matplotlib.colormaps["rainbow"]
    colors = [cmap(i / len(new_lines)) for i in range(len(new_lines))]

    t = np.arange(len(count))
    print(new_lines)
    print(new_lines[::2])
    print(new_lines[1::2])
    pos1 = np.arange(len(new_lines[::2]))*2
    pos2 = np.arange(len(new_lines[1::2]))*2+1
    plt.bar(t, count, color=colors)
    plt.gca().autoscale(enable=True, axis='x')
    ax = plt.gca()
    ax.xaxis.set_minor_locator(matplotlib.ticker.FixedLocator(pos2))
    ax.xaxis.set_minor_formatter(matplotlib.ticker.FixedFormatter(new_lines[1::2]))
    ax.xaxis.set_major_locator(matplotlib.ticker.FixedLocator(pos1))
    ax.xaxis.set_major_formatter(matplotlib.ticker.FixedFormatter(new_lines[::2]))



    ax.tick_params(axis='x', which='minor', length=15)
    ax.tick_params(axis='x', which='both', color='lightgrey')
    ax.autoscale(enable=True, axis='x', tight=True)


    # plt.xticks(t, new_lines)
    # plt.bar(t, count)
    plt.grid(True)
    plt.title("Number of creatures of each class")
    plt.ylabel("count")
    plt.xlabel("class")
    figure = plt.gcf()
    figure.set_size_inches(15, 6)
    plt.savefig("Deeplearning figure2.png")
    plt.show()






