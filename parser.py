import json

class Parser:

    def __init__(self, input_data):
        self.input = input_data
        self.data = json.loads(self.input['d']['data'])['BasicCodes']

        # parse out data into manageable chunks
        # we have the following keys
        # [u'HHR',  # data type, match or ticket?
        #  u'CURRENCIES', # currency, USD or BRL
        #  u'STCONV', # some kind of action types...
        #  u'TSTMQ', # product codes for all the possible matches
        #  u'VENUES', # stadiums
        #  u'TEAMS', # the 32 teams
        #  u'TVALUES', # transaction actions
        #  u'COLVENUES', # simpler stadium names for columns in the table
        #  u'PRODUCTS', # all the tickets.
        #               VST: venue specific (all matches for that stadium)
        #               IMT: individual match tickets (one match, we want this)
        #               TST: team specific, we don't care
        #  u'MINCOMP',
        #  u'PRODUCTPRICES', # prices, and different sections of products.
        #                       has number of tickets also
        #  u'COLCENTRES',  # venue information, address, airport...
        #  u'COUNTRIESORG', # all the countries in the world, phone code
        #                   fee...
        #  u'ROUNDS',  # all the rounds, round of 16, etc...
        #  u'CATEGORIES'] # ticket categories, want Category 1
        self.teams = self.data['TEAMS']
        self.team_by_name = {}
        for team in self.teams:
            self.team_by_name[team['TeamName']] = team

        self.products = self.data['PRODUCTS']
        self.tickets = self.data['PRODUCTPRICES']

    def find_product_by_teams(self, home_team, away_team, prod_type='IMT'):
        home_team_id = self.team_by_name[home_team]['TeamId']
        away_team_id = self.team_by_name[away_team]['TeamId']
        return ([p for p in self.products
            if p.get('MatchHomeTeamId') == home_team_id and
               p.get('MatchAwayTeamId') == away_team_id and
               p.get('ProductTypeCode') == prod_type])

    def find_ticket_by_product_id(self, product_id, category_name):
        return ([t for t in self.tickets
            if t['PRPProductId'] == product_id and
               t['CategoryName'] == category_name])
