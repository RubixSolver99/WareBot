import time

from basics import L1_ina
from basics import L1_log as log

while True:
    log.tmpFile(L1_ina.readVolts(), "INA219 Voltage")
    time.sleep(1)