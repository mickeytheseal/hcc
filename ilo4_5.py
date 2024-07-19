import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import exception


def collect(ip,login,password):

  srv_data = {}

  s = requests.Session() 

  ## login
  url = f"https://{ip}/json/login_session"
  payload = "{\"method\":\"login\",\"user_login\":\""+login+"\",\"password\":\""+password+"\"}"
  headers = {
    'Content-Type': 'text/plain'
  }
  response = s.request("POST", url, headers=headers, data=payload, verify=False, timeout=3)
  if response.status_code == 403:
    raise  exception.WrongCredentials

  ## summary
  url = f"https://{ip}/json/overview?"
  payload = {}
  headers = {}
  response = s.request("GET", url, headers=headers, data=payload, verify=False)
  srv_data["summary"] = response.json()

  fru_list = {f"https://{ip}/json/overview?": "summary",
                f"https://{ip}/json/proc_info": "cpu",
                f"https://{ip}/json/mem_info": "ram",
                f"https://{ip}/json/health_phy_drives": "storage",
                f"https://{ip}/json/comm_controller_info": "nic",
                f"https://{ip}/json/pci_info": "pci",
                f"https://{ip}/json/power_supplies": "psu"}
  for unit in list(fru_list.items()):
    url = unit[0]
    payload = {}
    headers = {}
    response = s.request("GET", url, headers=headers, data=payload, verify=False)
    srv_data[unit[1]] = response.json()

  ## logout
  url = f"https://{ip}/json/login_session"
  cookies = s.cookies.get_dict()
  session_key = cookies.get("sessionKey")
  payload = "{\"method\":\"logout\",\"session_key\":\"%s\"}" % (session_key)
  headers = {
    'Content-Type': 'text/plain',
    'Cookie': 'sessionKey=%s' % (session_key)
  }
  response = requests.request("POST", url, headers=headers, data=payload, verify=False)

  return srv_data

