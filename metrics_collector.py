#!/usr/bin/env python

import logging
import logging.handlers
import stem
from stem.control import Controller
from stem.util.str_tools import get_size_label
from datetime import timedelta

class MetricObject:
    def __init__(self):
        self.relay_bandwidth_rate = get_size_label(int(controller.get_conf('RelayBandwidthRate', '0')))
        self.effective_bandwidth_rate = get_size_label(int(controller.get_effective_rate()))
        self.bandwidth_read = get_size_label(int(controller.get_info("traffic/read")))
        self.bandwidth_written = get_size_label(int(controller.get_info("traffic/written")))
        with open('/proc/uptime', 'r') as f:
            uptime_seconds = float(f.readline().split()[0])
            uptime_string = str(timedelta(seconds = uptime_seconds))
            self.uptime = uptime_string[:uptime_string.rfind(":")]

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

metrics = MetricObject()
with open('/tmp/metrics.txt', 'w') as w:
    w.write(metrics.relay_bandwidth_rate + "\n")
    w.write(metrics.effective_bandwidth_rate + "\n")
    w.write(metrics.bandwidth_read + "\n")
    w.write(metrics.bandwidth_written + "\n")
    w.write(metrics.uptime + "\n")