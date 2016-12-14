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
from keras.layers import Dense, Activation, LSTM
from keras.layers.wrappers import TimeDistributed




if (len(sys.argv) != 4):
	print("USAGE: <trainfile> <testfile> <no_epochs>")
else:
	fp = open("tokens.txt", "r")
	data = fp.readlines()
	dic = {}
	ctr = 0
	for i in data:
	    i = i.split(' ')
	    dic[i[0]] = ctr
	    ctr+=1
	fp.close()

	reverse_dic = [0]*(ctr+1)
	for element in dic:
		reverse_dic[dic[element]]=element
		#print(dic[element], element)

	fp = open(sys.argv[1],"r", encoding='latin1')
	data1 = fp.readlines()
	n1 = len(data1)
	fp32 = open(sys.argv[2], "r")
	data32 = fp32.readlines()
	n32 = len(data32)


	vocab_size = ctr
	hm_epochs = int(sys.argv[3])
	n_classes = vocab_size
	batch_size = 10
	max_seq_len = 30
	

	def getbatch(i, data_to_read):
	    #for j in range(batch_size):
	    temp = data_to_read[i].split(' ')
	    #print(temp)
	    n_tokens = len(temp)
	    n_tokens = n_tokens-1
	    #print(temp)
	    batch_x = []
	    batch_y = []
	    ggg = []
	    token_counter = 0
	    for k in range(0, n_tokens-1):
	        #print(k)
	        temp_x = [0] * vocab_size
	        temp_y = [0] * vocab_size
	        if temp[k] not in dic:
	            temp[k] = "<RARE_TOKEN>"
	        if temp[k+1] not in dic:
	            #print(temp[k+1], "made rare")
	            temp[k+1] = "<RARE_TOKEN>"
	        if k == n_tokens-2:
	        	temp[k+1] = temp[k+1]#[:-1]
	        temp_x[dic[temp[k]]] = 1
	        temp_y[dic[temp[k+1]]] = 1
	        batch_x.append(temp_x)
	        batch_y.append(temp_y)
	        index=[dic[temp[k+1]]]
	        ggg.append(index)

	    batch_x = np.array(batch_x)
	    batch_y = np.array(batch_y)
	    ggg = np.array(ggg)
	    batch_x = batch_x.transpose()
	    batch_x = sequence.pad_sequences(batch_x, maxlen=max_seq_len)
	    batch_x = batch_x.transpose()
	    batch_y = batch_y.transpose()
	    batch_y = sequence.pad_sequences(batch_y, maxlen=max_seq_len)
	    batch_y = batch_y.transpose()
	    ggg = ggg.transpose()
	    ggg = sequence.pad_sequences(ggg, maxlen=max_seq_len, value=-1)
	    ggg = ggg.transpose()

	    return batch_x, batch_y, ggg

	



	print('Building training model...')
	hiddenStateSize = 128
	hiddenLayerSize = 128
	model = Sequential()

	model.add(LSTM(hiddenStateSize, return_sequences = True, input_shape=(max_seq_len, vocab_size)))
	model.add(TimeDistributed(Dense(hiddenLayerSize)))
	model.add(TimeDistributed(Activation('relu'))) 
	model.add(TimeDistributed(Dense(vocab_size)))  
	model.add(TimeDistributed(Activation('softmax')))
	
	model.compile(loss='categorical_crossentropy', optimizer = RMSprop(lr=0.001))

	#cprint(model.summary()) 

	print("Training lines:",n1)
	i=0
	#while i < n1-50:
	temp_testx=[]
	temp_testy=[]
	for k in range(0, n1):
		x, y, g = getbatch(k, data1)
		x=x.tolist()
		y=y.tolist()
		temp_testx.append(x)
		temp_testy.append(y)
		print("Making in progress: ", (k/n1)*100, end="\r", flush=True)
	temp_testx = np.array(temp_testx)
	temp_testy = np.array(temp_testy)
	#i = i+50
	print(temp_testx.shape, temp_testy.shape)
	model.fit(temp_testx, temp_testy, batch_size=n1, nb_epoch=50, verbose=1)
	

	for k in range(0, n32):
		x, y, g = getbatch(k, data32)
		x=x.tolist()
		temp_testx=[x]
		x=np.array(temp_testx)
		outputs = model.predict(x)
		outputs = outputs[0]
		log_sum = 0
		for j in range(0,30):
			log_sum += math.log(outputs[j][g[j][0]],2)
		entropy = -(log_sum/30)
		print(entropy, k)
	


##########################################################################
'''
print("Training lines:",n1)
	for i in range(0, n1):
		x, y, g = getbatch(i, data1)
		x=x.tolist()
		temp_testx=[x]
		temp_testx=np.array(temp_testx)
		y=y.tolist()
		temp_testy=[y]
		temp_testy=np.array(temp_testy)

		history=model.fit(temp_testx, temp_testy, batch_size=1, nb_epoch=3, verbose=0)
		print("Training in progress: ", (i/n1)*100, end="\r", flush=True)
		if i % 100 == 0:
			print("Loss: ", history.history['loss'])
'''



