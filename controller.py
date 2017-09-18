import os, sys
if 'SUMO_HOME' in os.environ:
     tools = os.path.join(os.environ['SUMO_HOME'], '')
     sys.path.append(tools)
else:   
     sys.exit("please declare environment variable 'SUMO_HOME'")

import traci
import random
import math
import numpy as np


sumoBinary = "/usr/bin/sumo-gui"
sumoCmd = [sumoBinary, "-c", "rl.sumo.cfg"]

traci.start(sumoCmd)

D1_0 = 750*[0]
D2_0 = 750*[0]
D3_0 = 750*[0]
D4_0 = 750*[0]
D5_0 = 750*[0]
D6_0 = 750*[0]
D7_0 = 750*[0]
D8_0 = 750*[0]
D1_1 = 750*[0]
D2_1 = 750*[0]
D3_1 = 750*[0]
D4_1 = 750*[0]
D5_1 = 750*[0]
D6_1 = 750*[0]
D7_1 = 750*[0]
D8_1 = 750*[0]

def changelights(num) :
  states = traci.trafficlights.getRedYellowGreenState("3")
  n = states[0:4]
  s = states[7:11]
  e = states[4:7]
  w = states[11:14]
  if num==1:
    n = "GGGG"
    s = "GGGG"
    e = "rrr"
    w = "rrr"
  if num==2:
    n = "rrrr"
    s = "rrrr"
    w = "GGG"
    e = "GGG"
  if num==3:
    n = "GgGg"
    s = "GgGg"
    e = "rrr"
    w="rrr"
  if num==4:
    e = "GgG"
    w = "GgG"
    n="rrrr"
    s="rrrr"
  if num==5:
    n = "yyyy"
    s = "yyyy"
    e = "GGG"
    w = "GGG"
  if num==6:
    e = "yyy"
    w = "yyy"
    n = "GGGG"
    s="GGGG"
  if num==7:
    n = "rrrr"
    s = "rrrr"
    e = "rrr"
    w = "rrr"
  final = n+e+s+w
  traci.trafficlights.setRedYellowGreenState("3", final)
  traci.trafficlights.setPhaseDuration("3", 4000)

wta = []
qla = []
step = 0
while step < 1000:
   traci.simulationStep()
   D1_0 = 750*[0]
   d10s = 750*[0]
   D2_0 = 750*[0]
   d20s = 750*[0]
   D3_0 = 750*[0]
   d30s = 750*[0]
   D4_0 = 750*[0]
   d40s = 750*[0]
   D5_0 = 750*[0]
   d50s = 750*[0]
   D6_0 = 750*[0]
   d60s = 750*[0]
   D7_0 = 750*[0]
   d70s = 750*[0]
   D8_0 = 750*[0]
   d80s = 750*[0]
   D1_1 = 750*[0]
   d11s = 750*[0]
   D2_1 = 750*[0]
   d21s = 750*[0]
   D3_1 = 750*[0]
   d31s = 750*[0]
   D4_1 = 750*[0]
   d41s = 750*[0]
   D5_1 = 750*[0]
   d51s = 750*[0]
   D6_1 = 750*[0]
   d61s = 750*[0]
   D7_1 = 750*[0]
   d71s = 750*[0]
   D8_1 = 750*[0]
   d81s = 750*[0]
   mapper ={"D8_0":[D8_0, d80s],"D7_0":[D7_0, d70s],"D6_0":[D6_0, d60s],"D5_0":[D5_0, d50s],"D4_0":[D4_0,d40s],"D3_0":[D3_0,d30s],"D2_0":[D2_0,d20s],"D1_0":[D1_0, d10s],"D8_1":[D8_1, d81s],"D7_1":[D7_1, d71s],"D6_1":[D6_1,d61s],"D5_1":[D5_1,d51s],"D4_1":[D4_1,d41s],"D3_1":[D3_1,d31s],"D2_1":[D2_1, d21s],"D1_1":[D1_1, d11s]}
   ly = ["D8_0", "D8_1", "D4_0", "D4_1", "D7_0", "D7_1", "D3_0", "D3_1"]
   lx = ["D1_0", "D1_1", "D2_0", "D2_1", "D6_0", "D6_1", "D5_0", "D5_1"]
   ql = ["D8_0", "D8_1", "D7_0", "D7_1", "D6_0", "D6_1", "D1_0", "D1_1"]
   veh = traci.vehicle.getIDList()
   avg_wait_time = 0
   avg_ql = 0
   for l in ql :
     avg_ql = avg_ql + traci.lane.getLastStepHaltingNumber(l)
   for l in ly :
     avg_wait_time = avg_wait_time + traci.lane.getWaitingTime(l)
   for l in lx :
     avg_wait_time = avg_wait_time + traci.lane.getWaitingTime(l)
   avg_wait_time = avg_wait_time/16
   wta.append(avg_wait_time)
   avg_ql = avg_ql/8 
   qla.append(avg_ql)
   for v in veh:
     lane = traci.vehicle.getLaneID(v)
     try :
       arr = mapper[lane][0]
       speed = mapper[lane][1]
     except KeyError, e:
       continue    
     if lane in ly :
       pos = abs(int(round(traci.vehicle.getPosition(v)[1])))
     else :
       pos = abs(int(round(traci.vehicle.getPosition(v)[0])))
     arr[pos-1]=1
     speed[pos-1]=traci.vehicle.getSpeed(v)
#function call experience replay
#set traffic lights
   step += 1
traci.close(False)




  
    
    
    









