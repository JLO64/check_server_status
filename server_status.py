#!/bin/python3
#Written by Julian Lopez and GitHub Copilot

version_number = "1.0.0"

from fastapi import FastAPI
from getpass import getpass
import subprocess, os, sys, getopt, uvicorn, json

docker_active_txt = os.path.expanduser("~") + "/.docker_running.txt"
ips_to_check_json = os.path.expanduser("~") + "/.ips_to_check.json"
version_number = "1.0.0"

class runClass:
	def __init__(self):
		self.run_print_help = False
		self.run_print_version = False
		self.run_print_all = False
		self.run_print_docker_info = False
		self.run_print_server_uptime = False
		self.run_print_num_of_upgradable_packages = False
		self.run_print_virsh_info = False
		self.run_check_ips = False

api_server = False

app = FastAPI()
@app.get("/server-status")
async def api_responce(uptime = False, docker = False, packages = False, virtual_machines = False, show_all = False, version = False, show_help = False, show_ips = False):
	apiargsBool = runClass()

	apiargsBool.run_print_server_uptime = uptime
	apiargsBool.run_print_docker_info = docker
	apiargsBool.run_print_num_of_upgradable_packages = packages
	apiargsBool.run_print_virsh_info = virtual_machines
	apiargsBool.run_print_all = show_all
	apiargsBool.run_print_version = version
	apiargsBool.run_print_help = show_help
	apiargsBool.run_check_ips = show_ips

	response = return_info_as_string(apiargsBool)
	return {"response":response}

def check_if_server(argv):
	try:
		opts, args = getopt.getopt(argv, "adpuvih", ["all", "docker", "packages", "uptime", "virtual-machines", "ip-check", "help", "version", "docker-path=", "api-server", "ip-json="])
	except getopt.GetoptError:
		print ( "Invalid arguments. Please use -h or --help for help." )
		sys.exit(2)
	if( len(opts) == 0 ):
		print(return_help())
		sys.exit()
	#check for variables
	for opt, arg in opts:
		if (opt == "--docker-path"):
			global docker_active_txt
			docker_active_txt = arg
		if (opt == "--ip-json"):
			global ips_to_check_json
			ips_to_check_json = arg
	#check if api server
	for opt, arg in opts:
		if (opt == "--api-server"):
			uvicorn.run(app, host="0.0.0.0", port=3000)
			sys.exit()
	check_local_args(opts)

def import_listofips_from_JSON(filetoimport):
	with open(filetoimport) as f:
		return json.load(f)

def check_local_args(opts):
	printargsBool = runClass()
	
	for opt in opts:
		if opt[0] in ("-h", "--help"): printargsBool.run_print_help = True
		elif (opt[0] == "--version"): printargsBool.run_print_version = True
		elif opt[0] in ("-a", "--all"): printargsBool.run_print_all = True
		elif opt[0] in ("-d", "--docker"):	printargsBool.run_print_docker_info = True
		elif opt[0] in ("-u", "--uptime"):	printargsBool.run_print_server_uptime = True
		elif opt[0] in ("-p", "--packages"): printargsBool.run_print_num_of_upgradable_packages = True
		elif opt[0] in ("-v", "--virtual-machines"):  printargsBool.run_print_virsh_info = True
		elif opt[0] in ("-i", "--ip-check"):  printargsBool.run_check_ips = True
	print(return_info_as_string(printargsBool))

def return_info_as_string(boolClasstoCheck):
	if (boolClasstoCheck.run_print_help):
		return return_help()
	if (boolClasstoCheck.run_print_version):
		return return_version()

	responce = ""
	if (boolClasstoCheck.run_print_all):
		responce += return_server_uptime() + "\n"
		responce += return_num_of_upgradable_packages() + "\n"
		responce += return_docker_info() + "\n"
		responce += return_virsh_info() + "\n"
	else:
		if (boolClasstoCheck.run_print_server_uptime): responce += return_server_uptime() + "\n"
		if (boolClasstoCheck.run_print_num_of_upgradable_packages): responce += return_num_of_upgradable_packages() + "\n"
		if (boolClasstoCheck.run_print_docker_info): responce += return_docker_info() + "\n"
		if (boolClasstoCheck.run_print_virsh_info): responce += return_virsh_info() + "\n"
	if (boolClasstoCheck.run_check_ips): responce += return_ips_to_check() + "\n"
	return responce[:-1]

def line_count(filename):
	with open(filename, 'r') as fp:
		return len(fp.readlines())

def read_lines_without_newline(filename):
	with open(filename, 'r') as fp:
		return fp.read().replace('\n', ' ')

def return_docker_info():
	if os.path.exists(docker_active_txt):
		docker_active_lines = line_count(docker_active_txt)
		if docker_active_lines == 0: return ( "There are no running docker containers.")
		elif docker_active_lines == 1: return ( "Currently there is one running docker container: " + read_lines_without_newline(docker_active_txt)[:-1] + ")" )
		else: return ( "Currently there are " + str(docker_active_lines) + " running docker containers: (" + read_lines_without_newline(docker_active_txt)[:-1] + ")" )
	else: return ( "Unable to locate docker_running.txt file. Please check if your sudo crontab is properly configured." )

# TODO add option for remote virsh
def return_virsh_info():
	active_vms = subprocess.run("virsh -c qemu:///system list --name", shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
	num_active_vms = len(active_vms.split())
	if num_active_vms == 0: return ( "There are no running virtual machines.")
	elif num_active_vms == 1: return ( "Currently there is one running virtual machine: (" + active_vms.replace('\n', ' ')[:-2] + ")" )
	else: return ( "Currently there are " + str(num_active_vms) + " running virtual machines: (" + active_vms.replace('\n', ' ')[:-2] + ")" )

def return_server_uptime():
	return ( "Your server has been " + subprocess.run("uptime -p", shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n', ' ')[:-1] + "." )

def return_line_with_matching_string(stringtolookfor, stringtolookin):
	for line in stringtolookin.splitlines():
		if stringtolookfor in line:
			return line

# XX upgraded
def return_num_of_upgradable_packages():
	num_of_upgradable_packages = return_line_with_matching_string("upgraded, ", subprocess.run("apt-get --just-print upgrade", shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')).split()[0]
	if num_of_upgradable_packages == "0": return ( "There are no packages to upgrade." )
	elif num_of_upgradable_packages == "1": return ( "There is currently one package to upgrade.")
	else: return ( "There are currently " + num_of_upgradable_packages + " packages to upgrade." )

def return_help():
	response = ""
	response += ( "Usage: server_status.py [OPTION]..." )
	response += ( "\nShow the status of your server." )
	response += ( "\n " )
	response += ( "\n  -a, --all              Show all status" )
	response += ( "\n  --api-server		      Start the api server" )
	response += ( "\n  -d, --docker           Show docker status" )
	response += ( "\n  --docker-path=PATH     Specify the path to the docker_running.txt file" )
	response += ( "\n  -h, --help             Show this help message and exit" )
	response += ( "\n  -i, --ip-check         Check IPs connected to network" )
	response += ( "\n  -p, --packages         Show number of upgradable packages" )
	response += ( "\n  -u, --uptime           Show server uptime" )
	response += ( "\n  --version              Show program's version number and exit" )
	response += ( "\n  -v, --virtual-machines Show virtual machine status" )
	return response

def return_ips_to_check():
	countallips = False
	listallips = False	

	if os.geteuid() != 0: return "This script must be run as root in order to check ips."
		
	response = ""
	scan_results = subprocess.run("arp-scan -l", shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
	try:
		jsondata = import_listofips_from_JSON(ips_to_check_json)
	except:
		return "Unable to open " + ips_to_check_json + ". Please check if the file exists and is properly formatted."
	
	if countallips:
		response += ("There are " + str(scan_results.count("192.168.1")) + " devices connected to the network.")
	if listallips:
		for line in scan_results.splitlines():
			if ("192.168.1" in line) and ("Interface" not in line): response += (line.split()[0])
			
	for ipobject in jsondata:
		if ipobject["IP"] in scan_results:
			if "TrueStatement" in ipobject: response += ( ipobject["TrueStatement"] )
			else: response += (ipobject["Name"] + " is on the network.")
		else:
			if "FalseStatement" in ipobject: response += (ipobject["FalseStatement"])
			#else: print(ipobject["Name"] + " is NOT on the network.")

	return response

def return_version():
	return ( "server_status.py version " + version_number )

if __name__=="__main__":
	check_if_server(sys.argv[1:])
