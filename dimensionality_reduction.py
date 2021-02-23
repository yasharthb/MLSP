# -*- coding: utf-8 -*-
"""Dimensionality-reduction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1QdScdaUna5W18L-6-kWd8J8tkZQ_MvUQ
"""

from __future__ import division

import numpy as np
import keras
from keras.datasets import mnist

import matplotlib.pyplot as plt

from mpl_toolkits import mplot3d

(x_train, y_train), (x_test, y_test) = mnist.load_data()
print(x_train.shape)
print(y_train.shape)
print(x_test.shape)
print(y_test.shape)

x_train_scaled=x_train/255
x_test_scaled=x_test/255

fig, ax = plt.subplots(3,5, figsize=(10,7), subplot_kw={'xticks':(), 'yticks': ()})
ax = ax.ravel()
for i in range(15):
    pixels = x_train[i].reshape(-1,28)
    ax[i].imshow(pixels, cmap='viridis')
    ax[i].set_title("Digit - " + str(y_train[i]))
plt.imshow(pixels, cmap='gray')
plt.show()

def NMF(V,k):
    W=np.random.random((V.shape[0],k))
    H=np.random.random((k,V.shape[1]))
    epsW=np.ones((V.shape[0],k))*0.00001
    epsH=np.ones((k,V.shape[1]))*0.00001
    Nh=np.matmul(W.T,V)
    Dh=np.matmul(np.matmul(W.T,W),H)+epsH
    
    H=np.multiply(H, Nh/Dh)
    iterations=60
    threshold=0.00001
    for iter in range(iterations):
        Nw=np.matmul(V,H.T)
        Dw=np.matmul(np.matmul(W,H),H.T)+epsW
        W=np.multiply(W,Nw/Dw)
        
        Nh=np.matmul(W.T,V)
        Dh=np.matmul(np.matmul(W.T,W),H)+epsH
        H=np.multiply(H, Nh/Dh)
        
        if np.abs(np.sum(V-np.matmul(W,H)) )< threshold:
            break
        print(np.abs(np.sum(V-np.matmul(W,H))))
        
    return W

V=np.reshape(x_train_scaled,(60000, 784))
W=NMF(V.T,2)

def reconstruct_from_nmf(V,W,k):
    print(V.shape)
    print(W.shape)
    H=np.random.random((k,V.shape[1]))
    epsH=np.ones((k,V.shape[1]))*0.00001
    Nh=np.matmul(W.T,V)
    Dh=np.matmul(np.matmul(W.T,W),H)+epsH
    H=np.multiply(H, Nh/Dh)
    
    iterations=60
    threshold=0.00001
    for iter in range(iterations):
        
        
        Nh=np.matmul(W.T,V)
        Dh=np.matmul(np.matmul(W.T,W),H)+epsH
        H=np.multiply(H, Nh/Dh)
        
        if np.abs(np.sum(V-np.matmul(W,H)) )< threshold:
            break
        print(np.abs(np.sum(V-np.matmul(W,H))))
        
    
    
    
    
    
    return H

Vtest=np.reshape(x_test_scaled,(10000, 784))
H=reconstruct_from_nmf(Vtest.T,W,2)

print(H.shape)
plt.scatter(H.T[:,0], H.T[:,1], c=y_test,  cmap='prism', alpha=0.4)
plt.show()

V=np.reshape(x_train_scaled,(60000, 784))
W=NMF(V.T,10)

Vtrain=np.reshape(x_train_scaled,(60000, 784))
H=reconstruct_from_nmf(Vtrain.T,W,10)

print(H.shape)
ax = plt.axes(projection='3d')
ax.scatter3D(H.T[:,0], H.T[:,1], H.T[:,2], c=y_test,  cmap='prism', alpha=0.4)
plt.show()

recon=np.matmul(W,H)

print(recon.shape)

recon1=np.reshape(recon.T,(60000,28,28))

print(recon1.shape)

fig, ax = plt.subplots(3,5, figsize=(10,7), subplot_kw={'xticks':(), 'yticks': ()})
ax = ax.ravel()
for i in range(15):
    pixels = recon1[i].reshape(-1,28)
    ax[i].imshow(pixels, cmap='viridis')
    ax[i].set_title("Digit - " + str(y_train[i]))
plt.imshow(pixels, cmap='gray')
plt.show()

def PCA(V,M):
    mean=np.mean(V,axis=1)
    X=(V.swapaxes(0,1)-mean).swapaxes(0,1)
    S=np.array([np.matmul(np.expand_dims(X[:,i],axis=1),np.expand_dims(X[:,i],axis=0)) for i in range(X.shape[1])])
    Sm=np.mean(S,axis=0)
    eigen_value,eigen_vector=np.linalg.eig(Sm)
    order=np.argsort(eigen_value)
    decreasing=np.flip(order)
    new_dim=np.take(eigen_vector.T, decreasing)[0:M]
    red_dim=np.zeros((M,X.shape[1]))
    #for i in range(X.shape[1]):
    #   red_dim[:,i]=np.array([np.matmul(X[:,i],new_dim[j,:]) for j in range(M)])
    red_dim=np.matmul(new_dim,X)
    return red_dim

X=np.reshape(x_train_scaled,(60000, 784))
red_dim=PCA(X.T,2)

print(red_dim.shape)
plt.scatter(red_dim.T[:,0], red.T[:,1], c=y_test,  cmap='prism', alpha=0.4)
plt.show()