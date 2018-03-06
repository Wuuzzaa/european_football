from random import shuffle

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import plotly.plotly as py
import numpy as np
import xlrd

import Spiel
import Wette


def datenanalyse_absolute_haeufigkeit_quoten(spiele, quotenart):
    # Relevante Quoten auslesen
    quoten = []

    # HEIMQUOTE
    if quotenart == "H":
        for spiel in spiele:
            quoten.append(spiel.quote_heimsieg)
    # GASTQUOTE
    elif quotenart == "A":
        for spiel in spiele:
            quoten.append(spiel.quote_gastsieg)
    # UNENTSCHIEDENQUOTE
    elif quotenart == "D":
        for spiel in spiele:
            quoten.append(spiel.quote_unentschieden)
    # MINQUOTE
    elif quotenart == "MIN":
        for spiel in spiele:
            quoten.append(spiel.min_quote)

    # Quoten sortieren
    quoten.sort()

    # Absolute Häufigkeit bestimmen
    counts = {}
    for num in quoten:
        count = counts.get(num, 0)
        counts[num] = count + 1

    # Quartile bestimmen
    quantil_low = np.percentile(quoten, 25)
    quantil_median = np.percentile(quoten, 50)
    quantil_high = np.percentile(quoten, 75)

    # Plotten
    lists = sorted(counts.items())
    x, y = zip(*lists)  # unpack a list of pairs into two tuples

    plt.plot(x, y)
    plt.xlabel('Quote')
    plt.ylabel('Anzahl')
    plt.title('Quotenkeitsverteilung')

    # Patch (Quartil und Anzahl Datensätze)
    black_patch = mpatches.Patch(color="black", label="Anzahl Datensätze: {}".format(len(quoten)))
    red_patch = mpatches.Patch(color='red', label='Unteres Quartil: {}'.format(round(quantil_low, 2)))
    blue_patch = mpatches.Patch(color="blue", label="Median: {}".format(round(quantil_median, 2)))
    green_patch = mpatches.Patch(color="green", label="Oberes Quartil: {}".format(round(quantil_high, 2)))

    plt.legend(handles=[black_patch, red_patch, blue_patch, green_patch], loc=0)  # loc= 0 heißt die Location wird automatisch ausgewählt, sodass sie optimal passt siehe https://matplotlib.org/api/legend_api.html

    plt.grid(True)
    plt.show()


def spiele_auslesen():
    filename = "testbert.xlsx"

    # Datei öffnen und Tabelle auswählen
    workbook = xlrd.open_workbook(filename)
    tabelle = workbook.sheet_by_index(0)  # 0 da nur eine Seite in der Datei

    # Inhalt auslesen
    zeilen = []

    for i in range(tabelle.nrows):
        zeilen.append(tabelle.row_values(i))

    # Spiele anlegen
    spiele = []
    id = -1  # -1 da Kopfzeile entfernt werden muss (Div, Date, HomeTeam, AwayTeam...)

    for zeile in zeilen:
        spiele.append(Spiel.Spiel(id, zeile[0], zeile[1], zeile[2], zeile[3], zeile[4], zeile[5], zeile[6], zeile[7], zeile[8], zeile[9]))
        id += 1

    # Kopfzeile entfernen
    spiele = spiele[1:]
    return spiele


def spiele_filtern_min_quote(spiele, min_quote_minimal, min_quote_maximal):
    """
    Filtert anhand er minimalen Quote eines Spieles
    :param spiele:
    :param min_quote_minimal: Quote als Untere Grenze
    :param min_quote_maximal: Quote als Obere Grenze
    :return:
    """
    spiele = [spiel for spiel in spiele if min_quote_minimal <= spiel.min_quote <= min_quote_maximal]
    return spiele


def komibiwetten_erzeugen(spiele, einsatz_pro_wette, anzahl_tipps_je_wette):
    """
    Erzeugt Kombiwetten aus allen übergebenen Spielen
    :param spiele: Spiele auf die Tippbedingungen zutreffen - vorher filtern!
    :param einsatz_pro_wette: Geldeinsatz
    :param anzahl_tipps_je_wette: Wie viele Tipps bilden die Kombiwette
    :return: Liste von Wettscheinen
    """
    shuffle(spiele)

    wetten = []

    while len(spiele) > anzahl_tipps_je_wette:
        temp_spiele = spiele[0:anzahl_tipps_je_wette]
        tipps = []

        for i in range(anzahl_tipps_je_wette):
            tipps.append(temp_spiele[i].min_quote)

        wetten.append(Wette.Wette(temp_spiele, tipps, einsatz_pro_wette))
        spiele = spiele[anzahl_tipps_je_wette:]

    return wetten


def monte_carlo_simulation(spiele, anzahl_simulationen, einsatz, spiele_pro_wette):
    gewinne = []

    for i in range(anzahl_simulationen):
        gewinn = 0

        # Wette erzeugen
        wetten = komibiwetten_erzeugen(spiele, einsatz, spiele_pro_wette)

        for wette in wetten:
            gewinn += wette.gewinn

        # Wetten auswerten
        gewinne.append(gewinn)

    return gewinne


def simulation_plotten(gewinne, ist_sortiert=True):
    """
    Gibt einen Plott über den Gewinnverlauf einer Simulation aus mit Min-, Mittel- und Maximalem- Gewinn
    :param gewinne: Gewinne die geplottet werden sollen
    :param ist_sortiert: Soll der Plott aufsteigend sortiert sein?
    :return:
    """
    # Gewinne sollen sortiert geplottet werden?
    if ist_sortiert:
        y = sorted(gewinne)
    else:
        y = gewinne

    x = [x for x in range(len(gewinne))]

    plt.plot(x, y)
    plt.xlabel('Simulationsnummer')
    plt.ylabel('Gewinn')
    plt.title('Gewinnverteilung')

    # Minimaler Gewinn, Mittelwert, Maximaler Gewinn
    red_patch = mpatches.Patch(color='red', label='Minimaler Gewinn: {}'.format(round(min(gewinne),2)))
    blue_patch = mpatches.Patch(color="blue", label="Mittlerer Gewinn: {}".format(round(sum(gewinne)/len(gewinne), 2)))
    green_patch = mpatches.Patch(color="green", label="Maximaler Gewinn: {}".format(round(max(gewinne), 2)))

    plt.legend(handles=[red_patch, blue_patch, green_patch], loc=0)  # loc= 0 heißt die Location wird automatisch ausgewählt, sodass sie optimal passt siehe https://matplotlib.org/api/legend_api.html

    plt.grid(True)
    plt.show()


###
# MAIN START
###

spiele = spiele_auslesen()
datenanalyse_absolute_haeufigkeit_quoten(spiele, "MIN")
spiele = spiele_filtern_min_quote(spiele, 2.7, 3)

#datenanalyse_absolute_haeufigkeit_quoten(spiele, "MIN")
#gewinne = monte_carlo_simulation(spiele, 100, 5, 3)
#simulation_plotten(gewinne, False)








