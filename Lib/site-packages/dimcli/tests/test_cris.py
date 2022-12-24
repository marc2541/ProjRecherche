#!/usr/bin/python
# -*- coding: utf-8 -*-


"""
simple client for CRIS  API

> python test_cris.py search publications return publications[id+category_sdg]

PRIVATE FILE

last checked 
2021-03-15

"""

import click 
import requests
import json


USE_PROD_CRIS = False



@click.command()
@click.argument('query', nargs=-1)
def main(query=None):
    """
    Simple test script for new API based on Readcube

    # CRIS API ON  READCUBE AUTH

    [instance.readcube] # new readcube auth
    url=https://cris-api.dimensions.ai/v2
    key=rA8BvwViA0YJH9U9dBSoLmcLyDN9iyaF

    [instance.sandbox-readcube] # staging new readcube auth
    url=https://sandbox-cris-api.dimensions.ai/v2
    key=RIczYn3cEfcRB6U6MIZx7BvcfiRYhNYp

    # From the docs 

    From command line:

    export endpoint="https://sandbox-api.dimensions.ai/"
    export DSL_TOKEN="$(curl -X GET "https://$endpoint/token?api_key=8cGaPHPQfxjmMR5NcnWCwzwjHIleGrTz")"
    curl -X POST https://$endpoint/api/query -H "authorization: Bearer $DSL_TOKEN" -d 'search publications return publications'

    ====
    @TODO embed in main dimcli auth, needing two updates 

    * login method in auth.py
    * query method in api.py
    ====

    """
    if not query: 
        click.secho(f"You did not pass a DSL query - using defaults..", dim=True)
        q = "search publications return publications[id+year] limit 5"
    else:
        q = " ".join([x for x in query])

    if USE_PROD_CRIS: #LIVE 
        api_key = "rA8BvwViA0YJH9U9dBSoLmcLyDN9iyaF"
        endpoint = "cris-api.dimensions.ai/v2"
    else: #STG
        api_key = "RIczYn3cEfcRB6U6MIZx7BvcfiRYhNYp" # v2
        api_key = "0ymUN7N3XT2gGJmkzarcmUn9lSiFWG4j" # v3
        endpoint = "sandbox-cris-api.dimensions.ai/v3"

    click.secho(f"Endpoint: {endpoint}", dim=True)

    # get token from key    

    url_token = f"https://{endpoint}/token?api_key={api_key}"
    response = requests.get(url_token)
    response.raise_for_status()
    token = response.text.strip("\n") # NOTE token has newline char at the end
    click.secho(f"Token obtained: {token}", fg="green")
    
    # query using token
    
    headers = {'Authorization': "Bearer " + token}
    url_query = f"https://{endpoint}/api/query"
    response = requests.post(url_query, data=q, headers=headers)
    
    try:
        res_json = response.json()
        print(json.dumps(res_json,  indent=4, sort_keys=True))
    except:
        print('Unexpected error. JSON could not be parsed.')
        print("Raw Response:",  response)

    while True:
        import time
        time.sleep(2)
        main()

if __name__ == '__main__':
    main()


