import os
import sys
import math
import numpy as np
import tensorflow as tf
from keras.datasets import imdb
from keras.models import Sequential
from keras.callbacks import History
from keras.models import load_model
from keras.optimizers import RMSprop
from keras.preprocessing import sequence
from keras.layers import Dense, Activation, LSTM
from keras.layers.wrappers import TimeDistributed

model=load_model("classifier.h5")

fp = open("final_entropies.txt", )
data = fp.readlines()
n1 = len(data)
prob = [0]*n1
entropy = [0]*n1
bugflag = [0]*n1
for k in range(0, len(data)):
	temp_data = data[k].split(" ")
	n = len(temp_data)
	prob[k]=temp_data[n-1]
	entropy[k]=temp_data[n-2]
	bugflag[k]=temp_data[n-3]
	#print(temp_data[n-1])
#print(model.summary())

train_size = math.floor(0.8 * n1)
print(train_size) 

maxi = -1000
mini = 1000 
for k in range(train_size, n1):
	input_val = np.array([float(prob[k])])
	output_val = float(bugflag[k])
	proba = float(entropy[k])
	print(input_val, output_val)
	x = model.predict(input_val)
	print(x)
	print("\n")




