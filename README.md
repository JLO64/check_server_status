# check_server_status

## Description

A script made to check the status of a (Debian-Based) Linux server that is meant to be run locally on it. I use it with Shortcuts on my iPhone over SSH to check the status of my home server with Siri.

I mainly wrote this script to try out GitHub Copilot and try and make a script that's not 100% jank with has some documentation.

Suggestions and bug reports are appreciated!

## Prerequisites

### To Check Docker Status

Add this line to your sudo crontab file (be sure to change the user in the path):

    */1 * * * * docker ps -a --format "{{.Names}}" --filter status=running > /home/user/.docker_running.txt

You can change the path/filename to wherever you want, but make sure you use the --docker-path flag to match the path/filename used in the crontab file.

If you are not running Docker as root, you will need to use the __non-root__ user's crontab file.

## Usage

All you need to is to run the script with the arguments you want to check. For instance, to check the status of Docker and server uptime, run the following command:

    $ ./server_status.py -d -u

You can run it using python:

    $ python server_status.py -d -u

## Output Examples

### Without any arguments / "-h" or "--help"

	$ ./server_status.py
	Usage: server_status.py [OPTIONS...]

	Options:
		-a, --all              Check all status
		--api-server		      Start the api server
		-d, --docker           Check docker status
		--docker-path=PATH     Specify the path to the docker_running file
		-h, --help             Show this help message and exit
		-p, --packages         Check number of upgradable packages
		-u, --uptime           Check server uptime
		--version              Show program's version number and exit
		-v, --virtual-machines Show virtual machine status
	

### With "-a" or "--all" argument

	$ ./server_status.py --all
	Your server has been up 6 hours, 47 minutes
	There are currently 3 upgradable packages.
	Currently there are 2 running docker containers: (rutorrent jellyfin)
	There are no running virtual machines.

### With "-d" or "--docker" argument

	$ ./server_status.py --docker
	Currently there are 2 running docker containers: (rutorrent jellyfin)
You can specify the path to the .docker_running.txt file with the "--docker-path" argument.

	$ ./server_status.py --docker --docker-path=/home/user/.docker_running.txt
### With "-v" or "--virtual-machines" argument

	$ ./server_status.py --virtual-machines
	There are no running virtual machines.

### With "-p" or "--packages" argument

	$ ./server_status.py --packages
	There are currently 3 upgradable packages.

### With "-u" / "--uptime" argument

	$ ./server_status.py --uptime
	Your server has been up 6 hours, 47 minutes

## API Server Usage
To launch the API server, run the following command:

	$ ./server_status.py --api-server

The API will be available at http://localhost:3000/server-status

### API Server Output Examples
To request the status using the equivalent of the "-a" argument, use the following URL:

	http://localhost:3000/server-status?show_all=True

The request will be formated as a JSON with the key "response" containing a string.

	{
		"response": "Your server has been up 6 hours, 47 minutes\nThere are currently 3 upgradable packages.\nCurrently there are 2 running docker containers: (rutorrent jellyfin)\nThere are no running virtual machines."
	}


## Credits

Written by me [Julian Lopez](https://github.com/JLO64) using GitHub Copilot. I guess credit goes to everyone who posted their code onto GitHub as well?