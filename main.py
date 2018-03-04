import xlrd
import Spiel
import Wette
from random import shuffle


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


def wetten_erzeugen(spiele, einsatz_pro_wette, anzahl_tipps_je_wette):
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


spiele = spiele_auslesen()
#print(len(spiele))
spiele = spiele_filtern_min_quote(spiele, 1.7, 1.8)
print(len(spiele))

#for i in range(5):
    #print(spiele[i])


#Monte Carlo Simulation
gewinn = 0
anzahl_simulationen = 10000

for i in range(anzahl_simulationen):
    # Wette erzeugen
    wetten = wetten_erzeugen(spiele, 5, 3)

    for wette in wetten:
        gewinn += wette.gewinn

print("Gewinn: {}".format(gewinn / anzahl_simulationen))




