# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 12:46:20 2022

@author: David Ernesto Ramirez Arboleda
"""
import numpy as np
import random
from scipy.stats import norm  # Importa  distribución normal
    
    
class Cirugia():    
    def __init__(self,duracion,vencimiento): 
        self.duracion=duracion 
        self.vencimiento=vencimiento #prioridad
    def quirofano(self,a):
        self.quirofano=a 

class AsignacionesIniciales():
    def __init__(self):
        self.CrearCirugias() 
        self.Bubblesort()
        self.AsignacionInicial()
        
    def CrearCirugias(self):
        self.quirofanos=[[],[],[],[],[],[]]
        self.ListaCirugias=[]
        #Seis quirofanos,5 dias, cirugias entre 1 y 5 horas
        TotalCirugias=int((24*5*6)/3) #24 horas, seis pabellones 5 dias 
        for x in range(TotalCirugias):
            self.ListaCirugias.append(Cirugia(random.randint(1,5),random.randint(5,54*5)))


    def Bubblesort(self): #ordenamos la prioridad de las cirugias
        contador=1
        while contador!=0:
            contador=0
            for x in range(len(self.ListaCirugias)-1):
                if self.ListaCirugias[x].vencimiento>self.ListaCirugias[x+1].vencimiento:
                    a=self.ListaCirugias[x]
                    b=self.ListaCirugias[x+1]
                    self.ListaCirugias[x]=b
                    self.ListaCirugias[x+1]=a
                    contador+=1
                    
    def printVencimientos(self):  #Ver prioridades de cirugias
        for x in self.ListaCirugias:
            print(x.vencimiento,end="  ")
            
    def printDuraciones(self): #ver tiempos cirugias
         for x in self.ListaCirugias:
            print(x.duracion,end="  ")
    def printQuirofanos(self,n):
        for x in self.quirofanos[n]:
            print(x.duracion,x.vencimiento, end=",  ")
    def AsignacionInicial(self): #Asignamos los quirofanos por prioridad
        turno=0
        while turno<len(self.ListaCirugias):
            for y in self.quirofanos:
                y.append(self.ListaCirugias[turno])
                turno+=1
    def SumaTiemposCirugias(self,n):
        suma=0
        for x in self.quirofanos[n]:
            suma+=x.duracion
        return suma

class Simulacion():
    def __init__(self,AsignacionesQuirofanos,ListaCirugias):
        self.AsignacionesQuirofanos=AsignacionesQuirofanos
        self.ListaCirugias=ListaCirugias
        self.simular()
        
    def simular(self):
        retrazos=[]
        for x in self.AsignacionesQuirofanos:
            RetrazoTotal=0
            for y in x: #Solo los retrazos se suman, las cirugias + rapidas d elo programado reducen tiempo de retrazo ó dejan la sala vacia.
                mu, sigma=y.duracion, y.duracion*0.2
                retrazo=np.random.normal(mu, sigma, 1)[0]
                if RetrazoTotal>0:
                    RetrazoTotal+=retrazo
                else:
                    if retrazo>0:
                        RetrazoTotal+=retrazo
            retrazos.append(RetrazoTotal)
        self.retrazos=retrazos
        #print(retrazos,"####")
        #print("promedio=",sum(retrazos)/len(retrazos))
        self.promedio=sum(retrazos)/len(retrazos)
    def darwin(self):
        n=200#Numero de simulaciones
        retrazos=[]
        for x in range(n):
            retrazos.append(self.retrazos)
            self.simular()
        #averiguamos que asignaciones a salas tienen mejores y peores desempeños
        promedios=np.array([0.0,0.0,0.0,0.0,0.0,0.0])
        for x in retrazos:
            for y in range(6): #6 salas                
                promedios[y]+=x[y]                
        promedios=promedios/n        
        #print(retrazos)
        #print(promedios)
        self.promedios0=promedios
    def mutar(self,promedios):
        k=promedios.copy()
        k.sort()
        for x in range(3,6):
            for y in range(6):
                if promedios[y]==k[x]:
                    s=random.randint(0,len(self.AsignacionesQuirofanos[y])-1)
                    cromosoma=self.AsignacionesQuirofanos[y].pop(s)
                    insertar=random.randint(0,5)
                    self.AsignacionesQuirofanos[insertar].append(cromosoma)
    
    def mesclar0(self):
        self.hijos=[]
        for x in range(6):
            for y in range(x,6):
                if x!=y:
                    self.mesclar1(self.AsignacionesQuirofanos[x],self.AsignacionesQuirofanos[y])
                    self.hijos.append(self.hijo2)
                    self.hijos.append(self.hijo1)
               
    def mesclar1(self,a,b):
        random.shuffle(a)
        random.shuffle(b)
        self.hijo1=a[:int(len(a)/2)]+b[int(len(b)/2):]
        self.hijo2=a[int(len(a)/2):]+b[:int(len(b)/2)]
        
    def depredacion(self):
        sobrevivientes=[]
        self.AsignacionesQuirofanos=self.hijos
        self.simular()
        k=self.retrazos.copy()
        k.sort()
        for x in range(len(self.retrazos)):
            for y in range(6):
                if self.retrazos[x]==k[y]:
                    sobrevivientes.append(self.AsignacionesQuirofanos[x])
        self.AsignacionesQuirofanos=sobrevivientes
        
print("SE REALIZAN 200 SIMULACIONES SOBRE CADA GENERACION PARA ESTIMAR EL TIEMPO PROMEDIO,")
r=AsignacionesIniciales() #Creamos cirugias, asignamos a quirofanos
t=Simulacion(r.quirofanos,r.ListaCirugias) #simulamos con asignacines iniciales
print("PROMEDIO RETRAZO TOTAL PRIMERA GENERACION=",t.promedio)
for x in range(4000): # Cada iteracion es una nueva generacion y una simulacion sobre como se desempeñaria.
    t.darwin()
    t.mutar(t.promedios0)
    t.mesclar0()
    t.depredacion()
    print("GENERANCION=",x,"     ",t.promedio)
    print(t.promedio)


"""

###SIMULACION DE ASIGNACIONES INICIALES
prom=[]
for x in range(10**3):

    r=AsignacionesIniciales() #Creamos cirugias, asignamos a quirofanos
    t=Simulacion(r.quirofanos,r.ListaCirugias) #simulamos con asignaciones iniciales
    prom.append((t.promedio))
print("RESULTADO: El promedio de demora con las asignaciones iniciales es")
print(sum(prom)/len(prom))

"""


