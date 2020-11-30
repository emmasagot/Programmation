import sys

import numpy as np

import matplotlib.pyplot as plt

import datetime



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

        exit()

    action = args.pop()

    if action == "display" or action == "displayStat":

        variable = args.pop()

        try:

            column = variables[variable]

        except:

            print("variable", variable, "non soutenue")

            exit()

    elif action == "corrélation":

        if len(args) < 2:

            print("nombre", len(args), " insuffisant de variables pour corrélation")

            exit()

        variable1 = args.pop()

        variable2 = args.pop()

        try:

            column1 = variables[variable1]

            column2 = variables[variable2]

        except:

            print("l'une des variables", variable1, variable2, "non soutenue")

            exit()

    else:

        print("action", action, "non soutenue")

        exit()

    dateintervalset = False

    if len(args) == 2:

        start_date = datetime.datetime.fromisoformat(args.pop())

        end_date = datetime.datetime.fromisoformat(args.pop() + " 23:59:59")

        dateintervalset = True




# load csv file data into data variable

try:

    fname = "/Users/mac/Desktop/EIVP/Algo et programmation/EIVP_KM.csv"

    dtype1 = np.dtype([("id", "i4"), ("day", "i4"), ("noise", "f4"), ("temp", "f4"),

                       ("hum", "f4"), ("lum", "i4"), ("co2", "i4"), ("time", "M8[m]")])

    data = np.loadtxt(fname, dtype=dtype1, delimiter=";", skiprows=1)

except Exception as exep:

    print(exep)

    exit()



# filter values if interval is set

if action != "corrélation":

    if dateintervalset:

        boolfilter = (data["time"] >= start_date) & (data["time"] <= end_date)

        times = data["time"][boolfilter]

        values = data[column][boolfilter]

    else:

        times = data["time"]

        values = data[column]



    # plot

    plt.plot(times, values)

    plt.xlabel("temps")

    plt.ylabel(variable)



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

    if dateintervalset:

        boolfilter = (data["time"] >= start_date) & (data["time"] <= end_date)

        times = data["time"][boolfilter]

        values1 = data[column1][boolfilter]

        values2 = data[column2][boolfilter]

    else:

        times = data["time"]

        values1 = data[column1]

        values2 = data[column2]



    # indice de corrélation

    corrcoef = np.corrcoef(data[column1][boolfilter],

                           data[column2][boolfilter])

    print(corrcoef)



    # plot

    fig, ax1 = plt.subplots()



    color = "tab:red"

    ax1.set_xlabel("temps")

    ax1.set_ylabel(variable1, color=color)

    ax1.plot(times, values1, color=color)

    ax1.tick_params(axis='y', labelcolor=color)



    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis



    color = "tab:blue"

    # we already handled the x-label with ax1

    ax2.set_ylabel(variable2, color=color)

    ax2.plot(times, values2, color=color)

    ax2.tick_params(axis="y", labelcolor=color)



    fig.tight_layout()  # otherwise the right y-label is slightly clipped



    plt.title("l'indice de corrélation entre {0} et {1}: {2}".format(

        variable1, variable2, corrcoef[0][1]))



plt.show()





def getHumidex(t, d):

    kelvin = 273.15

    temperature = t+kelvin

    dewpoint = d+kelvin

    # Calculate vapor pressure in mbar.

    e = 6.11 * math.exp(5417.7530 * ((1 / kelvin) - (1 / dewpoint)))

    # Calculate saturation vapor pressure

    es = 6.11 * math.exp(5417.7530 * ((1 / kelvin) - (1 / temperature)))

    humidity = e / es

    h = 0.5555 * (e - 10.0)

    humidex = temperature + h - kelvin

    return humidex

