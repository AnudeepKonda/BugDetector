import os
import sys
import math
import numpy as np
import tensorflow as tf
from keras.datasets import imdb
from keras.models import Sequential
from keras.callbacks import History
from keras.optimizers import RMSprop
from keras.preprocessing import sequence
from keras.layers import Dense, Activation, LSTM, Dropout
from keras.layers.wrappers import TimeDistributed


fp = open("final_entropies.txt", "r")
data = fp.readlines()
n1 = len(data)
entropy = [0]*n1
bugflag = [0]*n1
prob = [0]*n1
for k in range(0, len(data)):
	temp_data = data[k].split(" ")
	n = len(temp_data)
	prob[k] = temp_data[n-1]
	entropy[k]=temp_data[n-2]
	bugflag[k]=temp_data[n-3]

model = Sequential()
model.add(Dense(5, input_dim=1, init='uniform', activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(5, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])
#print(model.summary())

train_size = math.floor(0.8 * n1)
print(train_size) 


for j in range(0, 20):
	epoch_loss = 0
	for k in range(0, train_size):
		input_val = np.array([float(prob[k])])
		output_val = np.array([float(bugflag[k])])
		#print(input_val, output_val)
		history = model.fit(input_val, output_val, batch_size=1, nb_epoch=1, verbose=0)
		#print(history.history['loss'], k, end="\r", flush=True)
		epoch_loss += history.history['loss'][0]
		print("progress :", (float(k)/float(train_size))*100, end="\r", flush=True)
	print("Epoch loss: ", (float(epoch_loss)/float(train_size)) , "at epoch ", j)


model.save('classifier.h5')



