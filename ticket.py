import requests
import json
from parser import Parser
from email_sender import Email
from config import conf

res = requests.get('https://fwctickets.fifa.com/TopsAkaCalls/Calls.aspx/getBasicData?l=en&c=OTH')
res.raise_for_status()
data = res.json()
parser = Parser(data)

products = parser.find_product_by_teams('Korea Republic', 'Belgium')
for prod in products:
    tickets = parser.find_ticket_by_product_id(prod['ProductId'], 'CAT1')
    for tic in tickets:
        if int(tic.get('Quantity')) > 0:
            msg = json.dumps({'product': prod}, indent=4)
            msg += '\n\n'
            msg += json.dumps({'ticket': tic}, indent=4)
            Email.send_email(conf['email_user_name'], 'Ticket Available!', msg)
            print 'Tickets found! Email sent'
        else:
            print 'No tickets :( Email not sent'
