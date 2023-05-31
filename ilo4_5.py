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


  ## cpu
  url = f"https://{ip}/json/proc_info"
  payload = {}
  headers = {}
  response = s.request("GET", url, headers=headers, data=payload, verify=False)
  srv_data["cpu"] = response.json()

  ## ram
  url = f"https://{ip}/json/mem_info"
  payload = {}
  headers = {}
  response = s.request("GET", url, headers=headers, data=payload, verify=False)
  srv_data["ram"] = response.json()

  ## storage
  url = f"https://{ip}/json/health_phy_drives"
  payload = {}
  headers = {}
  response = s.request("GET", url, headers=headers, data=payload, verify=False)
  srv_data["storage"] = response.json()

  ## nic
  url = f"https://{ip}/json/comm_controller_info"
  payload = {}
  headers = {}
  response = s.request("GET", url, headers=headers, data=payload, verify=False)
  srv_data["nic"] = response.json()

  ## pci
  url = f"https://{ip}/json/pci_info"
  payload = {}
  headers = {}
  response = s.request("GET", url, headers=headers, data=payload, verify=False)
  srv_data["pci"] = response.json()

  ## psu
  url = f"https://{ip}/json/power_supplies"
  payload = {}
  headers = {}
  response = s.request("GET", url, headers=headers, data=payload, verify=False)
  srv_data["psu"] = response.json()


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

