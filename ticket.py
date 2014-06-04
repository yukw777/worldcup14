import requests
import json
from parser import Parser
from email_sender import Email
from config import conf
import time
import logging

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.INFO)
while True:
    res = requests.get('https://fwctickets.fifa.com/TopsAkaCalls/Calls.aspx/getBasicData?l=en&c=OTH')
    if res.ok:
        break
    else:
        logging.info('sleep for 5 seconds and retry')
        time.sleep(5)
data = res.json()
parser = Parser(data)

def find_tickets(team1, team2, categories=['CAT1', 'CAT2', 'CAT3']):
    products = parser.find_product_by_teams(team1, team2)
    for prod in products:
        tickets = []
        for cat in categories:
            tickets.extend(
                parser.find_ticket_by_product_id(prod['ProductId'], cat))
        for tic in tickets:
            if int(tic.get('Quantity')) > 0:
                msg = json.dumps({'product': prod}, indent=4)
                msg += '\n\n'
                msg += json.dumps({'ticket': tic}, indent=4)
                for email in conf['email_list']:
                    Email.send_email(
                        email,
                        ('Ticket Available! (%s vs %s, %s)' %
                            (team1, team2, tic['CategoryName'])),
                        msg
                    )
                logging.info('Tickets found! (%s vs %s, %s) Email sent' %
                    (team1, team2, tic['CategoryName']))
            else:
                logging.info('No tickets :( (%s vs %s, %s) Email not sent' %
                    (team1, team2, tic['CategoryName']))

# Korea Republic vs Belgium
find_tickets('Korea Republic', 'Belgium', categories=['CAT1'])

# Belgium vs Russia
find_tickets('Belgium', 'Russia')

# Ecuador vs France
#find_tickets('Ecuador', 'France')

# Argentina v Bosnia-Herzegovina
find_tickets('Argentina', 'Bosnia-Herzegovina')

# Ghana v USA
find_tickets('Ghana', 'USA')

# Spain v Chile
find_tickets('Spain', 'Chile')
