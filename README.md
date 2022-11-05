# check_server_status

## Description

A script made to check the status of a Linux server that is meant to be run locally on it. I use it with Shortcuts on my iPhone over SSH to check the status of my home server with Siri.

Suggestions and bug reports are appreciated!

## Prerequisites

### To Check Docker Status

Add this line to your sudo crontab file (be sure to change the user in the path):

    */1 * * * * docker ps -a --format "{{.Names}}" --filter status=running > /home/user/.docker_running.txt

You can change the path to wherever you want, but make sure you change the txt file path in the script (variable *docker_active_txt*) to match the path used in the crontab file.

If you are not running Docker as root, you will need to use the __non-root__ user's crontab file.

## Usage

All you need to is to run the script without any arguments:

    $ ./server_status.py

Otherwise, you can run it using python:

    $ python server_status.py


## Options

    -a, --all             Check all status
    -v, --version         Show program's version number and exit
    -h, --help            Show this help message and exit

## Output Examples

### Without any arguments / with "--all" argument
Command

    $ ./server_status.py
    or
    $ ./server_status.py --all

Output

    Your server has been up 6 hours, 47 minutes
    There are currently 3 upgradable packages.
    Currently there are 2 running docker containers: (rutorrent jellyfin)
    There are no running virtual machines.


## Credits

Written by me [Julian Lopez](https://github.com/JLO64) using GitHub Copilot. I guess credit goes to everyone who posted their code onto GitHub as well?