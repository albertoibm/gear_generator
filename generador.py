from sys import argv,exit
from math import sin,cos,pi,sqrt,atan,atan2
from time import sleep
from random import random
try:
	from graf import *
	gui = True
except ImportError:
	gui = False
def radianes(grados):
	return grados*pi/180
class Gear:
	def __init__(self,N,D,Pd):
		self.N=N
		if Pd==0 and D!=0:
			self.D=float(D)
			self.m0=self.D/self.N
			self.Pd=25.4/self.m0
		elif D==0 and Pd!=0:
			self.Pd=Pd
			self.m0=25.4/self.Pd
			self.D=self.m0*self.N
		else:
			exit("No se tienen suficientes datos o hay datos de mas")
		self.R=self.D/2.
		if self.N<10:
			self.Ra=self.R+25.4*.6/self.Pd
		else:
			self.Ra=self.R+25.4*.8/self.Pd
		self.Da=self.Ra*2
		if self.N<10:
			self.Rb=self.R-25.4*.6/self.Pd
		else:
			self.Rb=self.R-25.4*1./self.Pd
		self.Db=self.Rb*2
		self.fase=pi/(self.N)\
			+2*(sqrt(self.R**2-self.Rb**2)/self.Rb\
			-atan(sqrt(self.R**2-self.Rb**2)/self.Rb))
		if details:
			print "%d dientes"%self.N
			print "%.2f diametro"%self.D
			print "%.3f paso diametral"%self.Pd
	def Involuta(self,n,th):
		if th<0:
			fase = self.fase
		else:
			fase=0
		l=self.Rb*radianes(th)
		th=radianes(n*360./self.N+th)+fase
		return self.Rb*cos(th)+l*sin(th),self.Rb*sin(th)-l*cos(th)
if len(argv)<5:
	print "Forma de uso:"
	print "%s <OPCIONES>"%argv[0]
	print "\n"
	print "-n N\tNumero de dientes"
	print "-d D\tDiametro del engrane"
	print "-p P\tPaso diametral"
	print "-s\tGuardar en una imagen"
	print "-a\tAnimar la generacion"
	print "-c\tIncluir los circulos de adendum,primitivo y base (default:y)"
	print "-t\tSolo texto. Sin interfaz grafica de usuario"
	print "-o\tImprime todos los puntos del engrane"
	print "-r\tImprime los detalles del engrane. Paso diametral, diametro, etc."
	print "\n"
	print "Se debe especificar al menos el numero de dientes y diametro o paso diametral"
	exit()
save = '-s' in argv
animar = '-a' in argv
gui = not '-t' in argv
points = '-o' in argv
details = '-r' in argv
circs = '-c' in argv
Op=['-n','-d','-p']
Vals=[0,0.0,0.0]
for i in range(len(Op)):
	if Op[i] in argv:
		try:
			Vals[i]=type(Vals[i])(argv[argv.index(Op[i])+1])
			if type(Vals[i])==type(str()) and '-' in Vals[i]:
				exit("Falta especificar valor para %s"%Op[i])
		except IndexError:
			exit("Falta especificar valor para %s"%Op[i])
		except ValueError:
			exit("Valor erroneo")
engrane=Gear(Vals[0],Vals[1],Vals[2])
Width=640
Height=480
X0=Width/2
Y0=Height/2
if gui:
	screen=Pantalla(Width,Height)
puntos=[]
for i in range(engrane.N):
#	print "Dibujando diente %d"%i
	for j in range(-90,90):
		if animar and gui:
			screen.fondo(BLANCO)
			screen.circulo([X0,Y0],engrane.R,width=1,color=ROJO)
			screen.circulo([X0,Y0],engrane.Ra,width=1,color=MORADO)
			screen.circulo([X0,Y0],engrane.Rb,width=1,color=VERDE)
		x,y=engrane.Involuta(i,j)
		if sqrt(x**2+y**2)<engrane.Ra:
			if points:
				print "%f,%f"%(x,y)
			if gui:
				th=radianes(360.*i/engrane.N+j)
				P1=[int(round(X0+engrane.Rb*cos(th))),int(round(Y0-engrane.Rb*sin(th)))]
				P2=[int(round(X0+x)),int(round(Y0-y))]
				puntos.append(P2)
			if animar and gui:
				screen.linea(P1,P2,color=VERDE)
				for k in puntos:
					if random()>.3:screen.punto(k[0],k[1])
				if random()>.7: ##ANIMAR
					screen.actualizar()
			if j > 0:
				ang2 = atan2(y,x)+radianes(.1)
		else:
			if j < 0:
				ang1 = atan2(y,x)-radianes(.1)
	####### CUBRE LA PUNTA DEL DIENTE (ADENDUM)
	th = ang2
	while th < ang1:
		x = engrane.Ra * cos(th)
		y = engrane.Ra * sin(th)
		if points:
			print "%f,%f"%(x,y)
		th += 0.001
		P2=[int(round(X0+x)),int(round(Y0-y))]
		puntos.append(P2)
	###### CUBRE LA BASE DEL DIENTE (DEDENDUM)
	th = engrane.fase
	incr = 2 * pi / engrane.N
	while th < incr:
		x = engrane.Rb * cos(incr * i + th)
		y = engrane.Rb * sin(incr * i + th)
		if points:
			print "%f,%f"%(x,y)
		th += 0.001
		P2=[int(round(X0+x)),int(round(Y0-y))]
		puntos.append(P2)
##Dibuja figura final en Negro
if gui:
	if not circs:
		screen.fondo()
	for k in puntos:
		screen.punto(k[0],k[1],color=NEGRO)
	##Dibuja una cruz indicando el centro
	screen.linea([X0-10,Y0],[X0+10,Y0])
	screen.linea([X0,Y0+10],[X0,Y0-10])
	##Escribe el numero de dientes y el paso diametral del engrane
	myfont = pygame.font.SysFont("monospace", 15)
	label = myfont.render("%d%.2f"%(engrane.N,engrane.Pd), 1, (0,0,0))
	screen.Screen.blit(label, (X0-22, Y0-engrane.Rb+\
		(10 if engrane.D>75 else - 30)))
	if save:
		name="Engrane-%d-%.3f.png"%(engrane.N,engrane.Pd)
		print "Guardando imagen en",name
		pygame.image.save(screen.Screen,name)
	while 1:
		screen.actualizar()
		screen.endloop()
		sleep(.1)
