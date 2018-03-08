from random import shuffle

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import itertools
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


def kombiwetten_erzeugen_zufaellig(spiele, einsatz_pro_wette, anzahl_tipps_je_wette):
    """
    Erzeugt zufällige Kombiwetten aus allen übergebenen Spielen
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


def kombiwetten_erzeugen_combinations(spiele, einsatz_pro_wette, anzahl_tipps_je_wette):
    #x = [1, 2, 3]
    #print(list(itertools.combinations(x, 2)))

    print(list(itertools.combinations(spiele, anzahl_tipps_je_wette)))


def monte_carlo_simulation(spiele, anzahl_simulationen, einsatz, spiele_pro_wette):
    gewinne = []

    for i in range(anzahl_simulationen):
        gewinn = 0

        # Wette erzeugen
        wetten = kombiwetten_erzeugen_zufaellig(spiele, einsatz, spiele_pro_wette)

        for wette in wetten:
            gewinn += wette.gewinn

        gewinne.append(gewinn)

    return gewinne


def simulation_plotten(gewinne, ist_sortiert=True, extremwertfilter=0.1):
    """
    Gibt einen Plott über den Gewinnverlauf einer Simulation aus mit Min-, Mittel- und Maximalem- Gewinn
    :param gewinne: Gewinne die geplottet werden sollen
    :param ist_sortiert: Soll der Plott aufsteigend sortiert sein?
    :param extremwertfilter: Wie viel Prozent sollen gefiltert werden. z.B. 0.1 bedeutet die untersten 10%
    und obersten 10% werden gefiltert. WICHTIG wird nur verwendet falls ist_sortiert = True
    :return:
    """
    # Gewinne sollen sortiert geplottet werden?
    if ist_sortiert:
        y = sorted(gewinne)

        # Extremwerte filtern
        if extremwertfilter > 0:
            filteranzahl = int(len(y) * extremwertfilter)

            y = y[filteranzahl: len(y) - filteranzahl]
    else:
        y = gewinne

    x = [x for x in range(len(y))]

    plt.plot(x, y, )

    # Verlust und Gewinnbereich farbig markieren
    if ist_sortiert:
        gewinnschwelle_x = -1
        for i in range(len(y)):
            if y[i] >= 0:
                gewinnschwelle_x = i
                break

        # Verlustfälle
        plt.fill_between(x[:gewinnschwelle_x], y[:gewinnschwelle_x], 0, color='red', alpha=.2)
        # Gewinnfälle
        plt.fill_between(x[gewinnschwelle_x:], y[gewinnschwelle_x:], 0, color='green', alpha=.2)

    plt.xlabel('Simulationsnummer')
    plt.ylabel('Gewinn')
    plt.title('Gewinnverteilung')

    # Minimaler Gewinn, Mittelwert, Maximaler Gewinn
    red_patch = mpatches.Patch(color='red', label='Minimaler Gewinn: {}'.format(round(min(y), 2)))
    blue_patch = mpatches.Patch(color="blue", label="Mittlerer Gewinn: {}".format(round(sum(y)/len(y), 2)))
    green_patch = mpatches.Patch(color="green", label="Maximaler Gewinn: {}".format(round(max(y), 2)))

    plt.legend(handles=[red_patch, blue_patch, green_patch], loc=0)  # loc= 0 heißt die Location wird automatisch ausgewählt, sodass sie optimal passt siehe https://matplotlib.org/api/legend_api.html

    plt.grid(True)
    plt.show()


def bestimme_beste_parameter(spiele_ungefiltert, min_kombinationen, max_kombinationen, quotenart, min_quote, max_quote, quoten_step, simulationen_anzahl, einsatz):
    ergebnisse = []
    untere_quote = round(min_quote, 2)
    obere_quote = round(min_quote + quoten_step, 2)

    # Vorfiltern mit min und max quote -> schnelleres "detailfiltern"
    spiele_ungefiltert = spiele_filtern_min_quote(spiele_ungefiltert, min_quote, max_quote)

    # Min -> Max KOMBINATIONEN
    for kombinationen_anzahl in range(min_kombinationen, max_kombinationen+1):
        # Min -> Max MAXQUOTE
        while obere_quote <= max_quote:
            # Min -> Max MINQUOTE
            while untere_quote <= max_quote:
                print("Aktuelle Berechnung: Kombinationen: {}, Unterequote: {}, Oberequote: {}".format(kombinationen_anzahl, untere_quote, obere_quote))

                # Sicherstellen, dass Untere Quote kleiner gleich als Obere Quote ist
                if untere_quote > obere_quote:
                    break

                spiele_gefiltert = spiele_filtern_min_quote(spiele_ungefiltert, untere_quote, obere_quote)
                gewinne = monte_carlo_simulation(spiele_gefiltert, simulationen_anzahl, einsatz, kombinationen_anzahl)
                ergebnisse.append((kombinationen_anzahl, untere_quote, obere_quote, gewinne))
                untere_quote += quoten_step
                untere_quote = round(untere_quote, 2)

            obere_quote += quoten_step
            untere_quote = min_quote

            obere_quote = round(obere_quote, 2)
            untere_quote = round(untere_quote, 2)
        obere_quote = round(min_quote + quoten_step, 2)
    # Auswerten

    ergebnisse.sort(key=lambda x: sum(x[3]), reverse=True)  # der key=lambda.... sorgt dafür, das nur die summe der Gewinne als sortierargument dient
    for ergebniss in ergebnisse:
        print("Kombinationen: {}, Minquote: {}, Maxquote: {}, Durchschnittlichergewinn: {}".format(ergebniss[0], ergebniss[1], ergebniss[2], round(sum(ergebniss[3]) / len(ergebniss[3]), 2)))

###
# MAIN START
###

spiele = spiele_auslesen()
spiele = spiele_filtern_min_quote(spiele, 1.7, 1.9)
datenanalyse_absolute_haeufigkeit_quoten(spiele, "MIN")
#kombiwetten_erzeugen_combinations(spiele, 5, 3)
gewinne = monte_carlo_simulation(spiele, 10000, 5, 3)
simulation_plotten(gewinne, True, 0)
#bestimme_beste_parameter(spiele, 1, 4, "MIN", 1, 1.9, 0.05, 250, 5)







