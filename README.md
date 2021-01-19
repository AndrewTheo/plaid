<h1 align="center"> Money Management App, using the Plaid Api </h1>

<p align="center">
   <img src="https://raw.githubusercontent.com/AndrewTheo/plaid/main/media/showcase.gif?token=ADJSS55HHOTCZHMLE2GKGHLAB7NTM" />
</p>
<br />

## How it works (Plaid Api)

### Getting a sandbox public token 
```python
$ from plaid import Client
$ client = Client(client_id='YOUR_CLIENT_ID', secret='YOUR_SECRET', environment='sandbox')
$ res = client.Sandbox.public_token.create('ins_1', ['transactions'])
$ publicToken = res['public_token']
```

<br />
