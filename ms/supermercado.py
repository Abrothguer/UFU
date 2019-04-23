import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import colors
import statistics as stc
import math
import numpy as npy
import pandas as pd


def read_data(filename="market-data.txt"):
    """
        Reads data from file
    """
    with open(filename, "r") as market_file:
        market_data = market_file.read().strip().split('\n')
    return list(map(int, market_data))


def default_analysis(data):
    pass


def outlier_analysis(data):

    print("Analise dos Outliers:\n\n")
    data_copy = data.copy()
    data_copy.sort()

    qt1 = data_copy[int(len(data) / 4) - 1]
    qt3 = data_copy[int(len(data) * 3 / 4) - 1]
    qrng = qt3 - qt1

    print(f"Quartil 1: {qt1}")
    print(f"Quartil 3: {qt3}")
    print(f"Amplitude interquartil: {qrng}")

    ext_out = [val for val in data if val < (qt1 - qrng * 3) or val > (qt3 + qrng * 3)]
    mod_out = [val for val in data if val < (qt1 - qrng * 1.5) or val > (qt3 + qrng * 1.5)]

    print(f"Outliers moderados: {mod_out}")
    print(f"Outliers extremos: {ext_out}")
    input("Pressione Enter para mostrar o grafico boxplot")

    fig = plt.figure(figsize=(10, 6))
    bxpt1 = fig.add_subplot(131)
    bxpt2 = fig.add_subplot(132)
    bxpt3 = fig.add_subplot(133)

    bxpt1.boxplot(data)
    bxpt1.set_title("Dados Brutos")

    bxpt2.boxplot([val for val in data if val not in mod_out])
    bxpt2.set_title("Sem Outliers Moderados")

    bxpt3.boxplot([val for val in data if val not in ext_out])
    bxpt3.set_title("Sem Outliers Extremos")

    plt.show()
    print("\nAs proximas analises serao feitas desconsiderando os outliers extremos...\n")
    return [val for val in data if val not in ext_out]


def correlation_analysis(data):

    print("Analise de correlacao:\n\n")
    xarr = data[:-1]
    yarr = data[1:]

    plt.scatter(xarr, yarr, label="Grafico de Dispersao")
    plt.show()


def inference_analysis(data):

    print("Inferencias:\n\n")

    kcls = round(1 + 3.3 * math.log10(len(data)))
    csize = (max(data) - min(data)) / kcls
    bins = [x * csize for x in range(kcls)]
    bins.append(max(data))

    hist = plt.hist(data, bins, histtype='bar')
    patches = hist[2]

    fracs = [val / max(bins) for val in bins]
    norm = colors.Normalize(min(fracs), max(fracs))

    for frac, patch in zip(fracs, patches):
        color = plt.cm.viridis(norm(frac))  # pylint: disable = E1101
        patch.set_facecolor(color)

    plt.title(f"Histograma da amostra: {kcls} Classes de tamanho {csize:.2}.")
    plt.show()


def adherence_analysis(data):

    print("Analise de Aderencia:\n\n")


def main():
    """
        Main function
    """
    nm_market_data = read_data()

    default_analysis(nm_market_data)
    nm_market_data = outlier_analysis(nm_market_data)
    print(nm_market_data)

    # correlation_analysis(nm_market_data)
    inference_analysis(nm_market_data)


if __name__ == "__main__":
    main()
