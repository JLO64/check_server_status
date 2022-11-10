#!/bin/python3
#Written by Julian Lopez and GitHub Copilot

import subprocess, os, sys, getopt

version_number = "1.0.0"

docker_active_txt = os.path.expanduser("~") + "/.docker_running.txt"

def check_args(argv):
	try:
		opts, args = getopt.getopt(argv, "adpuvh", ["all", "docker", "packages", "uptime", "virtual-machines", "help", "version", "docker-path="])
	except getopt.GetoptError:
		print ( "Invalid arguments. Please use -h or --help for help." )
		sys.exit(2)
	if( len(opts) == 0 ):
		print_help()
		sys.exit()
	#check for variables
	for opt, arg in opts:
		if (opt == "--docker-path"):
			global docker_active_txt
			docker_active_txt = arg
    #print functions
	for opt, arg in opts:
		if opt in ("-h", "--help"): print_help()
		elif (opt == "--version"): print_version()
		elif opt in ("-a", "--all"): print_all()
		elif opt in ("-d", "--docker"):	print_docker_info()
		elif opt in ("-u", "--uptime"):	print_server_uptime()
		elif opt in ("-p", "--packages"): print_num_of_upgradable_packages()
		elif opt in ("-v", "--virtual-machines"):  print_virsh_info()
		else: print ( "Invalid arguments. Please use -h or --help for help." )
	sys.exit()

def line_count(filename):
    with open(filename, 'r') as fp:
        return len(fp.readlines())

def read_lines_without_newline(filename):
	with open(filename, 'r') as fp:
		return fp.read().replace('\n', ' ')

def print_docker_info():
	if os.path.exists(docker_active_txt):
		docker_active_lines = line_count(docker_active_txt)
		if docker_active_lines == 0: print ( "There are no running docker containers.")
		elif docker_active_lines == 1: print ( "Currently there is one running docker container: " + read_lines_without_newline(docker_active_txt)[:-1] + ")" )
		else: print ( "Currently there are " + str(docker_active_lines) + " running docker containers: (" + read_lines_without_newline(docker_active_txt)[:-1] + ")" )
	else: print ( "Unable to locate docker_running.txt file. Please check if your sudo crontab is properly configured." )

def print_virsh_info():
	active_vms = subprocess.run("virsh -c qemu:///system list --name", shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
	num_active_vms = len(active_vms.split())
	if num_active_vms == 0: print ( "There are no running virtual machines.")
	elif num_active_vms == 1: print ( "Currently there is one running virtual machine: (" + active_vms.replace('\n', ' ')[:-2] + ")" )
	else: print ( "Currently there are " + str(num_active_vms) + " running virtual machines: (" + active_vms.replace('\n', ' ')[:-2] + ")" )

def print_server_uptime():
	print( "Your server has been " + subprocess.run("uptime -p", shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').replace('\n', ' ')[:-1] + "." )

def return_line_with_matching_string(stringtolookfor, stringtolookin):
	for line in stringtolookin.splitlines():
		if stringtolookfor in line:
			return line

def print_num_of_upgradable_packages():
	num_of_upgradable_packages = return_line_with_matching_string("upgraded, ", subprocess.run("apt-get --just-print upgrade", shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')).split()[0]
	if num_of_upgradable_packages == "0": print( "There are no packages to upgrade." )
	elif num_of_upgradable_packages == "1": print( "There is currently one package to upgrade.")
	else: print( "There are currently " + num_of_upgradable_packages + " packages to upgrade." )

def print_help():
	print ( "Usage: server_status.py [OPTION]..." )
	print ( " " )
	print ( "  -a, --all              Show all status" )
	print ( "  -d, --docker           Show docker status" )
	print ( "  --docker-path=PATH     Specify the path to the docker_running.txt file" )
	print ( "  -v, --virtual-machines Show virtual machine status" )
	print ( "  -p, --packages         Show number of upgradable packages" )
	print ( "  -u, --uptime           Show server uptime" )
	print ( "  -h, --help             Show this help message and exit" )
	print ( "  --version              Show program's version number and exit" )
	
def print_version():
	print ( "server_status.py version " + version_number )

def print_all():
	print_num_of_upgradable_packages()
	print_server_uptime()
	print_docker_info()
	print_virsh_info()

if __name__=="__main__":
	check_args(sys.argv[1:])
