import numpy as np
fp = open("tokens.txt", "r")
data = fp.readlines()
dic = {}
ctr = 0
for i in data:
    ctr += 1
    i = i.split(' ')
    dic[i[0]] = ctr

vocab_size = ctr
fp.close()

fp = open("tokenlines_100.txt","r")
data1 = fp.readlines()
n = len(data1)
fp32 = open("tokenlinetest.txt", "r")
data32 = fp32.readlines()
n32 = len(data32)


import tensorflow as tf
from tensorflow.python.ops import rnn_cell
from tensorflow.python.ops import rnn

hm_epochs = 10
n_classes = vocab_size
batch_size = 100
chunk_size = ctr
n_chunks = 1
rnn_size = 256

x = tf.placeholder('float', [None, n_chunks, chunk_size])
y = tf.placeholder('float')

def getbatch(i):
    #for j in range(batch_size):
    temp = data1[i].split(' ')
    #print(temp)
    batch_x = []
    batch_y = []
    token_counter = 0
    for k in temp:
        temp_x = [0] * vocab_size
        temp_y = [0] * vocab_size
        if k not in dic:
            k = "<RARE_TOKEN>"
        #print(k)

        if token_counter < batch_size:
            temp_x[dic[k]-1] += 1
            batch_x.append(temp_x)
            if token_counter > 0:
                temp_y[dic[k]-1] += 1
                batch_y.append(temp_y)
            token_counter = token_counter + 1
        else:
            temp_y[dic[k]-1] += 1
            batch_y.append(temp_y)
    '''fbatch_x = []
    fbatch_y = []
    for l in batch_x:
        fbatch_x += l
    for m in batch_y:
        fbatch_y += m
    return np.array(fbatch_x).reshape(1, 87600), np.array(fbatch_y).reshape(1, 87600)'''
    return np.array(batch_x), np.array(batch_y)

def recurrent_neural_network(x):
    layer = {'weights':tf.Variable(tf.random_normal([rnn_size, n_classes])),
                      'biases':tf.Variable(tf.random_normal([n_classes]))}

    x = tf.transpose(x, [1,0,2])
    x = tf.reshape(x, [-1, chunk_size])
    x = tf.split(0, n_chunks, x)

    lstm_cell = rnn_cell.BasicLSTMCell(rnn_size)
    outputs, states = rnn.rnn(lstm_cell, x, dtype=tf.float32)

    output = tf.matmul(outputs[-1],layer['weights']) + layer['biases']

    return output

def train_neural_network(x):
    prediction = recurrent_neural_network(x)
    cost = tf.reduce_mean( tf.nn.softmax_cross_entropy_with_logits(prediction,y) )
    optimizer = tf.train.AdamOptimizer().minimize(cost)
    
    with tf.Session() as sess:
        sess.run(tf.initialize_all_variables())

        for epoch in range(hm_epochs):
            epoch_loss = 0
            for i in range(len(data1)):
                epoch_x, epoch_y = getbatch(i)
                #print(epoch_x.shape, batch_size, n_chunks , chunk_size)
                epoch_x = epoch_x.reshape((batch_size, n_chunks, chunk_size))
                _, c = sess.run([optimizer, cost], feed_dict={x: epoch_x, y: epoch_y})
                epoch_loss += c
                #print (i)
            print('Epoch', epoch, 'completed out of',hm_epochs,'loss:',epoch_loss/1000)

        for i in range(len(data32)):
                epoch_xx, epoch_yy = getbatch(i)
                #print(epoch_x.shape, batch_size, n_chunks , chunk_size)
                epoch_xx = epoch_xx.reshape((batch_size, n_chunks, chunk_size))
            
        correct = tf.equal(tf.argmax(prediction, 1), tf.argmax(y, 1))

        accuracy = tf.reduce_mean(tf.cast(correct, 'float'))
        print('Accuracy:',accuracy.eval({x:epoch_xx, y:epoch_yy}))

train_neural_network(x)

fp.close()
fp32.close()
