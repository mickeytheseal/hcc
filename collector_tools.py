import os
import json
import csv
import requests
import logging
import sys
import ipaddress
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
    response = requests.request("GET", url, headers=headers, data=payload, verify = False, timeout=3)
    data = response.json()
    ver = data["moniker"]["PRODGEN"]
    return ver

def getIPfromFile(path,custom_delimeter):
    with open(path, newline='') as f:
        reader = csv.reader(f,delimiter=custom_delimeter)
        headers = next(f)
        data = list(reader)
    return(data)

def getCustomLogger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.CRITICAL)
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)
    file_handler = logging.FileHandler('logs.log','w+')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

def generateList(ip_range):
    ip_list = None
    if '/' in ip_range:
        ip_list = [str(ip) for ip in ipaddress.IPv4Network(ip_range)]
    elif '-' in ip_range:
        octets = ip_range.split('.')
        oct4_range = octets[3].split('-')
        ip_list = [f"{octets[0]}.{octets[1]}.{octets[2]}.{oct4}" for oct4 in range(int(oct4_range[0]),int(oct4_range[1])+1)]
    return ip_list

def progressbar(it, prefix="", size=60, out=sys.stdout):
    count = len(it)
    def show(j):
        x = int(size*j/count)
        print("{}[{}{}] {}/{}".format(prefix, "#"*x, "."*(size-x), j, count), 
                end='\r', file=out, flush=True)
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    print("\n", flush=True, file=out)