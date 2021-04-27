import multiprocessing
import concurrent.futures
import json
import os
import platform
import sys
import time
import math
from warnings import catch_warnings
import numpy as np
import random

from numpy.lib import arraypad

EXPEDIENTE = 21711787


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
    workers = int(os.cpu_count()/2-2)

#* STARTED CREATING THE ARRAY USING PROCESS (MY ACTUAL NUMBER - 2 are being used, for performance issues)
    
    startFillup = time.perf_counter()
    print(f"Started to fillup array with {EXPEDIENTE} elements and {workers} processors ")
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        results = [executor.submit(AddToArray, workers) for _ in range(workers)]
        for f in concurrent.futures.as_completed(results):
            startArray = startArray + (f.result())
        
        finishFillup = time.perf_counter()    
    print(f'Finished in {round(finishFillup-startFillup,2)} second(s)')
    for _ in range(len(startArray) - EXPEDIENTE):
        startArray.pop()
        
#* FINISHED ARRAY CREATING PROCESS
    MergeSort([0,1,2,3,4,5,6,7])
    
    #idea1: dividir el array total en 8 (nºde proces./2 - 2) y hacer mergesort en cada parte
    #luego, hacer un mergesort del resto??
def CustomMergeSort(workers,startArray):
    arrayParts = []
    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        results = [executor.submit(Devide, startArray,worker) for worker in range(workers)]
        for f in concurrent.futures.as_completed(results):
            arrayParts.append(f.result())
def Devide(startArray, worker):
    arr = startArray[worker-1:worker]
    pass


def MergeSort(startArray):
    if len(startArray) <= 1:
        return startArray
    else:
        mid = int(len(startArray)/2)
        left = startArray[: mid]
        right = startArray[mid :]
        print(left,right)
        
        left = MergeSort(left)
        right = MergeSort(right)

    


def AddToArray(workers):
    arrayPart = []
    for _ in range(math.ceil(EXPEDIENTE/workers)):
        arrayPart.append(random.randint(0, 50))
    print("...")
    return arrayPart





def ExerciceC():
    print("exC")


# endregion
if __name__ == "__main__":

    data = DataController()
