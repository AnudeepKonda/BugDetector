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

model = load_model("my_model.h5")

fp = open(sys.argv[3], "r")
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
hm_epochs = int(sys.argv[4])
n_classes = vocab_size
batch_size = 10
max_seq_len = 30
	

def getbatch(i, data_to_read):
    #for j in range(batch_size):
    temp = data_to_read[i].split(' ')
	#print(temp)
    n_tokens = len(temp)
    if n_tokens != 2:
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

    return batch_x, batch_y, ggg, n_tokens
fp33 = open("final_entropies.txt", "w")

entropies = [0]*n32
for k in range(0, n32):
    x, y, g, n = getbatch(k, data32)
    x=x.tolist()
    temp_testx=[x]
    x=np.array(temp_testx)
    outputs = model.predict(x)
    outputs = outputs[0]
    log_sum = 0
    for j in range(30-n,30-1):
        if outputs[j][g[j][0]] == 0:
          outputs[j][g[j][0]] += 0.0000000000000000000000000000000000000000000000000000000001
        log_sum += math.log(outputs[j][g[j][0]],2)
    entropy = -(log_sum/(n))
    entropies[k]=entropy
    s = ''.join(data32[k])[:-1]+" "+str(entropy)+" "+str(outputs[28][g[28][0]])+"\n"
    fp33.write(s)
    print("Progress: ", (k/n32)*100, end="\r", flush=True)

print(len(entropies), min(entropies), max(entropies))
fp33.close()
fp32.close()
fp.close() 


