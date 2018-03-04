class Spiel:
    def __init__(self, id, liga, team_heim, team_gast, datum, tore_heim, tore_gast, gewinner, quote_heimsieg,
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
