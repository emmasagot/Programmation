import sys
import math
import numpy as np
import matplotlib.pyplot as plt
import datetime

# définition des variables
variables = {
    "bruit": "noise",
    "température": "temp",
    "humidité": "hum",
    "luminosité": "lum",
    "co2": "co2",
    "humidex": "humidex"
}

if __name__ == "__main__":
    args = sys.argv[1:]
    args.reverse()
    if len(args) < 2:
        print("nombre", len(args), "insuffisant de variables")
        sys.exit()
    action = args.pop()
    if action == "display" or action == "displayStat":
        variable = args.pop()
        try:
            column = variables[variable]
        except:
            print("variable", variable, "non soutenue")
            sys.exit()
    elif action == "corrélation":
        if len(args) < 2:
            print("nombre", len(args), "insuffisant de variables pour corrélation")
            sys.exit()
        variable1 = args.pop()
        variable2 = args.pop()
        try:
            column1 = variables[variable1]
            column2 = variables[variable2]
        except:
            print("l'une des variables", variable1, variable2, "non soutenue")
            sys.exit()
    else:
        print("action", action, "non soutenue")
        sys.exit()
    dateintervalset = False
    if len(args) == 2:
        start_date = datetime.datetime.fromisoformat(args.pop())
        end_date = datetime.datetime.fromisoformat(args.pop() + " 23:59:59")
        dateintervalset = True


# importation du ficher csv
try:
    fname = "EIVP_KM.csv"
    dtype1 = np.dtype([("index", "i4"), ("id", "i4"), ("noise", "f4"), ("temp", "f4"),
                       ("hum", "f4"), ("lum", "i4"), ("co2", "i4"), ("time", "M8[m]")])
    data = np.loadtxt(fname, dtype=dtype1, delimiter=";", skiprows=1)
except Exception as exep:
    print(exep)
    sys.exit()


# définition de l'intervalle temporel à l'aide du module datetime
if dateintervalset:
    boolfilter = (data["time"] >= start_date) & (data["time"] <= end_date)
    times = data["time"][boolfilter]
    ids = data["id"][boolfilter]
else:
    times = data["time"]
    ids = data["id"]


# calcul et affichage de l'indice Humidex
if action == "display" and variable == "humidex":
    if dateintervalset:
        temps = data["temp"][boolfilter]
        hums = data["hum"][boolfilter]
    else:
        temps = data["tmep"]
        hums = data["hum"]

    def CalculateHumidex(T, RH):
        b = 18.678
        c = 257.14
        alpha = math.log(RH/100) + (b*T / (c + T))
        Tdp = c * alpha / (b - alpha)
        H = T + (5/9) * (6.11 * math.exp(5417.7530 *
                                         (1/273.16 - 1/(273.15 + Tdp))) - 10)
        return H

    values = []
    for (temp, hum) in zip(temps, hums):
        values.append(CalculateHumidex(temp, hum))

    values = np.array(values)

    # plot
    uniqueids = set(ids)
    legend = []
    for id in uniqueids:
        plt.plot(times[ids == id], values[ids == id])
        legend.append("id {0}".format(id))

    plt.legend(legend)
    plt.xlabel("temps")
    plt.ylabel("humidex")
    plt.title("l'indice humidex")

# calcul et affichage des indicateurs statistiques
elif action == "display" or action == "displayStat":
    if dateintervalset:
        values = data[column][boolfilter]
    else:
        values = data[column]

    # plot
    uniqueids = set(ids)
    legend = []
    for id in uniqueids:
        plt.plot(times[ids == id], values[ids == id])
        legend.append("id {0}".format(id))

    plt.legend(legend)
    plt.xlabel("temps")
    plt.ylabel(variable)
    plt.title(variable)

    if action == "displayStat":
        def plotpoints(value, format):
            indices = np.where(values == value)
            itimes = times[indices]
            yaxis = np.empty(len(itimes))
            yaxis.fill(value)
            plt.plot(itimes, yaxis, format)

        plotpoints(np.min(values), "bo")
        plotpoints(np.max(values), "ro")

        # moyenne
        mean = np.mean(values)
        plt.plot([times[0], times[-1]], [mean, mean])
        plt.annotate("moyenne", xy=(times[0], mean))
        # médiane
        median = np.median(values)
        plt.plot([times[0], times[-1]], [median, median])
        plt.annotate("médiane", xy=(times[0], median))
        # écart-type
        # std = np.std(values)
        # plt.plot([times[0], times[-1]], [std, std])
        # plt.annotate("écart-type", xy=(times[0], std))
        # variance
        # var = np.var(values)
        # plt.plot([times[0], times[-1]], [var, var])
        # plt.annotate("variance", xy=(times[0], var))

        plt.title("Statistiques pour {0}".format(variable))
else:
    # Corrélation
    if dateintervalset:
        values1 = data[column1][boolfilter]
        values2 = data[column2][boolfilter]
    else:
        values1 = data[column1]
        values2 = data[column2]

    # indice de corrélation
    corrcoef = np.corrcoef(values1, values2)
    print("indice de corrélation entre", variable1,
          "et", variable2, ":", corrcoef[0][1])

    # plot
    fig, ax1 = plt.subplots()
    color = "tab:red"
    ax1.set_xlabel("temps")
    ax1.set_ylabel(variable1, color=color)

    uniqueids = set(ids)
    for id in uniqueids:
        ax1.plot(times[ids == id], values1[ids == id], color=color)

    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # ajout d'un second axe partageant le même abscisse

    color = "tab:blue"
    # l'ax1 garde le même nom que précemment
    ax2.set_ylabel(variable2, color=color)

    for id in uniqueids:
        ax2.plot(times[ids == id], values2[ids == id], color=color)

    ax2.tick_params(axis="y", labelcolor=color)

    fig.tight_layout()  # empêche la troncature de l'intitulé

    plt.title("l'indice de corrélation entre {0} et {1}: {2}".format(
        variable1, variable2, corrcoef[0][1]))

plt.show()
