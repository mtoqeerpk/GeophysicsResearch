# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 17:21:27 2017

@author: LLL
"""

import numpy as np
from tensorflow.examples.tutorials.mnist import input_data
import matplotlib.pyplot as plt

class GenData():
    def __init__(self,shape):
        self.shape=shape
        self.data=np.zeros(self.shape)
    def GenWave(self):
        
        #data=np.random.random(shape)
        #data=np.subtract(data,0.5)
        ariv=np.zeros([self.shape[0],1])
        for itrd in range(self.shape[0]):
            sbn=1+np.random.randint(30)
            for itr in range(sbn):
                f0=1+np.random.random(1)[0]*10
                Tc=1/(np.random.randint(5)+1)
                per=100
                t=np.linspace(0,1,per)
                wave=(1+np.cos(2.*np.pi*(t-Tc/2.)/Tc))*np.cos(2.*np.pi*f0*(t-Tc/2.))/2.
                nba=np.random.randint(self.shape[1]-per-1)
                ariv[itrd][0]=1
                self.data[itrd,nba:nba+per]=self.data[itrd,nba:nba+per]+wave
        mx=np.max(self.data,axis=1)
        mx=np.reshape(mx,[-1,1])
        self.data=np.multiply(np.divide(self.data,mx),0.3)
        #return ariv
        
        return self.data
    def AddNoise(self,bl=0.5):
        noise=np.random.random(self.shape)
        noise=np.subtract(noise,0.5)
        noise=np.multiply(noise,bl)
        return np.add(self.data,noise)
def my_weigh(shape):
    init=tf.truncated_normal(shape,stddev=0.1)
    return tf.Variable(init)
def my_bias(shape):
    init=tf.constant(0.1,shape=shape)
    return tf.Variable(init)
import tensorflow as tf
x = tf.placeholder(tf.float32,[50,784])
y = tf.placeholder(tf.float32,[50,784])



data1=tf.reshape(x,[50,784,1])
c1_w=my_weigh([8,1,16])
c1_b=my_weigh([16])
c1_f1=tf.nn.conv1d(data1,filters=c1_w,stride=2, padding='SAME')+c1_b
c1_f2=tf.nn.tanh(c1_f1)
c1=tf.nn.pool(c1_f2,window_shape=[2],pooling_type='MAX',strides=[2],padding='SAME')

c2_w=my_weigh([3,16,12])
c2_b=my_weigh([12])
c2_f1=tf.nn.conv1d(c1,filters=c2_w,stride=2, padding='SAME')+c2_b
c2_f2=tf.nn.tanh(c2_f1)
c2=tf.nn.pool(c2_f2,window_shape=[2],pooling_type='MAX',strides=[2],padding='SAME')

c3_w=my_weigh([3,12,24])
c3_b=my_weigh([24])
c3_f1=tf.nn.conv1d(c2,filters=c3_w,stride=1, padding='SAME')+c3_b
c3_f2=tf.nn.tanh(c3_f1)
c3=tf.nn.pool(c3_f2,window_shape=[1],pooling_type='MAX',strides=[1],padding='SAME')

c4_w=my_weigh([3,24,16])
c4_b=my_weigh([16])
c4_f1=tf.nn.conv1d(c3,filters=c4_w,stride=1, padding='SAME')+c4_b
c4_f2=tf.nn.tanh(c4_f1)
c4=tf.nn.pool(c4_f2,window_shape=[1],pooling_type='MAX',strides=[1],padding='SAME')

c5_w=my_weigh([3,16,8])
c5_b=my_weigh([8])
c5_f1=tf.nn.conv1d(c4,filters=c5_w,stride=1, padding='SAME')+c5_b
c5_f2=tf.nn.tanh(c5_f1)

c6_w=my_weigh([3,8,4])
c6_b=my_weigh([4])
c6_f1=tf.nn.conv1d(c5_f2,filters=c6_w,stride=1, padding='SAME')+c6_b
c6_f2=tf.nn.tanh(c6_f1)

data2=tf.reshape(c6_f2,[50,49*4])

W1 = my_weigh(([49*4,784]))
b1 = my_bias(([784]))
r1_f=tf.matmul(data2,W1)+b1
r1=tf.nn.tanh(r1_f)





kp_prb=tf.placeholder('float')
result=tf.nn.dropout(r1,kp_prb)

ce = tf.reduce_mean(tf.abs(r1-y))

train_step = tf.train.AdamOptimizer(1e-2).minimize(ce)

sess = tf.InteractiveSession()
tf.global_variables_initializer().run()

batch = GenData([50,784])
data=batch.GenWave()
data_noise=batch.AddNoise(0.1)
#print(sess.run(tf.shape(c2), feed_dict={x: data_noise, y: data,kp_prb:0.5}))



for itr in range(3000):
    data=batch.GenWave()
    data_noise=batch.AddNoise(0.3)
    sess.run(train_step, feed_dict={x: data_noise, y: data,kp_prb:0.5})
    #print(data[0])
    #plt.plot(data_noise[0])
    if(itr%100==0):
        print("%d:%f"%(itr,sess.run(ce, feed_dict={x: data_noise, y: data,kp_prb:1.})))
outdata=sess.run(result, feed_dict={x: data_noise, y: data,kp_prb:1.})
plt.subplot(511)
plt.plot(data_noise[0],color='b',lw=1,alpha=0.2)
plt.plot(outdata[0],color='cornflowerblue',lw=3)
plt.plot(data[0],color='orange',lw=1,alpha=0.5)

plt.subplot(512)
plt.plot(data_noise[1],color='b',lw=1,alpha=0.2)
plt.plot(outdata[1],color='cornflowerblue',lw=3)
plt.plot(data[1],color='orange',lw=1,alpha=0.5)

plt.subplot(513)
plt.plot(data_noise[2],color='b',lw=1,alpha=0.2)
plt.plot(outdata[2],color='cornflowerblue',lw=3)
plt.plot(data[2],color='orange',lw=1,alpha=0.5)

plt.subplot(514)
plt.plot(data_noise[3],color='b',lw=1,alpha=0.2)
plt.plot(outdata[3],color='cornflowerblue',lw=3)
plt.plot(data[3],color='orange',lw=1,alpha=0.5)

import scipy.signal as signal
b, a = signal.iirdesign([0.02, 0.3], [0.01, 0.4], 2, 40)
out = signal.lfilter(b, a, data_noise[3])

plt.subplot(515)
plt.plot(data_noise[3],color='b',lw=1,alpha=0.2)
plt.plot(out,color='cornflowerblue',lw=3)
plt.plot(data[3],color='orange',lw=1,alpha=0.5)

plt.show()

outfile=open("noise_data.txt")
for itry in range(3):
    outfile_no=open("no_data"+str(itry)+".txt")
    outfile_rw=open("rw_data"+str(itry)+".txt")
    outfile_fl=open("fl_data"+str(itry)+".txt")
    for itrx in range(784):
        outfile_no.write(str(data_noise[itry][itrx])+"\n")
        outfile_rw.write(str(data[itry][itrx])+"\n")
        outfile_fl.write(str(data[itry][itrx])+"\n")
        

















