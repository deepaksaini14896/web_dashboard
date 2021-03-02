#!/bin/sh
git pull origin master
pip3 install -r requirements.txt
python3 ./dashboard/manage.py migrate
sudo su    
visudo -f /etc/sudoers
jenkins ALL= NOPASSWD: ALL
sudo -S supervisorctl restart web_dashboard
