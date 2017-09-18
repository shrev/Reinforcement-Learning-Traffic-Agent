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
import theano
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.layers.convolutional import Convolution2D
from keras.utils import np_utils
from keras import backend as k
from keras.layers import Merge
from keras.layers.core import Flatten
import random

# Independent code 

r=16
c=12

curr_velocity_DTSE=np.random.random_integers(10,100,(1,r, c,1))
curr_boolean_DTSE=np.random.random_integers(0,1,(1,r, c,1))
P=np.random.random_sample((1, 7))

model1=Sequential()
model1.add(Convolution2D(16, 4, 4, border_mode='valid', input_shape=(r,c,1), subsample=(2,2), activation='relu'))
model1.add(Convolution2D(32, 2, 2, border_mode='valid', subsample=(2,2), activation='relu'))

#print model1.output_shape

model2=Sequential()
model2.add(Convolution2D(16, 4, 4, border_mode='valid', input_shape=(r,c,1), subsample=(2,2), activation='relu'))
model2.add(Convolution2D(32, 2, 2, border_mode='valid', subsample=(2,2), activation='relu'))

#print model2.output_shape

merged = Merge([model1, model2], mode='concat')

model3= Sequential()
model3.add(merged)
model3.add(Flatten())	
model3.add(Dense(128, activation='relu'))
model3.add(Dense(64, activation='relu'))
model3.add(Dense(64, activation='relu'))
model3.add(Dense(7, activation='linear'))

wta = []
qla = []

def getStates():
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
   veh = traci.vehicle.getIDList()
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
   curr_states = np.concatenate(([D8_0], [D8_1], [D4_0], [D4_1], [D7_0], [D7_1], [D3_0], [D3_1], [D1_0], [D1_1], [D2_0], [D2_1], [D6_0], [D6_1], [D5_0], [D5_1] ), axis=0)
   curr_states = curr_states[:,0:12]
   curr_speed = np.concatenate(([d80s],[d81s],[d40s],[d41s],[d70s],[d71s],[d30s],[d31s],[d10s],[d11s],[d20s],[d21s],[d60s],[d61s],[d50s],[d51s]),axis=0)
   curr_speed = curr_speed[:,0:12]
   #print curr_states
   #print curr_speed.shape
   return curr_states,curr_speed

def changelights(num) :
  states = traci.trafficlights.getRedYellowGreenState("3")
  n = states[0:4]
  s = states[7:11]
  e = states[4:7]
  w = states[11:14]
  if num==0:
    n = "GGGG"
    s = "GGGG"
    e = "rrr"
    w = "rrr"
  if num==1:
    n = "rrrr"
    s = "rrrr"
    w = "GGG"
    e = "GGG"
  if num==2:
    n = "GgGg"
    s = "GgGg"
    e = "rrr"
    w="rrr"
  if num==3:
    e = "GgG"
    w = "GgG"
    n="rrrr"
    s="rrrr"
  if num==4:
    n = "yyyy"
    s = "yyyy"
    e = "GGG"
    w = "GGG"
  if num==5:
    e = "yyy"
    w = "yyy"
    n = "GGGG"
    s="GGGG"
  if num==6:
    n = "rrrr"
    s = "rrrr"
    e = "rrr"
    w = "rrr"
  final = n+e+s+w
  print "i come here"
  traci.trafficlights.setRedYellowGreenState("3", final)
  traci.trafficlights.setPhaseDuration("3", 4000)

def getdelay():
   ly = ["D8_0", "D8_1", "D4_0", "D4_1", "D7_0", "D7_1", "D3_0", "D3_1"]
   lx = ["D1_0", "D1_1", "D2_0", "D2_1", "D6_0", "D6_1", "D5_0", "D5_1"]
   ql = ["D8_0", "D8_1", "D7_0", "D7_1", "D6_0", "D6_1", "D1_0", "D1_1"]
   avg_wait_time = 0
   avg_ql = 0
   for l in ql :
     avg_ql = avg_ql + traci.lane.getLastStepHaltingNumber(l)
   for l in ly :
     avg_wait_time = avg_wait_time + traci.lane.getWaitingTime(l)
   for l in lx :
     avg_wait_time = avg_wait_time + traci.lane.getWaitingTime(l)
   avg_wait_time = avg_wait_time/16
   avg_ql = avg_ql/8 
   wta.append(avg_wait_time)
   qla.append(avg_ql)
   return avg_wait_time
 
   


#CNN


buffer=5
batchSize=5
replay=[]

rms = keras.optimizers.RMSprop()
model3.compile(loss='mse', optimizer=rms)

epochs = 1000
gamma = 0.95 #since it may take several moves to goal, making gamma high
epsilon = 1
old_reward =0

sumoBinary = "/usr/bin/sumo-gui"
sumoCmd = [sumoBinary, "-c", "rl.sumo.cfg"]
traci.start(sumoCmd)	
print "im here"
old_delay = getdelay()
traci.simulationStep()
traci.simulationStep()
print old_delay
curr_boolean_DTSE,curr_velocity_DTSE = getStates()
print "this worked too"



for i in range(epochs):
	status = 1
	#while game still in progress
	h=0
      #  if i==0 :
          
         
        
        curr_boolean_DTSE=np.array(curr_boolean_DTSE).reshape(1,16,12,1)
	curr_velocity_DTSE=np.array(curr_velocity_DTSE).reshape(1,16,12,1)
	
        #print curr_boolean_DTSE
        
        qval=model3.predict([curr_boolean_DTSE ,curr_velocity_DTSE], batch_size=1)
        print i
	if (random.random() < epsilon): #choose random action
		action = np.random.randint(0,7)
	else: #choose best action from Q(s,a) values
	    action = (np.argmax(qval))
              
	#Take action, observe new state S'
        print action
        changelights(action)
        traci.simulationStep()
	traci.simulationStep()
	traci.simulationStep()
	traci.simulationStep()
        #do above 4 times for step+4
	new_boolean_DTSE, new_velocity_DTSE = getStates()
	new_boolean_DTSE=np.array(new_boolean_DTSE).reshape(1,16,12,1)
	new_velocity_DTSE=np.array(new_velocity_DTSE).reshape(1,16,12,1)
	#Observe reward
	new_delay = getdelay()
	if old_delay!=0:
		reward=(old_delay-new_delay)/old_delay
	else:
		reward=old_delay-new_delay

	#Experience replay storage
	if (len(replay) < buffer): #if buffer not filled, add to it
	    replay.append((curr_boolean_DTSE, curr_velocity_DTSE, action, reward, new_boolean_DTSE, new_velocity_DTSE))
	else: #if buffer full, overwrite old values
		if (h < (buffer-1)):
			h += 1
		else:
		    h = 0
		replay[h] = (curr_boolean_DTSE, curr_velocity_DTSE, action, reward, new_boolean_DTSE, new_velocity_DTSE)
		#randomly sample our experience replay memory
		minibatch = random.sample(replay, batchSize)
		X_train = []
		W_train = []
		y_train = []

		for memory in minibatch:
		    #Get max_Q(S',a)
			curr_boolean_DTSE, curr_velocity_DTSE, action, reward, new_boolean_DTSE, new_velocity_DTSE = memory
			old_qval = model3.predict([curr_boolean_DTSE, curr_velocity_DTSE], batch_size=1)
			newQ = model3.predict([new_boolean_DTSE, new_velocity_DTSE], batch_size=1)
			
			#print newQ
			maxQ = np.max(newQ)
			y = np.zeros((1,7))
			y[:] = old_qval[:]

			update = (reward + (gamma * maxQ))

			y[0][action] = update
			X_train.append(curr_boolean_DTSE)
			W_train.append(curr_velocity_DTSE)
			y_train.append(y)
			#X_train.append(old_state.reshape(64,))
			#y_train.append(y.reshape(4,))

		X_train = np.array(X_train).reshape(5,16,12,1)
		W_train = np.array(W_train).reshape(5,16,12,1)
		y_train = np.array(y_train).reshape(5,7)
		model3.fit([X_train, W_train], y_train, batch_size=batchSize, nb_epoch=1, verbose=1)
		curr_boolean_DTSE = new_boolean_DTSE
		curr_velocity_DTSE = new_velocity_DTSE
		
		
	old_delay=new_delay	

	if epsilon > 0.1: #decrement epsilon over time
	    epsilon -= (1/epochs)


traci.close(False)

np.savetxt("wta_exp3", wta)
np.savetxt("qla-exp3",qla)
