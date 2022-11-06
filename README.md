# check_server_status

## Description

A script made to check the status of a Linux server that is meant to be run locally on it. I use it with Shortcuts on my iPhone over SSH to check the status of my home server with Siri.

I mainly wrote this script to try out GitHub Copilot and try and make a script that's not 100% jank with has some documentation.

Suggestions and bug reports are appreciated!

## Prerequisites

### To Check Docker Status

Add this line to your sudo crontab file (be sure to change the user in the path):

    */1 * * * * docker ps -a --format "{{.Names}}" --filter status=running > /home/user/.docker_running.txt

You can change the path to wherever you want, but make sure you change the txt file path in the script (variable *docker_active_txt*) to match the path used in the crontab file.

If you have improperly set up your crontab command, the following message will be shown.
	
	Unable to locate docker_running.txt file. Please check if your sudo crontab is properly configured."

If you are not running Docker as root, you will need to use the __non-root__ user's crontab file.

## Usage

All you need to is to run the script without any arguments:

    $ ./server_status.py

Otherwise, you can run it using python:

    $ python server_status.py


## Options

	-a, --all              Check all status
	-d, --docker           Check docker status
	-v, --virtual-machines Check virtual machines status
	-p, --packages         Check number of upgradable packages
	-u, --uptime           Check server uptime
	-h, --help             Show this help message and exit
	--version              Show program's version number and exit

## Output Examples

### Without any arguments / with "-a" / "--all" argument
Command

    $ ./server_status.py
    or
    $ ./server_status.py --all

Output

    Your server has been up 6 hours, 47 minutes
    There are currently 3 upgradable packages.
    Currently there are 2 running docker containers: (rutorrent jellyfin)
    There are no running virtual machines.

### With "-d" / "--docker" argument
Command

	$ ./server_status.py -d
	or
	$ ./server_status.py --docker
Output

	Currently there are 2 running docker containers: (rutorrent jellyfin)

### With "-v" / "--virtual-machines" argument
Command

	$ ./server_status.py -v
	or
	$ ./server_status.py --virtual-machines
Output

	There are no running virtual machines.

### With "-p" / "--packages" argument
Command

	$ ./server_status.py -p
	or
	$ ./server_status.py --packages
Output
	
	There are currently 3 upgradable packages.
### With "-u" / "--uptime" argument
Command

	$ ./server_status.py -u
	or
	$ ./server_status.py --uptime
Output

	Your server has been up 6 hours, 47 minutes


## Credits

Written by me [Julian Lopez](https://github.com/JLO64) using GitHub Copilot. I guess credit goes to everyone who posted their code onto GitHub as well?