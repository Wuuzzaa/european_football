class Spiel:
    def __init__(self, id, liga, datum, team_heim, team_gast, tore_heim, tore_gast, gewinner, quote_heimsieg,
                 quote_unentschieden, quote_gastsieg):
        self.id = id
        self.liga = liga
        self.team_heim = team_heim
        self.team_gast = team_gast
        self.datum = datum
        self.tore_heim = tore_heim
        self.tore_gast = tore_gast
        self.gewinner = gewinner  # H - Heim, A - Gast, D - Unentschieden
        self.quote_heimsieg = quote_heimsieg
        self.quote_unentschieden = quote_unentschieden
        self.quote_gastsieg = quote_gastsieg
        self.min_quote = min(quote_gastsieg, quote_heimsieg, quote_unentschieden)
        self.quote_tipp_korrekt = self.bestimme_quote_tipp_korrekt()

    def bestimme_quote_tipp_korrekt(self):
        if self.gewinner == "H":
            return self.quote_heimsieg

        elif self.gewinner == "D":
            return self.quote_unentschieden

        elif self.gewinner == "A":
            return self.quote_gastsieg

    def __str__(self):
        return '##########\n' \
               'ID: {}\n' \
               'Liga: {}\n' \
               'Team Heim: {}\n' \
               'Team Gast: {}\n' \
               'Datum: {}\n' \
               'Tore Heim: {}\n' \
               'Tore Gast: {}\n' \
               'Gewinner: {}\n' \
               'Quote Heimsieg: {}\n' \
               'Quote Unentschieden: {}\n' \
               'Quote Gastsieg: {}\n' \
               'Quote minimal: {}\n' \
               '##########\n'.format\
                (self.id, self.liga,self.team_heim, self.team_gast, self.datum,self.tore_heim, self.tore_gast,
                 self.gewinner, self.quote_heimsieg, self.quote_unentschieden, self.quote_gastsieg, self.min_quote)