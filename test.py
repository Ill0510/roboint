import numpy as np
#from sklearn.datasets import load_digit
from sklearn.datasets import fetch_mldata
import pylab as pl
import matplotlib.pyplot as plt
#from math import exp
#from random import random
import random as ra
from numpy.random import *
import sys

mnist = fetch_mldata('MNIST original')
mnist.data = mnist.data.astype(np.float32)
mnist.data /= 255
mnist.target = mnist.target.astype(np.int32)

N = 60000
x_train,x_test = np.split(mnist.data,[N])
y_train,y_test = np.split(mnist.target,[N])
N_test = y_test.size

data_num = 28*28
input_vector_length = data_num + 1
inter_vector1_length = 300
inter_vector2_length = 300
output_vector_length = 10
learn_gain = 0.1

sig_gain = 1

def sigmoid(x):
    return 1.0/(1+np.exp(x*(-1)*sig_gain))

def softmax(x):
    e = np.exp(x - np.max(x))  # prevent overflow
    if e.ndim == 1:
        return e / np.sum(e, axis=0)
    else:  
        return e / np.array([np.sum(e, axis=1)]).T
    

def draw_digit(data):
    size = 28
    plt.figure(figsize = (2.5,3))
    X,Y = np.meshgrid(range(size),range(size))
    Z = data.reshape(size,size)
    Z = Z[::-1,:]
    plt.xlim(0,27)
    plt.ylim(0,27)
    plt.pcolor(X,Y,Z)
    plt.gray()
    plt.tick_params(labelbottom = "off")
    plt.tick_params(labelleft = "off")
    plt.show()

def make_delta_k(vector,err):
    return sig_gain*err*vector*(1-vector)

def make_delta_h(vector,sigma_vector):
    return sig_gain*vector*(1-vector)*sigma_vector

def make_delta_i(vector,sigma_vector):
    return sig_gain*vector*(1-vector)*sigma_vector

def neural_net(input_vector,w1,w2,w3):
    inter_vector1 = np.r_[1,sigmoid(np.dot(w1,input_vector))]
    inter_vector2 = np.r_[1,sigmoid(np.dot(w2,inter_vector1))]
    output =  sigmoid(np.dot(w3,inter_vector2))
    return output
    
weight_vector1 = rand(inter_vector1_length-1 , input_vector_length)/np.sqrt(input_vector_length)
weight_vector2 = rand(inter_vector2_length-1 , inter_vector1_length)/np.sqrt(inter_vector1_length)
weight_vector3 = rand(output_vector_length , inter_vector2_length)/np.sqrt(inter_vector2_length)
#print weight_vector3
#inter_vector1 = np.zeros(inter_vector1_length)
#input_vector = np.zeros(input_vector_length)
#output_vector = np.zeros(output_vector_length)

train_num = N

#draw_digit(x_test[9999])
#print y_test[9999]

for var in range(0,train_num):
    seed = ra.randint(0,train_num-1)
    if seed%100 ==0:
        input_vector = np.r_[1,x_train[seed]]
        inter_vector1 = np.r_[1,sigmoid(np.dot(weight_vector1,input_vector))]
        #inter_vector1 = inter_vector1 / np.linalg.norm(inter_vector1)
        #inter_vector2 = np.r_[1,sigmoid(np.dot(weight_vector2,inter_vector1))]
        #inter_vector2 = inter_vector2 / np.linalg.norm(inter_vector2)
        output_vector = softmax(np.dot(weight_vector3,inter_vector1))
        print output_vector
        print y_train[seed]
        minus = np.zeros(output_vector_length)
        minus[y_train[seed]] = 1
        err = output_vector - minus
        delta_k =  make_delta_k(output_vector,err)
        #delta_h = make_delta_h(inter_vector2,np.dot(weight_vector3.T,delta_k))[1:inter_vector2_length]
        #weight_vector2 -= learn_gain * np.dot(np.matrix(delta_h).T , np.matrix(inter_vector1) )
        delta_i = make_delta_i(inter_vector1,np.dot(weight_vector3.T,delta_k))[1:inter_vector1_length]
        weight_vector3 -= learn_gain * np.dot(np.matrix(delta_k).T , np.matrix(inter_vector1) )
        weight_vector1 -= learn_gain * np.dot(np.matrix(delta_i).T , np.matrix(input_vector))
    else:
        a=1

print "=========================================================================================="

test_num = 10000
correct_count = 0

for var in range(0,test_num):
    seed = ra.randint(0,test_num-1)
    if seed%100 == 0:
        input_vector = np.r_[1,x_test[seed]]
        inter_vector1 = np.r_[1,sigmoid(np.dot(weight_vector1,input_vector))]
        #inter_vector1 = inter_vector1 / np.linalg.norm(inter_vector1)
        #inter_vector2 = np.r_[1,sigmoid(np.dot(weight_vector2,inter_vector1))]
        #inter_vector2 = inter_vector2 / np.linalg.norm(inter_vector2)
        output_vector = softmax(np.dot(weight_vector3,inter_vector1))
        if np.argmax(output_vector) == y_test[var]:
            correct_count += 1
        #print inter_vector1
        print output_vector
        print y_test[seed]
    else:
        a=1

#print weight_vector1

#print correct_count / test_num * 100
#print delta_k.size
