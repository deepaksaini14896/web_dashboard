#!/bin/sh

sudo systemctl stop supervisor
git pull origin master
pip3 install -r requirements.txt
python3 ./dashboard/manage.py migrate
sudo systemctl start supervisor