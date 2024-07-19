# HPE Configuration Collector (HCC)

HCC allows collecting hardware configuration information directly from iLO using basic requests, similar to user queries to management in a browser.

## How it works
HCC interacts directly with iLO, enabling the collection of all information a user can see there. First, the script sends a POST request for login and receives a session token, which is used for further interactions. Then, the script uses GET requests to access each endpoint (one per position of collected information) and retrieves JSON objects containing the necessary configuration information. These JSON objects are compiled into a single JSON file, which is saved in the /output folder with the server's serial number as the filename. After this, the script closes the connection and moves on to the next server in the list.

## Collected Information:
- System Summary
- CPU
- RAM
- Storage
- NIC
- PCI
- PSU

## Supported Hardware

- HPE servers running iLO4
- HPE servers running iLO5
- Blade enclosures c7000 (in development)

## Installation

The script requires Python3 and several additional libraries:
- progress==1.6
- Requests==2.31.0
- urllib3==2.0.2

You can install the libraries individually using the command:
```sh
pip install ИмяБиблиотеки
```
Or all libraries at once using requirements.txt (located at the root of the repository):
```sh
pip install -r /path/to/requirements.txt
```

## Input
The script can accept a .csv file with the following format as input:
```sh
ip;login;password
172.24.1.1;testlogin;testpass
172.24.1.2;logintest;passtest
.....
```
The default delimiter is ;. You can use any other delimiter, but you will need to specify it when running the script.

## Usage
The script accepts the following arguments:
| Parameter | Description | 
| ------ | ------ |
| -f | Path to the input.csv file |
| -d | Custom delimiter for input.csv. Default is ; |
| -r | IP address range for collection with standard logins and passwords without input.csv |
| -l | Standard login |
| -p | Standard password |
| -dm | Debug mode |
**Parameters -f and -d cannot be used together with parameters -r, -l, -p**

## Examples
Run with a file containing iLO IP addresses, logins, and passwords:
```sh
python start.py -f C:\Users\micke\Desktop\UltimateHPEParser\input.csv
```
Run with a file containing iLO IP addresses, logins, and passwords + custom delimiter:
```sh
python start.py -f C:\Users\micke\Desktop\UltimateHPEParser\input.csv -d .
```
Run with an IP range in the last octet and identical logins-passwords:
```sh
python start.py -r 172.24.0.1-50 -l testlogin -p testpass 
```
Run with an IP range in CIDR notation and identical logins-passwords:
```sh
python start.py -r 172.24.0.0/28 -l testlogin -p testpass 
```

## Output
After the script runs, it will generate an /output folder containing configuration information in .json format. A logs.log file will also appear. You need to copy this file to the /output folder and archive it using any available archiver.
To convert output json file to excel format use:
```sh
python convert.py -i <PathToInput> -o <PathToOutput>
```

- PathToInput - path to the folder with collected json files. Mandatory parameter
- PathToOutput - path to the folder where the resulting table will be saved. Optional parameter, by default it will be saved in /output

