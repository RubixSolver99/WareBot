import time, math
from L1_log import tmpFile
from L1_lidar import Lidar as get
from L2_vector import getNearest

lidar = get(); lidar.connect(); lidar.run(); time.sleep(1)
def getLidarData(): return lidar.get()

while True:
    ds = getLidarData()
    if ds is None or getattr(ds, "size", 0) == 0: time.sleep(0.1)
    d, a = getNearest(ds)
    x = d * math.cos(math.radians(a)) 
    y = d * math.sin(math.radians(a)) 
    tmpFile(d, "distance"); tmpFile(a, "angle")
    tmpFile(x, "x");       tmpFile(y, "y")
    time.sleep(0.2)
    