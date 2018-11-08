from pylab import *
import matplotlib
from matplotlib.figure import Figure
import numpy as np
from tkinter import *
import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import matplotlib.pyplot as plt
import scipy as sc

class Application:

	pontos = [[0.42,18.9394688],[0.92,2.0833332],[1.42,20.7794668],[1.92,4.9233332],[2.42,24.6194668]]

	def __init__(self, main):
		self.fontePadrao = ("Arial", "10")

		self.primeiroContainer = Frame(main)
		self.primeiroContainer["pady"] = 10
		self.primeiroContainer.pack()

		self.segundoContainer = Frame(main)
		self.segundoContainer["padx"] = 20
		self.segundoContainer.pack()

		self.terceiroContainer = Frame(main)
		self.terceiroContainer["padx"] = 20
		self.terceiroContainer.pack()

		self.quartoContainer = Frame(main)
		self.quartoContainer["pady"] = 20
		self.quartoContainer.pack()

		self.quintoContainer = Frame(main)
		self.quintoContainer["padx"] = 20
		self.quintoContainer.pack()

		self.sextoContainer = Frame(main)
		self.sextoContainer["pady"] = 20
		self.sextoContainer.pack()

		self.adicionarPontosTitulo = Label(self.primeiroContainer, text="Adicionar Pontos")
		self.adicionarPontosTitulo["font"] = ("Arial", "10", "bold")
		self.adicionarPontosTitulo.pack()

		self.XLabel = Label(self.segundoContainer, text="X", font=self.fontePadrao)
		self.XLabel.pack(side=LEFT)

		self.X = Entry(self.segundoContainer)
		self.X["width"] = 10
		self.X["font"] = self.fontePadrao
		self.X.pack(side=LEFT)

		self.YLabel = Label(self.segundoContainer, text="Y", font=self.fontePadrao)
		self.YLabel.pack(side=LEFT)

		self.Y = Entry(self.segundoContainer)
		self.Y["width"] = 10
		self.Y["font"] = self.fontePadrao
		self.Y.pack(side=LEFT)

		self.adicionar = Button(self.terceiroContainer)
		self.adicionar["text"] = "Adicionar"
		self.adicionar["font"] = ("Calibri", "8")
		self.adicionar["width"] = 12
		self.adicionar["command"] = self.adicionarPontos
		self.adicionar.pack(side=BOTTOM)

		self.pontosTitulo = Label(self.quartoContainer, text="Pontos")
		self.pontosTitulo["font"] = ("Arial", "10", "bold")
		self.pontosTitulo.pack()

		self.pointsLabel = Label(self.quartoContainer, text=self.verificarPontos(), font=self.fontePadrao)
		self.pointsLabel.pack()

		self.limpar = Button(self.quartoContainer)
		self.limpar["text"] = "Limpar"
		self.limpar["font"] = ("Calibri", "8")
		self.limpar["width"] = 12
		self.limpar["command"] = self.limparPontos
		self.limpar.pack(side=BOTTOM)

		#

		self.adicionarPontosTitulo = Label(self.quintoContainer, text="Algoritmos")
		self.adicionarPontosTitulo["font"] = ("Arial", "10", "bold")
		self.adicionarPontosTitulo.pack()

		self.lagrange = Button(self.quintoContainer)
		self.lagrange["text"] = "Lagrange"
		self.lagrange["font"] = ("Calibri", "8")
		self.lagrange["width"] = 12
		self.lagrange["command"] = self.lagrangeAlg
		self.lagrange.pack(side=LEFT)

		self.newton = Button(self.quintoContainer)
		self.newton["text"] = "Newton"
		self.newton["font"] = ("Calibri", "8")
		self.newton["width"] = 12
		self.newton["command"] = self.newtonAlg
		self.newton.pack(side=LEFT)

		self.NG = Button(self.quintoContainer)
		self.NG["text"] = "Newton Gregory"
		self.NG["font"] = ("Calibri", "8")
		self.NG["width"] = 12
		self.NG["command"] = self.newtonGregoryAlg
		self.NG.pack(side=LEFT)

		#
		self.canvasFig=plt.figure(1)
		Fig = Figure(figsize=(4,3),dpi=100)
		FigSubPlot = Fig.add_subplot(111)
		x=[]
		y=[]
		self.line1, = FigSubPlot.plot(x,y,label='original')
		self.line2, = FigSubPlot.plot(x,y)
		self.canvas = matplotlib.backends.backend_tkagg.FigureCanvasTkAgg(Fig, master=self.sextoContainer)
		self.canvas.show()
		self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
		self.canvas._tkcanvas.pack(side=TOP, fill=BOTH, expand=1)

	def lagrangeAlg(self):

		arr = np.array(self.pontos)
		X = arr[:,0].tolist()
		Y = arr[:,1].tolist()

		t = linspace(-2,6,100)
		o = self.original(t)

		lagrange = self.pol(t,X,Y)

		# ax1 = subplot(231)
		# ax1.plot(t,o, label='original')
		# ax1.plot(t,lagrange, label='lagrange')
		# ax1.grid(True)
		# ax1.plot(X,Y,'ro')

		# x=[]
		# y=[]
		# for num in range(0,1000):x.append(num*.001+1)
		# # just some random function is given here, the real data is a UV-Vis spectrum
		# for num2 in range(0,1000):y.append(sc.math.sin(num2*.06)+sc.math.e**(num2*.001))
		# x = np.array(x)
		# y = np.array(y)
		
		self.line1.set_data(t,o)
		self.line2.set_data(t,lagrange)
		ax = self.canvas.figure.axes[0]
		ax.set_xlim(t.min(), t.max())
		ax.set_ylim(o.min(), o.max())        
		self.canvas.draw()

	def numerator(self,x,k,X):
		p = 1.
		for i in range(len(X)):
			if i != k:
				p *= (x - X[i])
		return p

	def denominator(self,x,k,X):
		p = 1.
		for i in range(len(X)):
			if i != k:
				p *= (X[k] - X[i])
		return p

	def L(self,k, x,X):
		return self.numerator(x,k,X) / self.denominator(x,k,X)

	def pol(self,x,X,Y):
		sum = 0.
		for i in range(len(X)):
			sum += Y[i] * self.L(i,x,X)
		return sum

	###

	def newtonAlg(self):

		arr = np.array(self.pontos)
		X = arr[:,0].tolist()
		Y = arr[:,1].tolist()

		t = linspace(-2,6,100)
		o = self.original(t)

		newton = self.N(t,X,Y)

	def n(self,j,xc,x):
		n = 1
		for i in range(j):
			n *= (xc-x[i])
		return n

	def a(self,j,l,x,y):
		if j == 0:
			return y[0]
		elif j-l == 1:
			return (y[j]-y[l])/(x[j]-x[l])
		else:
			return (self.a(j,l+1,x,y)-self.a(j-1,l,x,y))/(x[j]-x[l])

	def N(self,xc,x,y):
		N=0
		for j in range(len(x)):
			N += self.a(j,0,x,y)*self.n(j,xc,x)
		return N

	###

	def newtonGregoryAlg(self):

		arr = np.array(self.pontos)
		X = arr[:,0].tolist()
		Y = arr[:,1].tolist()
		h = X[1] - X[0]

		t = linspace(-2,6,100)
		o = self.original(t)

		newtonGregory = self.polNG(4,t,X,Y,h)

	def delta(self,r,x,X,Y,h):
		if r == 0:
			index = X.index(round(x,2))
			return Y[index]
		else:
			return self.delta(r-1,x+h,X,Y,h) - self.delta(r-1,x,X,Y,h)

	def production(self,x,n,X):
		sum = 1
		for i in range(n):
			sum *= x - X[i]
		return sum

	def polNG(self,k,x,X,Y,h):
		sum = self.delta(0, X[0],X,Y,h)
		for n in range(k):
			sum += self.production(x,n+1,X) * self.delta(n+1,X[0],X,Y,h) / ( math.factorial(n+1) * math.pow(h,n+1) )
		return sum

	###

	def adicionarPontos(self):

		x = self.X.get()
		y = self.Y.get()

		if x == "":
			x = "0."
		if y == "":
			y = "0."

		self.pontos.append([float(x), float(y)])

		self.pointsLabel["text"] = self.verificarPontos()

		self.X.delete(0, END)
		self.Y.delete(0, END)

	def limparPontos(self):
		self.pontos = []
		self.pointsLabel["text"] = self.verificarPontos()		

	def verificarPontos(self):

		st = ""

		if self.pontos != []:
			for pair in self.pontos:
				st += "(" + str(pair[0]) + ", " + str(pair[1]) + ") "

			return st.strip()
		else:
			return "Nenhum ponto adicionado"

	def original(self, x):
		#Rastrigin's function
		return 10 + x**2 - 10 * np.cos(2 * np.pi * x)

def ask_quit():
	plt.close()
	root.destroy()

root = Tk()
root.geometry("500x500")
root.resizable(0, 0)
Application(root)
root.protocol("WM_DELETE_WINDOW", ask_quit)
root.mainloop()