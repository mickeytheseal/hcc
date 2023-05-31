import os
import json
import csv
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def saveToJSON(data):
    if not os.path.exists('output'):
        os.makedirs('output')
    sn = data["summary"]["serial_num"]
    sn = sn.replace(" ", "")
    with open(f'./output/{sn}.json', 'w') as outfile:
        json.dump(data, outfile)

def getIloVer(ip):
    url = f"https://{ip}/json/login_session"
    payload = {}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload, verify = False)
    data = response.json()
    ver = data["moniker"]["PRODGEN"]
    return ver

def getIPfromFile(path):
    with open(path, newline='') as f:
        reader = csv.reader(f,delimiter=';')
        headers = next(f)
        data = list(reader)
    return(data)