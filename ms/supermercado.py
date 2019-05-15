"""
    Implementação dos exercícios feitos no capítulo 2 do livro Modelagem e Simulação de Eventos
    Discretos, utilizando a amostra de dados do supermercado
"""

import math
import matplotlib.pyplot as plt
from matplotlib import colors
from scipy.stats import chi2

KS_ALPHAS = {.2: 1.07, .1: 1.22, .05: 1.36, .02: 1.52, .01: 1.63}


def read_data(filename="market-data.txt"):
    """
        Le os dados de um arquivo
    """
    with open(filename, "r") as market_file:
        market_data = market_file.read().strip().split('\n')
    return list(map(int, market_data))


def outlier_analysis(data):
    """
        Faz a análise dos outliers e retorna os dados sem os outliers extremos
    """
    print("Analise dos Outliers:\n\n")
    data_copy = data.copy()
    data_copy.sort()

    # Calculo dos quartis e amplitude interquartil
    qt1 = data_copy[int(len(data) / 4) - 1]
    qt3 = data_copy[int(len(data) * 3 / 4) - 1]
    qrng = qt3 - qt1

    print(f"Quartil 1: {qt1}")
    print(f"Quartil 3: {qt3}")
    print(f"Amplitude interquartil: {qrng}")

    # Encontrando outliers moderados e extremos.
    ext_out = [val for val in data if val < (qt1 - qrng * 3) or val > (qt3 + qrng * 3)]
    mod_out = [val for val in data if val < (qt1 - qrng * 1.5) or val > (qt3 + qrng * 1.5)]

    print(f"Outliers moderados: {mod_out}")
    print(f"Outliers extremos: {ext_out}")

    # Plotando os boxplots para os dados brutos, dados sem outliers moderados e extremos.
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
    """
        Faz a análise de correlação e mostra o gráfico de dispersão
    """
    print("Analise de correlacao:\n\n")

    # Dois arrays para correlacao x = Ai ... An-1; y = A1 ... An
    xarr = data[:-1]
    yarr = data[1:]

    # Plotando o gráfico de dispersão
    plt.scatter(xarr, yarr, label="Grafico de Dispersao")
    plt.show()


def inference_analysis(data):
    """
        Faz a análise de inferência, divisão de classes e histograma
    """

    print("Inferencias:\n\n")

    # Calculo do nro de classes, tamanho das classes e divisórias para o histograma
    kcls = round(1 + 3.3 * math.log10(len(data)))
    csize = (max(data) - min(data)) / kcls
    bins = [x * csize for x in range(kcls)]
    bins.append(max(data))

    hist = plt.hist(data, bins, histtype='bar')
    patches = hist[2]

    # Colorindo o histograma
    fracs = [val / max(bins) for val in bins]
    norm = colors.Normalize(min(fracs), max(fracs))

    for frac, patch in zip(fracs, patches):
        color = plt.cm.viridis(norm(frac))  # pylint: disable = E1101
        patch.set_facecolor(color)

    # Divide os dados nas suas respectivas classes
    classes = [[x for x in data if x >= w and x < y] for w, y in
               [((z - 1) * csize, z * csize) for z in range(1, kcls + 1)]]

    # Retorna as classes, o nro de classes e o tamanho das classes
    print(f"\nNumero de classes: {kcls}")
    print(f"Tamanho das classes: {csize}")
    print(f"Valores para cada classe: \n")
    for clss in classes:
        print(clss)

    # Plota o histograma.
    plt.title(f"Histograma da amostra: {kcls} Classes de tamanho {csize:.2}.")
    plt.show()

    return (classes, kcls, csize)


def chi_squared_test(data, classes, alpha=.05):
    """
        Faz o teste do qui-quadrado, baseado no cálculo dos desvios das frequências observadas em
        cada classe e as frequências teóricas.
    """
    # H0: Adere a distribuição
    # H1: Não adere a distribuição
    print("\n\nAnalise de qui-quadrado:\n\n")

    # Parametro estimado da distribuiçao exponencial -> lambda = 1 / média
    exp_par = 1 / (sum(data) / len(data))

    # Coleta dos dados de classe. Tamanho, número e dados de cada classe.
    csize = classes[2]
    kcls = classes[1]
    classes = classes[0]

    # Probabilidade teórica de ocorrência das classes.
    prob_class = [-math.pow(math.e, -exp_par * b) + math.pow(math.e, -exp_par * a) for a, b in
                  [((z - 1) * csize, z * csize) for z in range(1, kcls + 1)]]

    # Distribuicao teórica das classes em uma distribuiçao exponencial.
    raw_theo_dist = [len(data) * prob for prob in prob_class]
    theo_dist = [dist for dist in raw_theo_dist if dist >= 5]

    # Agrupando frequencias teoricas menores que 5.
    theo_dist[-1] += sum([dist for dist in raw_theo_dist if dist < 5])
    theo_dist = list(map(round, theo_dist))
    print(f"Distribuicao teorica das classes:\n\t{theo_dist}\n")

    # Distribuicao observadas dos dados nas classes. Agrupamento
    raw_obsv_dist = [len(x) for x in classes]
    obsv_dist = [dist for dist in raw_obsv_dist if dist >= 5]
    obsv_dist[-1] += sum([dist for dist in raw_obsv_dist if dist < 5])
    print(f"Distribuicao observada das classes:\n\t{obsv_dist}\n")

    # Calcular qui = Soma de 1 a k de ((Oi-Ti)^2/Ti)
    # Oi: frequência observada
    # Ti: frequência esperada
    # k: numero de classes após agrupamento
    chi_found = sum([((obsv - theo)**2) / theo for obsv, theo in zip(obsv_dist, theo_dist)])
    print(f"Valor de qui calculado(Ek): {chi_found}")

    # Grau de liberdade = número de classes após agrupamento - 1 - parâmetros estimados (media)
    chi_df = len(theo_dist) - 1 - 1

    # Calcular qui esperado: nível de significância alpha e grau de liberdade chi_df
    chi_actual = chi2.isf(q=alpha, df=chi_df)
    print(f"Valor de qui tabelado(E): {chi_actual}")

    # Rejeita H0
    if chi_found >= chi_actual:
        print("\nA distribuicao dos dados nao adere a uma distribuicao exponencial\n\n")
    # Aceita H0
    else:
        print("\nA distribuicao dos dados adere a uma distribuicao exponencial\n\n")
    input("Pressione Enter para continuar")


def kolmogorov_smirnov_test(data, alpha=.05):  # pylint: disable = R0914
    """
        Faz o teste KS, comparando a função acumulada dos modelos teórico e observado, calculando a
        distância absoluta maxima entre as duas.
    """
    # H0: Adere a distribuição
    # H1: Não adere a distribuição
    print("Analise de Kolmogorov-Smirnov:\n\n")

    # Parametro estimado da distribuiçao exponencial -> lambda = 1 / média
    exp_par = 1 / (sum(data) / len(data))

    # Calculo da distribuicao de frequencia e distribuicao de frequencia acumulada.
    freq = [data.count(val) for val in range(max(data) + 1)]
    freq_ac = [sum(freq[:ind + 1]) for ind in range(len(freq))]

    # Calculo da funcao acumulada observada S(x) = eventos <= x / total de valores
    s_function = [fr / freq_ac[-1] for fr in freq_ac]

    # Calculo da funcao acumulada teórica F(x) = 1 - e^(-lambda*x) a esquerda e direita
    f_esq = [1 - math.pow(math.e, -exp_par * x) for x in range(len(freq))]
    f_dir = [1 - math.pow(math.e, -exp_par * x) for x in range(1, len(freq) + 1)]

    # Calculo da estatistica D a direita e a esquerda: F(x)-S(x)
    d_esq = [abs(esq - obsv) for esq, obsv in zip(f_esq, s_function)]
    d_dir = [abs(dir - obsv) for dir, obsv in zip(f_dir, s_function)]

    # Calcula da estatitica D: a maior entre a direita e esquerda
    d_max = list(map(max, zip(d_esq, d_dir)))

    print("Valor\tFrDados\tFrAcum\tS(x)\tF(x)esq\tF(x)dir\tDesq\tDdir\tDmax\n")
    for val, dfr, acm, sfx, fex, fdx, fde, fdd, fdm in zip(
            range(len(freq)), freq, freq_ac, s_function, f_esq, f_dir, d_esq, d_dir, d_max):
        print(f"{val}\t{dfr}\t{acm}\t{sfx:.3f}\t{fex:.3f}" +
              f"\t{fdx:.3f}\t{fde:.3f}\t{fdd:.3f}\t{fdm:.3f}\t")

    # Calculo da distancia encontrada: max(d_max)
    dist_found = max(d_max)
    print(f"\n\nMaior distancia encontrada: {dist_found}")
    # Calculo da distancia critica: 1.36/sqrt(n) 1.36 caso alpha = 0.5
    dist_actual = KS_ALPHAS[alpha] / math.sqrt(len(data))
    print(f"Distancia critica: {dist_actual}\n")

    # Rejeita H0
    if dist_found > dist_actual:
        print("\nA distribuicao dos dados nao adere a uma distribuicao exponencial\n\n")
    # Aceita H0
    else:
        print("\nA distribuicao dos dados adere a uma distribuicao exponencial\n\n")


def main():
    """
        Main function
    """
    nm_market_data = read_data()
    nm_market_data = outlier_analysis(nm_market_data)
    correlation_analysis(nm_market_data)
    classes = inference_analysis(nm_market_data)
    chi_squared_test(nm_market_data, classes)
    kolmogorov_smirnov_test(nm_market_data)


if __name__ == "__main__":
    main()
