import requests, json
from bigchaindb_driver.crypto import generate_keypair
url = 'http://127.0.0.1:5000/asset/order'

keys = {}
#keys['HTgAKNrmrag3Njzihedca2hNVh2xkUmBGtzpybSn7Qcz'] = 'HtUTNKZCm8KeNGhBsBFxpV7ETm2NLEumvkoG46sF8xe1'  # Alice
#keys['7MwEfEiUuHRi4kmGmZEMbnungfEXAgmW6tMWytocEvmY'] = 'kn9CBTgjzLBsbvGXqCTYJc1DjNd1P6YCUQRkFptqWmv'  # Bob
#keys['GTPRhKNfTyGiExbN2mzAH7nzYsRmFwd83sGYpUrJ3avQ'] = 'CJDMTBB7AbVQib25dBc7b8dDq1gbrod7wEo61bXeVfAS'  # Peter
#keys['5Wh4yb9PryArz42PbmDqaEp2hZUjyqrgqNX4mXoUtNTi'] = '2tPUfY7CKD6MWRn7hwjL6JuYV343KcSPdS7vY6x57pC3'  # Gary

for i in range(0,12):
    s = generate_keypair()
    keys[s.public_key] = s.private_key

payloads = []
payloads.append({
    "playerID": "HTgAKNrmrag3Njzihedca2hNVh2xkUmBGtzpybSn7Qcz",
    "orderAction": "BUY",
    "orderSymbol": "AAPL",
    "orderQuantity": "1"
})

payloads.append({
    "playerID": "7MwEfEiUuHRi4kmGmZEMbnungfEXAgmW6tMWytocEvmY",
    "orderAction": "BUY",
    "orderSymbol": "GOOG",
    "orderQuantity": "2"
})

payloads.append({
    "playerID": "GTPRhKNfTyGiExbN2mzAH7nzYsRmFwd83sGYpUrJ3avQ",
    "orderAction": "BUY",
    "orderSymbol": "FB",
    "orderQuantity": "3"
})

payloads.append({
    "playerID": "5Wh4yb9PryArz42PbmDqaEp2hZUjyqrgqNX4mXoUtNTi",
    "orderAction": "BUY",
    "orderSymbol": "AMZN",
    "orderQuantity": "2"
})

asset_ids = {}

count = 0
for key in keys.items():
    payloads[0]['playerID'] = key[0]
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url, headers=headers, data=json.dumps(payloads[0]))
    count += 1
    print("BUY - " + str(count) + ": " + str(r.status_code))
    if r.status_code == requests.codes.ok:
        asset_ids[key[0]] = r.json()['txID']

count = 0
sell_pay_load = {}
for key in keys.items():
    sell_pay_load['playerID'] = key[0]
    sell_pay_load['orderAction'] = "SELL"
    sell_pay_load['txID'] = asset_ids[key[0]]
    sell_pay_load['privateKey'] = key[1]
    headers = {'Content-Type': 'application/json'}
    r = requests.post(url, headers=headers, data=json.dumps(sell_pay_load))
    count += 1
    print("SELL - " + str(count) + ": " + str(r.status_code))