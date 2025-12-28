import numpy as np
from matplotlib import pyplot as plt

# Tamanho del sistema que vamos a estudiar
lx=100
ly=100
numeroDeNodos=lx*ly

# numero de veces que repetimos la percolacion para hacer estadistica
nSamples=1000
# numero de probabilidades (-1) que simulamos
nProba=100

#Definimos los vecinos y su conexion
r=[]
rC=[]
l=[]
lC=[]
u=[]
uC=[]
d=[]
dC=[]
recorrido=[]

#Definimos la topologia del sistema
for i in range(numeroDeNodos):
    r.append(i+1)
    rC.append(0)
    l.append(i-1)
    lC.append(0)
    u.append(i+lx)
    uC.append(0)
    d.append(i-lx)
    dC.append(0)
    recorrido.append(0)

# Hay que retocar los bordes del sistema.
# -1 significa que no hay conexion
for i in range(ly):
    r[(i+1)*lx-1]=-1
    l[(i*lx)]=-1
for i in range(lx):    
    d[i]=-1
    u[i+lx*(ly-1)]=-1

# Funciones necesarias para correr el algoritmo

def limpiaConexiones():
    # Limpia las conexiones para volver a generar una configuracion
    global rC,lC,uC,dC,recorrido
    for i in range(numeroDeNodos):
        rC[i]=0
        lC[i]=0
        uC[i]=0
        dC[i]=0
        recorrido[i]=0

listaVecinosACheckear=[]

def anadeVecinosLista(celdaARevisar):
    global listaVecinosACheckear
    # Miramos todos los vecinos accesibles de la celda a revisar y chekeamos
    # si hay conexiones accesibles no recorridas ya
    # Miramos el vecino de la derecha
    if ((r[celdaARevisar]!=-1) and (rC[celdaARevisar]==1) and (recorrido[r[celdaARevisar]]==0)):
        # Si la conexion existe topologicamente y
        # existe conexion debido a la percolacion y
        # no la hemos recorrido ya
        listaVecinosACheckear.append(r[celdaARevisar])
        # La anadimos a la lista de vecinos que deben ser checkeados
    # Hacemos lo mismo para los otros 3 vecinos
    if ((l[celdaARevisar]!=-1) and (lC[celdaARevisar]==1) and (recorrido[l[celdaARevisar]]==0)):
        listaVecinosACheckear.append(l[celdaARevisar])
    if ((u[celdaARevisar]!=-1) and (uC[celdaARevisar]==1) and (recorrido[u[celdaARevisar]]==0)):
        listaVecinosACheckear.append(u[celdaARevisar])
    if ((d[celdaARevisar]!=-1) and (dC[celdaARevisar]==1) and (recorrido[d[celdaARevisar]]==0)):
        listaVecinosACheckear.append(d[celdaARevisar])
    # Por ultimo marcamos como recorrida a la celda revisada
    recorrido[celdaARevisar]=1


# Codigo de ejemplo de una run del problema

'''
# Ahora vamos a hacer un ejemplo de conexion aleatoria

probabilidad=0.5

for i in range(numeroDeNodos):
    random=np.random.uniform()
    if(random<probabilidad):
        rC[i]=1
    random=np.random.uniform()
    if(random<probabilidad):
        lC[i]=1
    random=np.random.uniform()
    if(random<probabilidad):
        dC[i]=1
    random=np.random.uniform()
    if(random<probabilidad):
        uC[i]=1

# Ahora vamos a forzar que todos los elementos de la primera fila esten
# conectados a la fuerza (esto es considerado una condicion de contorno)
for i in range(tamanho):
    rC[i]=1

# Ahora vamos a ver si el sistema percola, i.e. si hay conexion entre 
# la fila 1 y la fila ultima
celdaInicial=0
listaVecinosACheckear=[]

def anadeVecinosLista(celdaARevisar):
    global listaVecinosACheckear
    # Miramos todos los vecinos accesibles de la celda a revisar
    # Miramos el vecino de la derecha
    if ((r[celdaARevisar]!=-1) and (rC[celdaARevisar]==1) and (recorrido[r[celdaARevisar]]==0)):
        # Si la conexion existe topologicamente y
        # existe conexion debido a la percolacion y
        # no la hemos recorrido ya
        listaVecinosACheckear.append(r[celdaARevisar])
        # La anadimos a la lista de vecinos que deben ser checkeados
    # Hacemos lo mismo para los otros 3 vecinos
    if ((l[celdaARevisar]!=-1) and (lC[celdaARevisar]==1) and (recorrido[l[celdaARevisar]]==0)):
        listaVecinosACheckear.append(l[celdaARevisar])
    if ((u[celdaARevisar]!=-1) and (uC[celdaARevisar]==1) and (recorrido[u[celdaARevisar]]==0)):
        listaVecinosACheckear.append(u[celdaARevisar])
    if ((d[celdaARevisar]!=-1) and (dC[celdaARevisar]==1) and (recorrido[d[celdaARevisar]]==0)):
        listaVecinosACheckear.append(d[celdaARevisar])
    # Por ultimo marcamos como recorrida a la celda revisada
    recorrido[celdaARevisar]=1

anadeVecinosLista(celdaInicial)

while(len(listaVecinosACheckear)>0):
    # Mientras queden vecinos que chekear
    celdaAnalizar=listaVecinosACheckear[0]
    # Elegimos un elemento de la lista
    anadeVecinosLista(celdaAnalizar)
    listaVecinosACheckear.remove(celdaAnalizar)

# Aqui ya ha terminado el bucle. Para comprobar si hay percolacion hay que ver la fila superior

for i in range(tamanho):
    if (recorrido[i+tamanho*(tamanho-1)]==1):
        print("Hay percolacion")
        break
'''

# Ahora vamos a replicar esto nSamples para hacer estadistica. Luego lo
# replicaremos para distintas p y veremos si presenta una transicion de fase


listaProbabilidades=[]
listaPercolaciones=[]

for k in range(nProba+1):
    probabilidad=k/nProba
    vecesPercola=0
    listaProbabilidades.append(probabilidad)
    for j in range(nSamples):
        # Para cada sample generamos una nueva conexion aleatoria
        limpiaConexiones()
        # Primero limpiamos y luego combinamos
        print (k+1," out of ",(nProba+1)," prob(",probabilidad,").  ",j+1," out of ",(nSamples)," samples        \r", end="")
        for i in range(numeroDeNodos):
            random=np.random.uniform()
            if(random<probabilidad):
                rC[i]=1
            random=np.random.uniform()
            if(random<probabilidad):
                lC[i]=1
            random=np.random.uniform()
            if(random<probabilidad):
                dC[i]=1
            random=np.random.uniform()
            if(random<probabilidad):
                uC[i]=1
        # Ahora vamos a forzar que todos los elementos de la primera fila esten
        # conectados a la fuerza (esto es considerado una condicion de contorno)
        for i in range(lx):
            rC[i]=1
        # Aqui ya estan las conexiones establecidas. Ahora vamos a ver si 
        # el sistema percola o no
        celdaInicial=0
        listaVecinosACheckear=[]
        anadeVecinosLista(celdaInicial)
        find = False
        while(len(listaVecinosACheckear)>0):
            # Mientras queden vecinos que chekear
            celdaAnalizar=max(listaVecinosACheckear)
            # Elegimos un elemento de la lista
            # El max siempre sera el que este más arriba y mas a la derecha
            anadeVecinosLista(celdaAnalizar)
            listaVecinosACheckear.remove(celdaAnalizar)
            # Comprobamos si hay percolacion
            for i in range(lx):
                if (recorrido[i+lx*(ly-1)]==1):
                    vecesPercola+=1
                    find = True 
                    break
            if find:
                break
        # Si sale por aqui no 
        '''
        for i in range(lx):
            if (recorrido[i+lx*(ly-1)]==1):
                vecesPercola+=1
                # print("PERCOLA")
                break
        '''
    # Aqui ya han terminado las nSamples
    listaPercolaciones.append(vecesPercola/nSamples)
# Aqui ya ha terminado el bucle. En resultadoPercolacion estan los datos a pintar

plt.plot(listaProbabilidades,listaPercolaciones)
plt.xlabel(r'$p$', fontsize=14)
plt.ylabel(r'$P_\infty$', fontsize=14)
plt.xticks(np.arange(0, 1.1, 0.1), fontsize=12)
plt.yticks(fontsize=12)
plt.savefig('percolacion.png', dpi=300, bbox_inches='tight')
plt.savefig('percolacion.pdf', bbox_inches='tight')
