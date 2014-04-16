import requests
import json
from parser import Parser

res = requests.get('https://fwctickets.fifa.com/TopsAkaCalls/Calls.aspx/getBasicData?l=en&c=OTH')
res.raise_for_status()
data = res.json()
parser = Parser(data)

products = parser.find_product_by_teams('Korea Republic', 'Belgium')
for prod in products:
    tickets = parser.find_ticket_by_product_id(prod['ProductId'], 'CAT1')
    for tic in tickets:
        if int(tic.get('Quantity')) > 0:
            print 'Buy this!'
            print prod
            print tic
        else:
            print 'Still nothing :('
            print prod
            print tic
