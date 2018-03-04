class Wette:
    def __init__(self, spiele, tipps, einsatz):
        self.spiele = spiele
        self.tipps = tipps  # Beinhaltet die Vorhersage über den Ausgang als Quoten (1.15, 1.5 , 1.1...)
        self.einsatz = einsatz
        self.quote = self.berechne_quote()
        self.ist_gewonnen = self.pruefe_ist_gewonnen()
        self.umsatz = self.berechne_umsatz()
        self.gewinn = self.berechne_gewinn()

    def berechne_quote(self):
        self.quote = 1

        for tipp in self.tipps:
            self.quote *= tipp

        return self.quote

    def pruefe_ist_gewonnen(self):
        """
        Wette gilt als Gewonnen, falls ALLE Tipps korrekt sind -> keine Teilgewinne oder ähnliches.
        :return:
        """
        for i in range(len(self.spiele)):
            if self.spiele[i].quote_tipp_korrekt != self.tipps[i]:
                return False

        return True

    def berechne_umsatz(self):
        if self.ist_gewonnen:
            return self.einsatz * self.quote

        else:
            return 0

    def berechne_gewinn(self):
        return self.berechne_umsatz() - self.einsatz