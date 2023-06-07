import json

class Processor():
  def __init__(self,jsonobj):
    self.name = jsonobj["proc_name"]
  
  def __eq__(self, other):
    return self.name == other.name

  def __repr__(self):
    return self.name

class Memory():
  def __init__(self,jsonobj):
    self.size = jsonobj["mem_mod_size"]
    self.type = jsonobj["mem_mod_type"]
    self.tech = jsonobj["mem_mod_tech"]
    self.frequency = jsonobj["mem_mod_frequency"]
    self.ranks = jsonobj["mem_mod_ranks"]
    self.part_num = jsonobj["mem_mod_part_num"]
  
  def __eq__(self, other):
    return self.name == other.name

  def __repr__(self):
    return str(self.size) + " " + self.type + " " + self.tech + " " + str(self.frequency) + " " + str(self.ranks) + "rank " + self.part_num

class Drive():
  def __init__(self,jsonobj):
    self.name = jsonobj["model"]
  
  def __eq__(self, other):
    return self.name == other.name

  def __repr__(self):
    return self.name

class Controller():
  def __init__(self,jsonobj):
    self.sn = jsonobj["serial_no"]
    self.name = jsonobj["model"]
    if jsonobj["has_accel"] == 1:
      self.cache = jsonobj["accel_tot_mem"]
    else:
      self.cache = None
    self.drvs = [Drive(jsondrv) for jsondrv in jsonobj["physical_drives"]]
  
  def __eq__(self, other):
    return self.name == other.name

  def __repr__(self):
    return self.name + " " + str(self.cache) + "KB cache"

class NIC():
  def __init__(self,jsonobj):
    self.name = jsonobj["name"]
  
  def __eq__(self, other):
    return self.name == other.name

  def __repr__(self):
    return self.name

class PCI():
  def __init__(self,jsonobj):
    self.name = jsonobj["name"]
    self.pn = jsonobj["part_num"]
    self.spn = jsonobj["board_num"]
  
  def __eq__(self, other):
    return self.name == other.name 

  def __repr__(self):
    return self.name + " " + self.spn

class PSU():
  def __init__(self,jsonobj):
    self.name = jsonobj["ps_model"]
    self.spn = jsonobj["ps_spare"]
  
  def __eq__(self, other):
    return self.name == other.name   

  def __repr__(self):
    return self.name + " " + self.spn


class Server:
  def __init__(self,pathToFile):
    jsondata = None
    with open(pathToFile) as f:
      jsondata = json.load(f)

    self.name = jsondata["summary"]["product_name"]
    self.pid = jsondata["summary"]["product_id"]
    self.sn = jsondata["summary"]["serial_num"]
    self.cpus = [Processor(jsoncpu) for jsoncpu in jsondata["cpu"]["processors"]]
    self.mems = [Memory(jsonram) for jsonram in jsondata["ram"]["mem_modules"] if jsonram["mem_mod_status"] != "MEM_NOT_PRESENT"]
    self.ctrls = [Controller(jsonctrl) for jsonctrl in jsondata["storage"]["phy_drive_arrays"]]
    self.nics = [NIC(jsonnic) for jsonnic in jsondata["nic"]["comm_controllers"] if not "iLO" in jsonnic["name"]]
    self.pcis = [PCI(jsonpci) for jsonpci in jsondata["pci"]["inventory"] if jsonpci["status"] != "OP_STATUS_ABSENT"]
    self.psus = [PSU(jsonpsu) for jsonpsu in jsondata["psu"]["supplies"] if jsonpsu["ps_error_code"] != "PS_STATUS_UNKNOWN"]

  def __eq__(self, other):
    return self.sn == other.sn