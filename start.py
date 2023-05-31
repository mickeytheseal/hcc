import ilo4
import collector_tools

##TODO Добавить исключения (нет подключение к серваку и т.д.)

iLO_creds = collector_tools.getIPfromFile(r"C:\Users\MUntura\Desktop\UltimateHPEParser\input.csv")
print (iLO_creds)

for srv in iLO_creds:
	ip = srv[0]
	login = srv[1]
	password = srv[2]

	print(f"Collecting info from {ip} " + collector_tools.getIloVer(ip))
	data = ilo4.collect(ip,login,password)
	collector_tools.saveToJSON(data)