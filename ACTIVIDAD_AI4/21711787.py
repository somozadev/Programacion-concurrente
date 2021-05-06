from concurrent.futures import thread
from multiprocessing import Process
import multiprocessing as mp
import concurrent.futures
import json
import multiprocessing
import os
import platform
import sys
import time
import math
import random

from numpy.lib import arraypad

EXPEDIENTE = 2171178#20000  # 21711787
workers = int(os.cpu_count()/2 - 2)


class ConsoleClear():
    def __init__(self):
        if platform.system() == 'Windows':
            def clear(): return os.system('cls')
            clear()
        elif platform.system() == 'Linux' or 'Darwin':
            def clear(): return os.system('clear')
            clear()
            
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


def ExercicesMenu():
    
    ConsoleClear()
    print(" **************************", "\n",
          "* SELECCIONE LA ACTIVIDAD *", "\n"
          " **************************", "\n",
          " - A: Ejercicio A ", "\n",
          " - B: Ejercicio B ", "\n",
          " - C: Ejercicio C ", "\n",
          " - L: Login menu ", "\n",
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


#region ej_A
def ExerciceA():

    # cuando pasamos al expediente de n7 (2171178) es necesario externalizar los calculos a la nube.
    # el error es el siguiente: OSError: [WinError 1455] El archivo de paginación es demasiado pequeño para completar la operación
    
    # Genero A[21535220][6]con num. aleatorios del 0 al 215
    m1 = [[random.randint(0, 215) for i in range(6)] for j in range(217117)] #21711787
    
    # Genero B[6][21535220]con num. aleatorios del 0 al 215
    m2 = [[random.randint(0, 215) for i in range(200)] for j in range(6)]
    m1f = len(m1)  # Obtengo num de filas de A
    m1c = len(m1[0])  # Obtengo num de colunmas de A
    m2f = len(m2)  # Obtengo num de filas de B
    m2c = len(m2[0])  # Obtengo num de filas de B
    if m1c != m2f:
        # Compruebo que se puedan multiplicar A y B
        raise Exception('Dimensiones no validas')

    startMultiply = time.time()
    MultiplyMat(m1, m2, m2c, m1f) 
    endMultiply = time.time()
    input(f'Finished multiply matrix in {round(endMultiply-startMultiply,2)} second(s)...')
    input(". . .")
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

# STARTED CREATING THE ARRAY USING PROCESS (MY ACTUAL NUMBER - 2 are being used, for performance issues)

    startFillup = time.perf_counter()
    print(
        f"Started to fillup array with {EXPEDIENTE} elements and {workers} processors ")
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        results = [executor.submit(AddToArray, workers)
                   for _ in range(workers)]
        for f in concurrent.futures.as_completed(results):
            startArray = startArray + (f.result())

        finishFillup = time.perf_counter()
    print(f'Finished fillup in {round(finishFillup-startFillup,2)} second(s)')
    for _ in range(len(startArray) - EXPEDIENTE):
        startArray.pop()

#  FINISHED ARRAY CREATING PROCESS

    startMergeSort = time.perf_counter()
    print(f"Started MergeSort array with {EXPEDIENTE} elements and {workers} processors ")
    MergeSort(startArray, 0, workers)
    endMergeSort = time.perf_counter()
    print(f'Finished MergeSort in {round(endMergeSort-startMergeSort,2)} second(s)')
    input(". . .")
    ExercicesMenu()
    


def MergeSort(startArray, i , workers):
    if len(startArray) == 1:
        return startArray
    
    if pow(2,i) < workers: 
        i += 1
    mid = len(startArray) // 2
    left = startArray[:mid]
    right = startArray[mid:]
    if pow(2,i) == workers:
        workers-= 2
        with concurrent.futures.ProcessPoolExecutor(max_workers= 2) as executor:
            result1 = executor.submit(MergeSort,left, i , workers)
            result2 = executor.submit(MergeSort,right, i , workers)
            print(result1, "has started with left side")
            print(result2, "has started with right side")
            
            arrOne = result1.result()
            arrTwo = result2.result()
    
    else:
        arrOne = MergeSort(left, i , workers)
        arrTwo = MergeSort(right, i , workers)
    
    return Merge(arrOne,arrTwo)

def Merge(arrA, arrB):
    arrC = []
    
    while len(arrA) > 0 and len(arrB) > 0 : 
        if arrA[0] > arrB[0]: 
            arrC.append(arrB[0]) 
            arrB.remove(arrB[0])
        else: 
            arrC.append(arrA[0])
            arrA.remove(arrA[0])
    while len(arrA) > 0: 
        arrC.append(arrA[0])
        arrA.remove(arrA[0])    
    
    while len(arrB) > 0: 
        arrC.append(arrB[0])
        arrB.remove(arrB[0])
        
    return arrC

def AddToArray(workers):
    arrayPart = []
    for _ in range(math.ceil(EXPEDIENTE/workers)):
        arrayPart.append(random.randint(0, EXPEDIENTE))
    print("...")
    return arrayPart

#endregion
#region ej_C

# qué mas dará el numero de cores cuando dependemos del numero anterior(el calculo anterior hecho por fib)
#  no podemos hacer que un nucleo opere hasta que acabe el otro... 

def ExerciceC():
    startFib = time.perf_counter()
    print(f"Started fibonacci sequence with number {EXPEDIENTE} and {workers} processors ")
    fibP(EXPEDIENTE)
    endFib = time.perf_counter()
    print(f'Finished fibonacci in {round(endFib-startFib,2)} second(s)')
    input(". . .")
    ExercicesMenu()

def fibP(nums):
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor: 
        fibRet = {executor.submit(fib,nums,)}
    
    for returner in concurrent.futures.as_completed(fibRet):
        n,f = returner.result()
        # print("{0}: {1}".format(n,f))
    

def fib(n):
    a,b = 0,1
    for _ in range(0,n):
        a,b = b, a + b 
    return((n,a))

        
# endregion
# endregion


if __name__ == "__main__":

    data = DataController()
