#!/bin/sh

pip3 install -r requirements.txt
python3 ./dashboard/manage.py migrate
sudo supervisorctl restart web_dashboard