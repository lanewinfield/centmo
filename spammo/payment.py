'''
Payment
'''

import logging
import sys
import requests
from random import randint

# Python 2.x fixes
try: from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode

import spammo

logger = logging.getLogger('spammo.payment')


def pay(user, amount, note):
    _pay_or_charge(user, amount, note)


def charge(user, amount, note):
    amount = -amount
    _pay_or_charge(user, amount, note)


def _pay_or_charge(user, amount, note):
    access_token = spammo.auth.get_access_token()
    if not access_token:
        logger.warn('No access token. Configuring ...')
        if not spammo.auth.configure():
            return
        access_token = spammo.auth.get_access_token()

    params = {
        'note': note,
        'amount': 0.01,
        'access_token': access_token,
        'audience': 'private',
    }
    if user.startswith('@'):
        username = user[1:]
        user_id = spammo.user.id_from_username(username.lower())
        if not user_id:
            logger.error('Could not find user @{}'.format(username))
            return
        params['user_id'] = user_id.lower()
    else:
        params['phone'] = user

    pennies = int(amount * 100)
    payments = []

    if pennies > 60:
    	# print "over 60 cents"
    	for x in range(0,60):
    		if x < 60:
    			realAmount = int(pennies / 60) / 100.00
    		else:
    			leftoverpennies = (pennies - int((realAmount * 100) * 60))
    			realAmount = (int(pennies / 60) + leftoverpennies) / 100.00
    		# print realAmount
    		payments.append(realAmount)
    else:
    	# print "under 60 cents"
    	for x in range(pennies):
    		payments.append(0.01)
    		# print "appending a cent"
    i = 0
    for x in payments:
	    params["note"] = note + " " + str(randint(0,10000))
	    # print "paying out " + str(payments[i])
	    params["amount"] = payments[i]
	    i = i+1
	    response = spammo.singletons.session().post(
	        _payments_url_with_params(params)
	    )
	    data = response.json()

	    try:
	        response.raise_for_status()
	    except requests.exceptions.HTTPError as e:
	        error_message = 'received {} from Venmo'.format(e.response.status_code)
	        if 'error' in data:
	            message = data['error']['message']
	            error_message += ': "{}"'.format(message)
	        print(error_message)
	        sys.exit(1)

	    payment = data['data']['payment']
	    target = payment['target']
	    payment_action = payment['action']
	    if payment_action == 'charge':
	        payment_action = 'charged'
	    if payment_action == 'pay':
	        payment_action = 'paid'
	    amount = payment['amount']
	    if target['type'] == 'user':
	        user = '{first_name} {last_name}'.format(
	            first_name=target['user']['first_name'],
	            last_name=target['user']['last_name'],
	        )
	    else:
	        user = target[target['type']],
	    # note = payment['note']
	    print(str(i) + '. Successfully {payment_action} {user} ${amount:.2f} for "{note}"'
	           .format(**locals()))

    print("You just sent a total of $"+amount+" in "+len(payments)+" payments of $"+payments[0]". I hope you're happy.")


def _payments_url_with_params(params):
    return '{payments_base_url}?{params}'.format(
        payments_base_url=spammo.settings.PAYMENTS_URL,
        params=urlencode(params),
    )
