import ilo4_5
import collector_tools
import requests
import exception
import logging
import json
import sys
import argparse

## Configure logging
logger = collector_tools.getCustomLogger()

## Configure args
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--file", help="File with iLO credentials")
parser.add_argument("-d", "--delimeter", help="Delimeter for input file. Default - ;", default=';',type=str)
parser.add_argument("-r", "--range", help="iLO IP range")
parser.add_argument("-l", "--login", help="Default login for range")
parser.add_argument("-p", "--password", help="Default password for range")
parser.add_argument("-dm", "--debug", help="Debug mode",action='store_true')

args = parser.parse_args()
input_method = 0 ## 0 - from file, 1 - from range
iLOs = None

if args.file is not None:
	iLOs = collector_tools.getIPfromFile(args.file,args.delimeter)	## Get iLO credentials from file
	logging.info("Getting data using file")
elif args.range is not None and args.login is not None and args.password is not None:
	iLOs = collector_tools.generateList(args.range)	## Generate IP list
	print(iLOs)
	input_method = 1
	logging.info("Getting data using range")

if args.debug:
	sys.exit()

## Get data from iLO
for srv in iLOs:
	ip = None
	login = None
	password = None

	if input_method == 0:
		ip = srv[0]
		login = srv[1]
		password = srv[2]
	else:
		ip = srv
		login = args.login
		password = args.password

	try:
		data = ilo4_5.collect(ip,login,password)
		logging.info(f"Collected data from {ip} {collector_tools.getIloVer(ip)}")
	except requests.exceptions.ConnectTimeout:
		logging.error(f"Connection timeout for {ip}")
		continue
	except requests.exceptions.ConnectionError:
		logging.error(f"Connection refused by {ip}")
		continue
	except json.decoder.JSONDecodeError:
		logging.error(f"JSONDecodeError at {ip}")
		continue		
	except exception.WrongCredentials:
		logging.error(f"Wrong credentials for {ip}")
		continue
	collector_tools.saveToJSON(data)