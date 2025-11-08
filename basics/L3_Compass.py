import time
from L1_log import tmpFile, stringTmpFile
from L2_compass_heading import get_heading

def read_heading():     
    return float(get_heading())

def to_cardinal(h):       
    d=["North","North East","East","South East","South","South West","West","North West"]
    a=(h + 180 + 360)%360
    return d[int(((a+22.5)%360)/45)]

if __name__ == "__main__":
    while True:
        h=read_heading()
        tmpFile(h,"compass_heading")
        stringTmpFile(to_cardinal(h),"compass_direction")
        time.sleep(0.2)