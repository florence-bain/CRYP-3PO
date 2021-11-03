import sys
sys.path.append('/Users/jessicabulman/.pyenv/versions/3.9.7/lib/python3.9/site-packages')
sys.path.append('/Users/jessicabulman/.pyenv/shims/python')
print(sys.path)

import requests


def get_contracts():
    contracts = []

    response_object = requests.get("https://www.bitmex.com/api/v1/instrument/active")

    for contract in response_object.json():
        contracts.append(contract["symbol"])

    return contracts
