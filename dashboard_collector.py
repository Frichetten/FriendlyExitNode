import logging
import logging.handlers
import stem
from stem.control import Controller
from stem.util.str_tools import get_size_label
from datetime import timedelta

# Adding Syslog logging
handler = logging.handlers.SysLogHandler(address = '/dev/log')
logger = logging.getLogger('tor_dashboard')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

# Create controller
try:
    controller = Controller.from_port()
except stem.SockerError as exc:
    logger.debug('Failed to create controller')
    exit()

# Trying to authenticate
try:
    pw = open('/root/controller_password','r').readline()[:-1]
    controller.authenticate(password = pw)
except stem.connection.MissingPassword:
    logger.debug('Failed to authenticate with control port')
    exit()

# Gather data
bandwidthrate = get_size_label(int(controller.get_conf('RelayBandwidthRate', '0')))
eff_bandwidthrate = get_size_label(int(controller.get_effective_rate()))
br = get_size_label(int(controller.get_info("traffic/read")))
bw = get_size_label(int(controller.get_info("traffic/written")))
with open('/proc/uptime', 'r') as f:
    uptime_seconds = float(f.readline().split()[0])
    uptime = str(timedelta(seconds = uptime_seconds))

# Do stuff

