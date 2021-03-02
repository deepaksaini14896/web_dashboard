#!/bin/sh

ssh ubuntu@ip-172-31-40-181 <<EOF
  cd web_dashboard
  git pull
  pip3 install -r requirements.txt
  ./dashboard/manage.py migrate
  sudo supervisorctl restart web_dashboard
  exit
EOF
