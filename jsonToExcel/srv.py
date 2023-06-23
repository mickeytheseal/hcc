import json

class Processor():
  def __init__(self,jsonobj):
    self.name = jsonobj["proc_name"].strip()
  
  def __eq__(self, other):
    return isinstance(other, Processor) and self.name == other.name

  def __hash__(self):
        return hash(self.name)

  def __repr__(self):
    return self.name

class Memory():
  def __init__(self,jsonobj):
    self.size = jsonobj["mem_mod_size"]
    self.type = jsonobj["mem_mod_type"]
    self.tech = jsonobj["mem_mod_tech"]
    self.frequency = jsonobj["mem_mod_frequency"]
    self.ranks = jsonobj["mem_mod_ranks"]
    self.part_num = jsonobj["mem_mod_part_num"].strip()
  
  def __eq__(self, other):
    return isinstance(other, Memory) and self.size == other.size and self.type == other.type and self.tech == other.tech and self.frequency == other.frequency and self.ranks == other.ranks

  def __hash__(self):
    return hash((self.size,self.type,self.tech,self.frequency,self.ranks))

  def __repr__(self):
    if self.part_num == "NOT AVAILABLE":
      return str(self.size) + " " + self.type + " " + self.tech + " " + str(self.frequency) + " " + str(self.ranks) + "rank "
    else:
      return self.part_num

class Drive():
  def __init__(self,jsonobj):
    self.name = jsonobj["model"]
  
  def __eq__(self, other):
    return isinstance(other, Drive) and self.name == other.name

  def __hash__(self):
    return hash(self.name)

  def __repr__(self):
    return self.name

class Controller():
  def __init__(self,jsonobj):
    self.name = jsonobj["model"]
    if jsonobj["has_accel"] == 1:
      self.cache = jsonobj["accel_tot_mem"]
    else:
      self.cache = None
    self.drvs = [Drive(jsondrv) for jsondrv in jsonobj["physical_drives"]]
  
  def __eq__(self, other):
    return isinstance(other, Controller) and self.name == other.name

  def __hash__(self):
    return hash((self.name,self.cache,tuple(self.drvs)))

  def __repr__(self):
    return self.name + " " + str(self.cache) + " cache"

class NIC():
  def __init__(self,jsonobj):
    self.name = jsonobj["name"]
  
  def __eq__(self, other):
    return isinstance(other, NIC) and self.name == other.name

  def __hash__(self):
    return hash(self.name)

  def __repr__(self):
    return self.name

class PCI():
  def __init__(self,jsonobj):
    self.name = jsonobj["name"]
    self.pn = jsonobj["part_num"]
    self.spn = jsonobj["board_num"]
  
  def __eq__(self, other):
    return isinstance(other, PCI) and self.name == other.name 

  def __hash__(self):
    return hash(self.name)

  def __repr__(self):
    return self.name + " " + self.spn

class PSU():
  def __init__(self,jsonobj):
    self.name = jsonobj["ps_model"]
    self.spn = jsonobj["ps_spare"]
  
  def __eq__(self, other):
    return isinstance(other, PSU) and self.name == other.name   

  def __hash__(self):
        return hash(self.name)

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
    return isinstance(other, Server) and self.sn == other.sn

  def __hash__(self):
        return hash(self.sn)


def countAndRemove(data):
  result = {}
  for obj in data:
    if obj in result.keys():
      result[obj] += 1
    else:
      result[obj] = 1
  return(result)

class ReportRecord:
  def __init__(self,server):
    self.name = server.name
    self.pid = server.pid
    self.sn = server.sn
    self.cpu = countAndRemove(server.cpus)
    self.ram = countAndRemove(server.mems)
    self.ctrl = countAndRemove(server.ctrls)
    drv_list = sum([drv for drv in [ctrl.drvs for ctrl in server.ctrls]],[])
    self.drv = countAndRemove(drv_list)
    self.nic = countAndRemove(server.nics)
    self.pci = countAndRemove(server.pcis)
    self.psu = countAndRemove(server.psus)