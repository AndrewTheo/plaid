
from app.home import blueprint
from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from app import login_manager
from jinja2 import TemplateNotFound
from plaid import Client
from datetime import date, timedelta


@blueprint.route('/index')
def index():
    return render_template('login.html', segment='index')


@blueprint.route('/home')
def home():
    client = Client(client_id='CLIENT_ID', secret='SECRET', environment='sandbox')
    res = client.Sandbox.public_token.create(
            'ins_3',
            ['transactions']
          )
    # The generated public_token can now be
    # exchanged for an access_token
    publicToken = res['public_token']
    res = client.Item.public_token.exchange(publicToken)
    print(res)
    accessToken = res['access_token']
    allAccounts = []
    currentAvailableBalance = 0

    response = client.Accounts.balance.get(accessToken)
    print(response['accounts'])
    for i in range(len(response['accounts'])):
        availableBal = response['accounts'][i]['balances']['available']
        if availableBal != None:
            currentAvailableBalance = currentAvailableBalance + availableBal
        currentBal = response['accounts'][i]['balances']['current']
        name = response['accounts'][i]['name']
        subtype = response['accounts'][i]['subtype']
        allAccounts.append([availableBal, currentBal, name, subtype])
    print(allAccounts)
    print(currentAvailableBalance)

    today = date.today()
    dPast30 = today - timedelta(30)
    dPast30 = dPast30.strftime("%Y-%m-%d")
    today = today + timedelta(2)
    dToday = today.strftime("%Y-%m-%d")

    response = client.Transactions.get('access-sandbox-4c706f86-9f31-41af-9016-2b7a5b822477',
                                       start_date=str(dPast30),
                                       end_date=str(dToday))
    transactions = response['transactions']
    # Manipulate the count and offset parameters to paginate
    # transactions and retrieve all available data
    while len(transactions) < response['total_transactions']:
        response = client.Transactions.get('access-sandbox-4c706f86-9f31-41af-9016-2b7a5b822477',
                                           start_date=str(dPast30),
                                           end_date=str(dToday),
                                           offset=len(transactions)
                                          )
        transactions.extend(response['transactions'])

    return render_template('index.html', balance = currentAvailableBalance, transactions = transactions, allAccounts = allAccounts)

@blueprint.route('/<template>')
def route_template(template):

    try:

        if not template.endswith( '.html' ):
            template += '.html'

        # Detect the current page
        segment = get_segment( request )

        # Serve the file (if exists) from app/templates/FILE.html
        return render_template( template, segment=segment )

    except TemplateNotFound:
        return render_template('page-404.html'), 404
    
    except:
        return render_template('page-500.html'), 500

# Helper - Extract current page name from request 
def get_segment( request ): 

    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment    

    except:
        return None  
