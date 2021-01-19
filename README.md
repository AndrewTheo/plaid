<h1 align="center"> Money Management App, using the Plaid Api </h1>

<p align="center">
   <img src="https://raw.githubusercontent.com/AndrewTheo/plaid/main/media/showcase.gif?token=ADJSS55HHOTCZHMLE2GKGHLAB7NTM" />
</p>
<br />

## How it works (Plaid Api)

### Getting a sandbox public token 
```python
from plaid import Client
client = Client(client_id='YOUR_CLIENT_ID', secret='YOUR_SECRET', environment='sandbox')
res = client.Sandbox.public_token.create('ins_1', ['transactions'])
publicToken = res['public_token']
```

#### Once we have a public token it can be exchanged for a access token, this will allow us to access the sandbox user's account information

<br />

### Exchanging the public token for an access token 
```python
res = client.Item.public_token.exchange(publicToken)
accessToken = res['access_token']
```
#### With a access token we can now get information such as the balances of each account
```python
res = client.Accounts.balance.get(accessToken)
```
### Or transaction information
```python
res = client.Transactions.get(accessToken, start_date='2019-09-23', end_date='2021-02-02')
transactions = res['transactions']
```
