#!/bin/bash
echo 'install python apache2 package'

sudo apt -y install python3-venv python3-pip python3
sudo apt -y install apache2 libapache2-mod-wsgi-py3
echo 'create net_admin user'
sudo useradd net_admin -d /opt/NetMonitorSystem -M -r -s "$(which bash)"
sudo chown -R net_admin:net_admin /opt/NetMonitorSystem
sudo chomd 771 /opt/NetMonitorSystem
echo 'su netadmin'
sudo su net_admin -c "pip3 install -r /opt/NetMonitorSystem/requirments"

## Setup wsgi
echo "import sys" >> /opt/NetMonitorSystem/server.wsgi
echo "from app import app as application" >>  /opt/NetMonitorSystem/server.wsgi
echo "sys.path.insert(0, '/opt/NetMonitorSystem')" >> /opt/NetMonitorSystem/server.wsgi
echo "activate_this = '/opt/NetMonitorSystem/venv/bin/activate'" >>  /opt/NetMonitorSystem/server.wsgi
echo "with open(activate_this) as file_:" >>  /opt/NetMonitorSystem/server.wsgi
echo "    exec(file_.read(), dict(__file__=activate_this))"  >>  /opt/NetMonitorSystem/server.wsgi

## Setup apache2 wsgi
echo "<virtualhost *:80>" >> /etc/apache2/sites-available/flask.conf
echo     "ServerName www.paul.local" >> /etc/apache2/sites-available/flask.conf
echo     "WSGIDaemonProcess flask user=net_admin group=net_admin threads=5" >> /etc/apache2/sites-available/flask.conf
echo     "WSGIScriptAlias / /opt/NetMonitorSystem/server.wsgi" >> /etc/apache2/sites-available/flask.conf
echo    " <directory /opt/NetMonitorSystem>" >> /etc/apache2/sites-available/flask.conf
echo       "WSGIProcessGroup flask" >> /etc/apache2/sites-available/flask.conf
echo        "Require all granted" >> /etc/apache2/sites-available/flask.conf
echo         "Order deny,allow" >> /etc/apache2/sites-available/flask.conf
echo        "Allow from all" >> /etc/apache2/sites-available/flask.conf
echo      "</directory>" >> /etc/apache2/sites-available/flask.conf
echo  "</virtualhost>" >> /etc/apache2/sites-available/flask.conf
sudo a2ensite flask
sudo systemctl restart apache2

## create admin user
python3 /opt/NetMonitorSystem/Useradd.py


