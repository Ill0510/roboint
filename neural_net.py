import numpy as np
from sklearn.datasets import fetch_mldata
import pylab as pl
import matplotlib.pyplot as plt
import random as ra
from numpy.random import *
import sys,time

mnist = fetch_mldata('MNIST original')
mnist.data = mnist.data.astype(np.float32)
mnist.data /= 255
mnist.target = mnist.target.astype(np.int32)

N = 60000
x_train,x_test = np.split(mnist.data,[N])
y_train,y_test = np.split(mnist.target,[N])
N_test = y_test.size

data_num = 28*28
input_vector_length = data_num
inter_vector1_length = 300
inter_vector2_length = 300
output_vector_length = 10
learn_ratio = 0.01
max_learn_ratio = 0.5

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

def neural_net(learn_gain):
    weight_vector1 = rand(input_vector_length,inter_vector1_length)/np.sqrt(input_vector_length)
    weight_vector2 = rand(inter_vector1_length , inter_vector2_length)/np.sqrt(inter_vector1_length)
    weight_vector3 = rand(inter_vector2_length , output_vector_length)/np.sqrt(inter_vector2_length)
    
    b1 = 0
    b2 = 0
    db1 = 0
    db2 = 0
    dw1 = 0
    dw3 = 0
    
    train_num = N
    warukazu = 1
    
    order=np.arange(train_num)
    np.random.shuffle(order)
    
    for var in range(0,train_num/warukazu):
        seed = order[var]
        out = var * 100 / train_num
        out_str = "\r learning now [" +str(out) + "%]" 
        sys.stdout.write(out_str)
        sys.stdout.flush()
        input_vector = x_train[seed]
        inter_vector1 = sigmoid(np.dot(input_vector,weight_vector1)+b1)
        output_vector = softmax(np.dot(inter_vector1,weight_vector3)+b2)
        minus = np.zeros(output_vector_length)
        minus[y_train[seed]] = 1
        reverse_vector3 = output_vector - minus
        db2 = reverse_vector3
        dw3 = np.dot(inter_vector1.reshape(inter_vector1_length,1),reverse_vector3.reshape(1,output_vector_length))
        reverse_vector2 = np.dot(reverse_vector3,weight_vector3.T)
        reverse_vector1 = reverse_vector2 * (1.0-inter_vector1) * inter_vector1
        db1 = reverse_vector1
        dw1 = np.dot(input_vector.reshape(input_vector_length,1),reverse_vector1.reshape(1,inter_vector1_length))
        b1 -= learn_gain * db1
        b2 -= learn_gain * db2
        weight_vector3 -= learn_gain * dw3
        weight_vector1 -= learn_gain * dw1
        
    sys.stdout.write("\r=======================================================\n")
    sys.stdout.flush()
    time.sleep(0.01)
    print "learning finished"
    
    print "learn ratio is "+ str(learn_gain)
    test_num = 10000
    correct_count = 0
    count = 0
    
    for var in range(0,test_num):
        seed = ra.randint(0,test_num-1)
        input_vector = x_test[seed]
        inter_vector1 = sigmoid(np.dot(input_vector,weight_vector1)+b1)
        output_vector = softmax(np.dot(inter_vector1,weight_vector3)+b2)
        if np.argmax(output_vector) == y_test[seed]:
            correct_count += 1
    
    print "presition is " + str(correct_count * 100.0 / test_num) + " %"
    return correct_count

'''
learn_ratio_step = 0.01
learn_count = int((max_learn_ratio - learn_ratio) / learn_ratio_step + 1)
print learn_count
learn_count_single = 5
learn_count_all = learn_count * learn_count_single
#learn_count = 5
result=np.zeros(learn_count)
for var in range(0,learn_count):
    for a in range(0,learn_count_single):
        tmp = neural_net(learn_ratio)
        print tmp
        result[var] += tmp
    learn_ratio += learn_ratio_step
    
ans = (np.argmax(result) + 1) * 0.01
print "best learn ratio is " + str(ans)
print result
'''

neural_net(0.1)
