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

r=16
c=8

curr_velocity_DTSE=np.random.random_integers(10,100,(1,r, c,1))
curr_boolean_DTSE=np.random.random_integers(0,1,(1,r, c,1))
P=np.random.random_sample((1, 7))

print curr_velocity_DTSE.shape
print curr_boolean_DTSE.shape

model1=Sequential()
model1.add(Convolution2D(16, 4, 4, border_mode='valid', input_shape=(r,c,1), subsample=(2,2), activation='relu'))
model1.add(Convolution2D(32, 2, 2, border_mode='valid', subsample=(2,2), activation='relu'))

print model1.output_shape

model2=Sequential()
model2.add(Convolution2D(16, 4, 4, border_mode='valid', input_shape=(r,c,1), subsample=(2,2), activation='relu'))
model2.add(Convolution2D(32, 2, 2, border_mode='valid', subsample=(2,2), activation='relu'))

print model2.output_shape

merged = Merge([model1, model2], mode='concat')

model3= Sequential()
model3.add(merged)
model3.add(Flatten())	
model3.add(Dense(128, activation='relu'))
model3.add(Dense(64, activation='relu'))
model3.add(Dense(64, activation='relu'))
model3.add(Dense(7, activation='linear'))

#print model3.output_shape

#p=[NSG, EWG, NSLG, EWLG, NSY, EWY, R]

def takeAction(curr_boolean_DTSE, curr_velocity_DTSE, action):
	return curr_boolean_DTSE, curr_velocity_DTSE

def getReward(new_boolean_DTSE, new_velocity_DTSE):
	return 0.5

def Q_Cnn_Train(curr_velocity_DTSE,curr_boolean_DTSE,p):
	

	buffer=5
	batchSize=5
	replay=[]

	rms = keras.optimizers.RMSprop()
	model3.compile(loss='mse', optimizer=rms)

	epochs = 10
	gamma = 0.95 #since it may take several moves to goal, making gamma high
	epsilon = 1

	for i in range(epochs):
		status = 1
		#while game still in progress
		h=0

		while(status <=10):
			qval=model3.predict([curr_boolean_DTSE ,curr_velocity_DTSE], batch_size=1)

			if (random.random() < epsilon): #choose random action
				action = np.random.randint(0,7)
			else: #choose best action from Q(s,a) values
			    action = (np.argmax(qval))
			#Take action, observe new state S'

			new_boolean_DTSE, new_velocity_DTSE = takeAction(curr_boolean_DTSE, curr_velocity_DTSE, action)
			#Observe reward
			reward = getReward(new_boolean_DTSE, new_velocity_DTSE)


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
					
					print newQ
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

				X_train = np.array(X_train).reshape(5,16,8,1)
				W_train = np.array(W_train).reshape(5,16,8,1)
				y_train = np.array(y_train).reshape(5,7)
				model3.fit([X_train, W_train], y_train, batch_size=batchSize, nb_epoch=1, verbose=1)
				curr_boolean_DTSE = new_boolean_DTSE
				curr_velocity_DTSE = new_velocity_DTSE

			

    		if epsilon > 0.1: #decrement epsilon over time
        	    epsilon -= (1/epochs)

			
Q_Cnn_Train(curr_velocity_DTSE,curr_boolean_DTSE,P)
print "Done"

