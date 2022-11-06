#!/bin/python3
#Written by Julian Lopez and GitHub Copilot

import subprocess, os

version_number = "1.0.0"

docker_active_txt = "/home/user/.docker_running.txt"

def check_args():
	import sys
	if len(sys.argv) == 1: main()
	elif len(sys.argv) == 2:
		if ((sys.argv[1] == "-a" or sys.argv[1] == "--all" )): main()
		elif ((sys.argv[1] == "--version" )): show_version()
        elif ((sys.argv[1] == "-h" or sys.argv[1] == "--help" )): show_help()
		elif ((sys.argv[1] == "-d" or sys.argv[1] == "--docker" )): print ( get_docker_info() )
		elif ((sys.argv[1] == "-u" or sys.argv[1] == "--uptime" )): print ( get_server_uptime().replace('\n', ' ') )
		elif ((sys.argv[1] == "-p" or sys.argv[1] == "--packages" )): print ( get_num_of_upgradable_packages() )
		elif ((sys.argv[1] == "-v" or sys.argv[1] == "--virtual-machines" )): print ( get_virsh_info() )
		else: print ( "Invalid argument. Please use -h or --help for help." )
	else: print ( "Invalid arguments" )

def line_count(filename):
    with open(filename, 'r') as fp:
        return len(fp.readlines())

def read_lines_without_newline(filename):
	with open(filename, 'r') as fp:
        return fp.read().replace('\n', ' ')

def get_docker_info():
	if os.path.exists(docker_active_txt):
		docker_active_lines = line_count(docker_active_txt)
		if docker_active_lines == 0: return ( "There are no running docker containers.")
		elif docker_active_lines == 1: return ( "Currently there is one running docker container: " + read_lines_without_newline(docker_active_txt)[:-1] + ")" )
		else: return ( "Currently there are " + str(docker_active_lines) + " running docker containers: (" + read_lines_without_newline(docker_active_txt)[:-1] + ")" )
	else: return ( "Unable to locate docker_running.txt file. Please check if your sudo crontab is properly configured." )

def get_virsh_info():
	active_vms = subprocess.run("virsh -c qemu:///system list --name", shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
	num_active_vms = len(active_vms.split())
	if num_active_vms == 0: return ( "There are no running virtual machines.")
	elif num_active_vms == 1: return ( "Currently there is one running virtual machine: (" + active_vms.replace('\n', ' ')[:-2] + ")" )
	else: return ( "Currently there are " + str(num_active_vms) + " running virtual machines: (" + active_vms.replace('\n', ' ')[:-2] + ")" )

def get_server_uptime():
	return "Your server has been " + subprocess.run("uptime -p", shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')

def get_num_of_upgradable_packages():
	num_of_upgradable_packages = subprocess.run("apt-get --just-print upgrade", shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8').splitlines()[-1].split()[-3]
	if num_of_upgradable_packages == "0": return "There are no upgradable packages."
	elif num_of_upgradable_packages == "1": return "There is currently one upgradable package."
	else: return "There are currently " + num_of_upgradable_packages + " upgradable packages."

def show_help():
	print ( "Usage: server_status.py [OPTION]" )
	print ( "Show the status of your server." )
	print ( " " )
	print ( "  -a, --all              Check all status" )
	print ( "  -d, --docker           Check docker status" )
	print ( "  -v, --virtual-machines Check virtual machine status" )
	print ( "  -p, --packages         Check number of upgradable packages" )
	print ( "  -u, --uptime           Check server uptime" )
	print ( "  -h, --help             Show this help message and exit" )
	print ( "  --version              Show program's version number and exit" )
	
def show_version():
	print ( "server_status.py version " + version_number )

def main():
	print ( get_server_uptime() + get_num_of_upgradable_packages() + "\n" + get_docker_info() + "\n" + get_virsh_info())

if __name__=="__main__":
	check_args()