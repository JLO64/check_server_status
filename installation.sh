#check if root
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

#check for file
if [ ! -f ./server_status.py ]; then
    echo "Unable to find server_status.py.\nIs this script being run from the cloned git directory?"
    exit 1
fi

pip install -r requirements.txt

cp ./server_status.py /usr/local/bin/server-status

touch /etc/systemd/system/server-status.service

cat > /etc/systemd/system/server-status.service << ENDOFFILE
[Unit]
Description=Starting the API server to check my server status.
After=network.target

[Service]
ExecStart=/usr/bin/python3 /usr/local/bin/server-status --api-server
Type=simple

[Install]
Alias=server-status.service:
ENDOFFILE

systemctl daemon-reload

systemctl enable server-status.service

sleep 3s

isEnabled="$(systemctl is-enabled server-status.service)"
if [ "$isEnabled" == "enabled" ]; then
    echo "Server status service enabled."
else
    echo "ERROR: Server status service not enabled."
    exit 1
fi