from pylab import *
import numpy as np
import random


def original(x):
	#Rastrigin's function
	return 10 + x**2 - 10 * np.cos(2 * np.pi * x)

## LAGRANGE ##

def numerator(x,k):
	p = 1.
	for i in range(len(X)):
		if i != k:
			p *= (x - X[i])
	return p

def denominator(x,k):
	p = 1.
	for i in range(len(X)):
		if i != k:
			p *= (X[k] - X[i])
	return p

def L(k, x):
	return numerator(x,k) / denominator(x,k)

def pol(x):
	sum = 0.
	for i in range(len(X)):
		sum += Y[i] * L(i,x)
	return sum

## NEWTON ##

def n(j,xc,x):
	n = 1
	for i in range(j):
		n *= (xc-x[i])
	return n

def a(j,l,x,y):
	if j == 0:
		return y[0]
	elif j-l == 1:
		return (y[j]-y[l])/(x[j]-x[l])
	else:
		return (a(j,l+1,x,y)-a(j-1,l,x,y))/(x[j]-x[l])

def N(xc,x,y):
	N=0
	for j in range(len(x)):
		N += a(j,0,x,y)*n(j,xc,x)
	return N

## NEWTON-GREGORY ##

def checkSpace(x):
	if len(x) < 2:
		return False
	h = x[1] - x[0]
	for i in range(2, len(x)):
	   if h != x[i] - x[i-1]:
		   return False
	return True

def delta(r,x):
	if r == 0:
		index = X.index(round(x,2))
		return Y[index]
	else:
		return delta(r-1,x+h) - delta(r-1,x)

def production(x,n):
	sum = 1
	for i in range(n):
		sum *= x - X[i]
	return sum

def polNG(k,x):
	sum = delta(0, X[0])
	for n in range(k):
		sum += production(x,n+1) * delta(n+1,X[0]) / ( math.factorial(n+1) * math.pow(h,n+1) )
	return sum

## PLOT ##

X = [0.42,0.92,1.42,1.92,2.42]
Y = [18.9394688,2.0833332, 20.7794668, 4.9233332, 24.6194668]
h = X[1] - X[0]

t = linspace(-2,6,100)
o = original(t)

lagrange = pol(t)
newton = N(t,X,Y)
newtonGregory = polNG(4,t)

plt.suptitle("Comparação entre os métodos")
ax1 = subplot(231)
ax1.plot(t,o, label='original')
ax1.plot(t,lagrange, label='lagrange')
ax1.grid(True)
ax1.plot(X,Y,'ro')
ax1.set_ylim(0,50)
ax1.set_xlim(-2,6)
ax1.legend(loc='upper right')
ax2 = subplot(232)
ax2.plot(t,o, label='original')
ax2.plot(t,newton, label='newton')
ax2.grid(True)
ax2.plot(X,Y,'ro')
ax2.set_ylim(0,50)
ax2.set_xlim(-2,6)
ax2.legend(loc='upper right')
ax3 = subplot(233)
ax3.plot(t,o, label='original')
ax3.plot(t,newtonGregory, label='newton-gregory')
ax3.grid(True)
ax3.plot(X,Y,'ro')
ax3.set_ylim(0,50)
ax3.set_xlim(-2,6)
ax3.legend(loc='upper right')
ax4 = subplot(212)
ax4.plot(t,o, label='original')
ax4.plot(t,lagrange, label='lagrange')
ax4.plot(t,newton, label='newton')
ax4.plot(t,newtonGregory, label='newton-gregory')
ax4.grid(True)
ax4.plot(X,Y,'ro')
ax4.set_ylim(0,50)
ax4.set_xlim(-2,6)
ax4.legend(loc='upper right')
show()