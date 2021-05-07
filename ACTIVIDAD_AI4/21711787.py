#region libs
import multiprocessing as mp
import concurrent.futures
import json
import os
import platform
import sys
import time
import math
import random
#endregion
#region constants
EXPEDIENTE = 21711787
workers = int(os.cpu_count() - 2)
#endregion
#region support_methods
"""
Clase de apoyo para limpiar la consola (dependiendo del sistema operativo),
usado para limpiar la consola y mantener una interfaz de usuario limpia.
"""
class ConsoleClear():
    def __init__(self):
        if platform.system() == 'Windows':
            def clear(): return os.system('cls')
            clear()
        elif platform.system() == 'Linux' or 'Darwin':
            def clear(): return os.system('clear')
            clear()
#endregion            
# region LOGIN


class User():
    def __init__(self, user, password, data):
        self.user = user
        self.password = password
        data.AddUser(self)

    def toDict(self):
        return {'user': self.user, 'password': self.password}

class DataController():
    def __init__(self):
        self.usersList = []
        self.GetUsers()
        self.ManageUsersPanel()

    def GetUsers(self):
        with open('users.json', 'r') as r: #E:/CARRERA/4ºCARRERA/2º CUATRI/Programacion concurrente/ACTIVIDAD_AI4/
            self.usersList = (json.loads(r.read()))

    def AddUser(self, userObject):
        self.usersList.append(userObject.toDict())
        self.SaveUsers()

    def SaveUsers(self):
        print(self.usersList)
        print(type(self.usersList))
        with open('users.json', 'w') as f: #E:/CARRERA/4ºCARRERA/2º CUATRI/Programacion concurrente/ACTIVIDAD_AI4/
            json.dump(self.usersList, f)

    def Register(self):
        User(input("Username:"), input("Password: "), self)
        self.ManageUsersPanel()

    def Login(self):
        user = input("username: ")
        password = input("password: ")

        for dbUser in self.usersList:
            if dbUser['user'] == user and dbUser['password'] == password:
                print("Welcome back,", user)
                time.sleep(.75)
                ExercicesMenu()
                return

        print("Wrong password or username!")
        input("...")
        self.ManageUsersPanel()

    def ManageUsersPanel(self):
        ConsoleClear()
        print(" ********************", "\n",
              "* INICIO DE SESIÓN *", "\n"
              " ********************", "\n",
              " - R para registrarse", "\n",
              " - L para iniciar sesión", "\n",
              " - X para salir", "\n",
              )
        response = input()
        if response == 'R':
            self.Register()
        elif response == 'L':
            self.Login()

        elif response == 'X':
            sys.exit()
        else:
            self.ManageUsersPanel()

# endregion
# region EXERCICES


"""
Función encargada de la selección de ejercicios.
Dependiendo del input, se llamará a uno u otro 
ejercicio.
"""
def ExercicesMenu():
    
    ConsoleClear()
    print(" **************************", "\n",
          "* SELECCIONE LA ACTIVIDAD *", "\n"
          " **************************", "\n",
          " - A: Ejercicio A ", "\n",
          " - B: Ejercicio B ", "\n",
          " - C: Ejercicio C ", "\n",
          " - L: Login menu ", "\n",
        #   " - Q para configuración", "\n",
          " - X: Exit ", "\n",
          )
    response = input()
    if response == 'A':
        ExerciceA()
    elif response == 'B':
        ExerciceB()
    elif response == 'C':
        ExerciceC()
    elif response == 'L':
        data = DataController()
        data.ManageUsersPanel()
    elif response == 'X':
        sys.exit()
    else:
        ExercicesMenu()
    
    """
    elif response == 'Q':
        print(" ****************", "\n",
              "* CONFIGURACION *", "\n"
              " ****************", "\n",
          " - EXP: Cambiar el nº de EXPEDIENTE ", "\n",
          " - COR: Cambiar el nº de cores usados ", "\n",
          " - R: Volver atrás ", "\n",
          )
        response2 = input()
        if response2 == 'EXP':
            EXPEDIENTE = input("EXPEDIENTE: ")
            ExercicesMenu()
        elif response2 == 'COR':
            print(f"CUIDADO! RECUERDE QUE SU MÁQUINA TIENE UN MÁXIMO DE {os.cpu_count()} CORES LÓGICOS")
            workers = int(input("Cores:"))
            while workers > os.cpu_count():
                print(f"CUIDADO! RECUERDE QUE SU MÁQUINA TIENE UN MÁXIMO DE {os.cpu_count()} CORES LÓGICOS")
                workers = input("Cores:")
            ExercicesMenu()
        elif response2 == 'R':
            ExercicesMenu()
        else:
            ExercicesMenu()
    """


#region ej_A
def ExerciceA():

    # cuando pasamos al EXPEDIENTE de n7 (2171178) es necesario externalizar los calculos a la nube.
    # el error es el siguiente: OSError: [WinError 1455] El archivo de paginación es demasiado pequeño para completar la operación
    
    # Genero A[21711787][6]con num. aleatorios del 0 al 215
    m1 = [[random.randint(0, 215) for i in range(6)] for j in range(int(str(EXPEDIENTE)[0:6]))] #21711787
    
    # Genero B[6][21711787]con num. aleatorios del 0 al 215
    m2 = [[random.randint(0, 215) for i in range(200)] for j in range(6)]
    m1f = len(m1)  # Obtengo num de filas de A
    m1c = len(m1[0])  # Obtengo num de colunmas de A
    m2f = len(m2)  # Obtengo num de filas de B
    m2c = len(m2[0])  # Obtengo num de filas de B
    if m1c != m2f:
        # Compruebo que se puedan multiplicar A y B
        raise Exception('Dimensiones no validas')

    startMultiply = time.time()
    mulmat = MultiplyMat(m1, m2, m2c, m1f) 
    endMultiply = time.time()
    print(f'Finished multiply matrix in {round(endMultiply-startMultiply,2)} second(s)...')
    response = input("print result (y/n)")
    if response == 'y':
        print(mulmat)
        input('. . . ')
        ExercicesMenu()
    else:
        ExercicesMenu()
    
# f() que prepara el reparto de trabajo para la mult. en paralelo
def MultiplyMat(m1, m2, m2c, m1f):
    
    n_cores = int(os.cpu_count()/2)  # Obtengo los cores de mi pc
    # Columnas  a procesar x c/cpre
    size_col = math.ceil(m2c/n_cores)
    # Filas a procesar x c/cpre
    size_fil = math.ceil(m1f/n_cores)
    # Array de memoria compartida donde se almacenaran los resultados
    sharedArr = mp.RawArray('i', m1f * m2c)
    cores = []  
    # Asigno a cada core el trabajo que le toca
    for core in range(n_cores):
        # Calculo i para marcar inicio del trabajo del core en relacion a las filas
        i_sharedArr = min(core * size_fil, m1f)
        # Calculo f para marcar fin del trabajo del core
        f_sharedArr = min((core + 1) * size_fil, m1f)
        # Añado al Array los cores y su trabajo
        cores.append(mp.Process(target=par_core, args=(m1, m2, sharedArr, i_sharedArr, f_sharedArr)))
    for core in cores:
        print(f"{core.name} started...")
        core.start()  # Arranco y ejecuto el trabajo para c/ uno de los cores que tenga mi equipo
    for core in cores:
        print(f"{core.name} ended...")
        core.join()  # Bloqueo cualquier llamada hasta que terminen su trabajo todos los cores
    # Convierto el array unidimensional compartido en una matrix 2D 
    finalMatrix = [[0] * m2c for i in range(m1f)]
    for i in range(m1f):  # i para iterar sobre las filas de m1
        for j in range(m2c):  # j para iterar sobre las columnas de m2
            # Guardo en finalMatrix los datos del array compartido
            finalMatrix[i][j] = sharedArr[i*m2c + j]
    return finalMatrix

def par_core(m1, m2, sharedArr, i_sharedArr, f_sharedArr):  # La tarea que hacen todos los cores
    # Size representado en colores en el excel que itera sobre las filas en m1
    startCore = time.time()
    for i in range(i_sharedArr, f_sharedArr):
        # Size representado en colores en el excel que itera sobre las columnas en m2
        for j in range(len(m2[0])):
            for k in range(len(m1[0])):  # m2f o lo que es l0 mismo el m1c
                # Guarda resultado  de cada core
                sharedArr[i*len(m2[0]) + j] += m1[i][k] * m2[k][j]
    endCore = time.time()
    print(f"{os.getpid()} finished in {round(endCore-startCore,2)} second(s)")
    
#endregion
#region ej_B

def ExerciceB():
    startArray = []

    startFillup = time.perf_counter()
    print(f"Started to fillup array with {EXPEDIENTE} elements and {workers} processors ")
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor: #pool de procesos de int(os.cpu_count() - 2) trabajadores que crean el array 
        results = [executor.submit(AddToArray, workers)
                   for _ in range(workers)]
    for f in concurrent.futures.as_completed(results): #una vez han finalizado todos los procesos, se unen sus resultados para formar el array completo
        startArray = startArray + (f.result())

    finishFillup = time.perf_counter()
    print(f'Finished fillup in {round(finishFillup-startFillup,2)} second(s)')
    for _ in range(len(startArray) - EXPEDIENTE):
        startArray.pop()

    startMergeSort = time.perf_counter()
    print(f"Started MergeSort array with {EXPEDIENTE} elements and {workers} processors ")
    mergesort = MergeSort(startArray.copy())
    endMergeSort = time.perf_counter()
    print(f'Finished MergeSort in {round(endMergeSort-startMergeSort,2)} second(s)')
    response = input("print result (y/n)")
    if response == 'y':
        print(mergesort)
        input('. . . ')
        ExercicesMenu()
    else:
        ExercicesMenu()
    
def MergeSort(array, *args):
    # crea el array compartido si es la primera llamada a MergeSort
    if not args:
        shared_array = mp.RawArray('i', array) 
        MergeSort(shared_array,0,len(array)-1,0) 
        array[:] = shared_array #array compartido
        return array
    else: #si no, usando depth como contador de cores, se irán dividiendo las tareas entre los cores disponibles 
        left,right,depth = args
        if(depth >= math.log(mp.cpu_count(),2)): #en caso de que nos quedemos sin cores, se realizará el mergesort habitual
            boringMergeSort(array,left,right)
        elif(left<right):#sino, asignar una mitad a un nuevo core y continuar con el bucle
            mid = (left + right) // 2 
            processJob = mp.Process(target=MergeSort,args=(array,left,mid,depth+1)) 
            processJob.start() 
            MergeSort(array,mid+1,right,depth+1) 
            processJob.join() 
            merge(array,left,mid,right)
            
# El algoritmo clásico de mergesort, aplicando divide y vencerás
def boringMergeSort(array, left, right): 
    if (left < right): 
        mid = (left+right)//2 
        boringMergeSort(array,left,mid)
        boringMergeSort(array, mid+1,right) 
        merge(array,left,mid,right) 
        
#Parte de la ordenación del mergesort clásico
def merge(array,left,mid,right): 
    
    arrA = array[left:mid+1].copy()
    arrB = array[mid+1:right+1].copy()
    a = 0 
    b = 0 
    index = left 

    while (a < (mid - left + 1) or b < (right- mid)): 
        if(a < (mid - left + 1) and b < (right - mid)): #Ordenamiento
            if(arrA[a] <= arrB[b]): #se ordena la izquierda
                array[index] = arrA[a]
                a += 1 
            else: #se ordena la derecha
                array[index] = arrB[b]
                b += 1
        elif(a<(mid-left+1)): #se ordena la izquierda
            array[index] = arrA[a]
            a += 1 
        elif(b < (right - mid)):
            array[index] = arrB[b]
            b += 1 #se ordena la derecha
        index += 1
        
"""
Función que añade a un array de tamaño EXPEDIENTE/nº cores elementos aleatorios de 0 a EXPEDIENTE. 
Usada concurrentemente para paralelizar el proceso de creación del array, uniendo al final el resultado 
de cada core en un array único (que posteriormente se convertirá en un array compartido).
"""
def AddToArray(workers):
    arrayPart = []
    for _ in range(math.ceil(EXPEDIENTE/workers)):
        arrayPart.append(random.randint(0, EXPEDIENTE))
    return arrayPart

#endregion
#region ej_C

"""
Para calcular la secuencia de fibonacci, se ha utilizado el método de O(log n), basado en la multiplicación matricial.
No se podría haber paralelizado el cálculo de fibo de otra manera dado que no se pueden 'particionar' los cálculos en 
el método lineal o el recursivo. 
Así pues, se paralelizan los cálculos de las multiplicaciones matriciales, y no los del conteo. Se ha podido reducir al
caso base de cálculos hasta 8 divisiones, lo que se traduce en el uso máximo de 8 cores (cabe destacar que se ha condicionado)
el código para casos de cores >= 8 y casos de cores <= 8 , dado que se podía divir los cálculos en 4 también.  
"""
def ExerciceC():
    startFib = time.perf_counter()
    print(f"Started fibonacci sequence with number {EXPEDIENTE} and {workers} processors ")  
    fib = matfib(EXPEDIENTE)
    endFib = time.perf_counter()
    print(f'Finished fibonacci in {round(endFib-startFib,2)} second(s)')
    
    input('. . . ')
    ExercicesMenu()

# multiplica matrices 
def matmut(x,y):
    if ( len(y) == 2 ): #si una de las dos matrices de entrada es de uno por uno se realiza este único cálculo (caso base) 
        a = x[0]*y[0]+x[1]*y[1]
        b = x[2]*y[0]+x[3]*y[1]
        return [a,b]
    #sino, se dividen los cálculos entre 4 u 8 procesos, dependiendo del número de cores de la máquina
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor: 
        if workers < 8: #si la máquina tiene < de 8 cores, se dividen los cálculos de las multiplicaciones matriciales entre 4
            a = {executor.submit(processMult,x,y,'a')}
            b = {executor.submit(processMult,x,y,'b')}
            c = {executor.submit(processMult,x,y,'c')}
            d = {executor.submit(processMult,x,y,'d')}
        elif workers >= 8:  #si la máquina tiene >= de 8 cores, se dividen los cálculos de las multiplicaciones matriciales entre 8
            a1 = {executor.submit(processMultMini,x,y,'a1')}
            b1 = {executor.submit(processMultMini,x,y,'b1')}
            c1 = {executor.submit(processMultMini,x,y,'c1')}
            d1 = {executor.submit(processMultMini,x,y,'d1')}
            
            a2 = {executor.submit(processMultMini,x,y,'a2')}
            b2 = {executor.submit(processMultMini,x,y,'b2')}
            c2 = {executor.submit(processMultMini,x,y,'c2')}
            d2 = {executor.submit(processMultMini,x,y,'d2')}
    if workers < 8:#en caso de haberse dividido entre 4, cuando un cálculo acaba, se guarda en su variable correspondiente
        for returner in concurrent.futures.as_completed(a):
            a = returner.result()
        for returner in concurrent.futures.as_completed(b):
            b = returner.result()
        for returner in concurrent.futures.as_completed(c):
            c = returner.result()
        for returner in concurrent.futures.as_completed(d):
            d = returner.result()
    
        return [a,b,c,d] #y se retorna la matriz formada por dichas variables calculadas
    elif workers >= 8:#en caso de haberse dividido entre 8, cuando un cálculo acaba, se guarda en su variable correspondiente  
        for returner in concurrent.futures.as_completed(a1):
            a1 = returner.result()
        for returner in concurrent.futures.as_completed(b1):
            b1 = returner.result()
        for returner in concurrent.futures.as_completed(c1):
            c1 = returner.result()
        for returner in concurrent.futures.as_completed(d1):
            d1 = returner.result()
        for returner in concurrent.futures.as_completed(a2):
            a2 = returner.result()
        for returner in concurrent.futures.as_completed(b2):
            b2 = returner.result()
        for returner in concurrent.futures.as_completed(c2):
            c2 = returner.result()
        for returner in concurrent.futures.as_completed(d2):
            d2 = returner.result()
        #se suman las dos mitades calculadas paralelamente a su variable correspondiente
        a = a1+a2
        b = b1+b2
        c = c1+c2
        d = d1+d2
        return [a,b,c,d] #y se retorna la matriz formada por dichas variables
"""
Función usada para paralelizar el clálculo de la multiplicación matricial en caso de que el número 
de cores sea superior o igual a 8
"""
def processMultMini(x,y,case):
    if case == 'a1':
        return x[0]*y[0] 
    elif case == 'b1':
        return x[0]*y[0] 
    elif case == 'c1':
        return x[2]*y[0] 
    elif case == 'd1':
        return x[2]*y[1] 
    if case == 'a2':
        return x[1]*y[2]
    elif case == 'b2':
        return x[1]*y[3]
    elif case == 'c2':
        return x[3]*y[2]
    elif case == 'd2':
        return x[3]*y[3]
"""
Función usada para paralelizar el clálculo de la multiplicación matricial en caso de que el número 
de cores sea inferior o igual a 4
"""    
def processMult(x,y,case):
    if case == 'a':
        return x[0]*y[0] + x[1]*y[2]
    elif case == 'b':
        return x[0]*y[0] + x[1]*y[3]
    elif case == 'c':
        return x[2]*y[0] + x[3]*y[2]
    elif case == 'd':
        return x[2]*y[1] + x[3]*y[3]
"""
Función usada para calcular fibonacci mediante la multiplicación matricial (explicado de forma extensa en la memoria). 
desde aquí se realizan las llamadas a las multiplicaciones matriciales paralelas.
"""
def matpow(mat,n):
    if n == 1:
        return mat
    if ( n % 2 == 0 ):
        return matpow(matmut(mat, mat), n//2 )
    return matmut(mat, matpow( matmut(mat, mat), n//2 ) )
"""
Función fibonacci, se crean las matrices necesarias para calcular fibo mediante multiplicaciones matriciales y se 
hace la primera llamada a matpow()
"""
def matfib(n):
    A = [1,1,1,0]
    v = [1,0]
    return matmut(matpow(A,n-1),v)[0]
        
# endregion
# endregion

if __name__ == "__main__":

    data = DataController()