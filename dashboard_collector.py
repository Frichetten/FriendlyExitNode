#!/usr/bin/env python

import logging
import logging.handlers
import stem
from stem.control import Controller
from stem.util.str_tools import get_size_label
from datetime import timedelta
from flask import Flask
from flask import render_template

app = Flask(__name__)

# Adding Syslog logging
handler = logging.handlers.SysLogHandler(address = '/dev/log')
logger = logging.getLogger('tor_dashboard')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

# Create controller
try:
    controller = Controller.from_port()
except stem.SockerError as exc:
    logger.debug('[Dashboard] Failed to create controller')
    exit()

# Trying to authenticate
try:
    pw = open('./controller_password','r').readline()[:-1]
    controller.authenticate(password=pw)
except stem.connection.MissingPassword:
    print("[-] You need a password to authenticate with Tor")
    logger.debug('[Dashboard] Failed to authenticate with control port')
    exit()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def homepage(path):
    return render_template('index.html')

def get_metrics():
    bandwidthrate = get_size_label(int(controller.get_conf('RelayBandwidthRate', '0')))
    eff_bandwidthrate = get_size_label(int(controller.get_effective_rate()))
    br = get_size_label(int(controller.get_info("traffic/read")))
    bw = get_size_label(int(controller.get_info("traffic/written")))
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        uptime = str(timedelta(seconds = uptime_seconds))

if __name__ == "__main__":
    app.run(port=5000)

