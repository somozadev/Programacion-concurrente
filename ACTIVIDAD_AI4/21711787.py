from concurrent.futures import thread
from multiprocessing import Process, Pipe
import concurrent.futures
import json
import os
import platform
import sys
import time
import math
import numpy as np
import random

from numpy.lib import arraypad

EXPEDIENTE = 21_711


class Timer():
    def __init__(self):
        pass


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
        with open('E:/CARRERA/4ºCARRERA/2º CUATRI/Programacion concurrente/ACTIVIDAD_AI4/users.json', 'r') as r:
            self.usersList = (json.loads(r.read()))

    def AddUser(self, userObject):
        self.usersList.append(userObject.toDict())
        self.SaveUsers()

    def SaveUsers(self):
        # userListDict = [user.toDict() for user in self.usersList]
        print(self.usersList)
        print(type(self.usersList))
        with open('E:/CARRERA/4ºCARRERA/2º CUATRI/Programacion concurrente/ACTIVIDAD_AI4/users.json', 'w') as f:
            json.dump(self.usersList, f)

    def Register(self):
        User(input("Username:"), input("Password: "), self)
        self.ManageUsersPanel()

    def Login(self):
        user = input("username: ")
        password = input("password: ")

        for dbUser in self.usersList:
            if dbUser['user'] == user and dbUser['password'] == password:
                print("welcome back, ", user)
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
          )
    response = input()
    if response == 'A':
        ExerciceA()
    elif response == 'B':
        ExerciceB()
    elif response == 'C':
        ExerciceC()
    else:
        ExercicesMenu()


# *
# * como os.cpu_count() = 20 ; tenemos 20 cores virtuales y 20/2 = 10 cores físicos
# *

def ExerciceA():

    # * ANTIGUAMENTE SE HACÍA A MANO
    # *processes = []
    # *start = time.perf_counter()
    # *for _ in range(10):
    # *    p = multiprocessing.Process(target = ExerciceB)
    # *    p.start()
    # *    processes.append(p)
    # *for process in processes:
    # *    process.join()
    # *
    # *finish = time.perf_counter()
    # *print(f'Finished in {round(finish-start,2)} second(s)')

    m1 = CreateMatrix()
    m2 = CreateMatrix()

    # with concurrent.futures.ProcessPoolExecutor() as executor:
    #     results = [executor.submit(ExerciceB) for _ in range(10)]
    #     for f in concurrent.futures.as_completed(results):
    #         print(f.result())

    print("exA")


def CreateMatrix():
    n = (math.ceil(math.sqrt(pow(EXPEDIENTE, 3))))  # matriz de orden N
    print("exp", EXPEDIENTE)
    print("pow", pow(EXPEDIENTE, 3))
    print("sqrt", math.sqrt(pow(EXPEDIENTE, 3)))
    print("final", n)
    m = [0] * n
    print(m)
    np.array[None, EXPEDIENTE]
    return np.array([[1, 2, 3], [1, 2, 3], [1, 2, 3]])


def ExerciceB():
    startArray = []
    workers = int(os.cpu_count()/2 - 2)

# * STARTED CREATING THE ARRAY USING PROCESS (MY ACTUAL NUMBER - 2 are being used, for performance issues)

    startFillup = time.perf_counter()
    print(
        f"Started to fillup array with {EXPEDIENTE} elements and {workers} processors ")
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        results = [executor.submit(AddToArray, workers)
                   for _ in range(workers)]
        for f in concurrent.futures.as_completed(results):
            startArray = startArray + (f.result())

        finishFillup = time.perf_counter()
    print(f'Finished in {round(finishFillup-startFillup,2)} second(s)')
    for _ in range(len(startArray) - EXPEDIENTE):
        startArray.pop()

# * FINISHED ARRAY CREATING PROCESS

    startMergeSort = time.perf_counter()
    print(
        f"Started MergeSort array with {EXPEDIENTE} elements and {workers} processors ")
    
    startArray = MergeSort(startArray, workers)

    finishMergeSort = time.perf_counter()
    print(startArray[:20])
    print(f'Finished in {round(finishMergeSort-startMergeSort,2)} second(s)')
    input()

def MergeSort(startArray, workers):

    cconn, pconn = Pipe()
    p = Process(target=MergeSortParalell, args=(startArray, cconn, workers-1))
    p.start()
    startArray = cconn.recv()
    p.join()


def MergeSortIterative(startArray):
    if len(startArray) <= 1:
        return startArray
    mid = len(startArray)//2
    return Merge(MergeSort(startArray[:mid]), MergeSort(startArray[mid:]))

#SORTS THE TWO GIVEN ARRAYS left & right WHILE MERGES THEM IN A SINGLE ARRAY returner
def Merge(left,right):
    returner = []
    leftL = rightL = 0
    while leftL < len(left) and rightL < len(right):
        if left[leftL] <= right[rightL]:
            returner.append(left[leftL])
            leftL+=1
        else:
            returner.append(right[rightL])
            rightL+=1
    if leftL == len(left):
        returner.extend(right[rightL:])
    else:
        returner.extend(left[leftL:])
    return returner

def MergeSortParalell(startArray, conn, workers):
    if workers <= 0 or len(startArray) <= 1:
        conn.send(MergeSortIterative(startArray))
        conn.close()
        return
    mid = len(startArray)//2
    pconnLeft, cconnLeft = Pipe()
    pconnRight, cconnRight = Pipe()
    leftProc = Process(target=MergeSortParalell, args=(startArray[:mid],pconnLeft,workers-1))
    rightProc = Process(target=MergeSortParalell, args=(startArray[mid:],pconnRight,workers-1))
    leftProc.start()
    rightProc.start()
    
    conn.send(Merge(pconnLeft.recv(),pconnRight.recv()))
    conn.close()
    leftProc.join()
    rightProc.join()

def AddToArray(workers):
    arrayPart = []
    for _ in range(math.ceil(EXPEDIENTE/workers)):
        arrayPart.append(random.randint(0, math.ceil(EXPEDIENTE/workers)))
    print("...")
    return arrayPart


# * qué mas dará el numero de cores cuando dependemos del numero anterior(el calculo anterior hecho por fib)
# * no podemos hacer que un nucleo opere hasta que acabe el otro... no sería mejor entonces utilizar hilos????????


def ExerciceC():
    workers = int(os.cpu_count()/2 - 2)


# endregion
if __name__ == "__main__":

    data = DataController()
