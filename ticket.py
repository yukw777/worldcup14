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

products = parser.find_product_by_teams('Korea Republic', 'Belgium')
for prod in products:
    tickets = parser.find_ticket_by_product_id(prod['ProductId'], 'CAT1')
    for tic in tickets:
        if int(tic.get('Quantity')) > 0:
            msg = json.dumps({'product': prod}, indent=4)
            msg += '\n\n'
            msg += json.dumps({'ticket': tic}, indent=4)
            for email in conf['email_list']:
                Email.send_email(email, 'Ticket Available!', msg)
            logging.info('Tickets found! Email sent')
        else:
            logging.info('No tickets :( Email not sent')
