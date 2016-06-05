import os
import sys

sys.path.append("../")

##Virtualenv Settings
activate_this = '/specific/a/home/cc/students/cs/shiranmazor/HOC/DB_Project/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

##Replace the standard out
sys.stdout = sys.stderr

##Add this file path to sys.path in order to import settings
sys.path.insert(0, os.path.join(os.path.dirname(os.path.realpath(__file__)), '../..'))

##Add this file path to sys.path in order to import app
sys.path.append('/specific/a/home/cc/students/cs/shiranmazor/HOC/DB_Project')

##Create appilcation for our app
from Server.server import application as application