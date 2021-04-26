from collections import UserList
import json
import os
import platform
import sys

class ConsoleClear():
    def __init__(self):
        if platform.system() == 'Windows':
            clear = lambda: os.system('cls')
            clear()
        elif platform.system() == 'Linux' or 'Darwin':
            clear = lambda: os.system('clear')
            clear()

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
        self.usersDict = []
        self.GetUsers()
        print("self.usersDict:",self.usersDict , "\n")  

    def GetUsers(self):
        with open('ACTIVIDAD_AI4/users.json', 'r') as r:
            self.usersDict = json.loads(r.read())

    def AddUser(self, userObject):
        self.usersList.append(userObject)
        self.SaveUsers()
    def SaveUsers(self):
        userListDict = [user.toDict() for user in self.usersList]
        saver = json.dumps(userListDict)
        with open('ACTIVIDAD_AI4/users.json', 'w') as f:
            json.dump(saver, f)

def Register(data):
    newUser = User(input("Username:"),input("Password: "),data)
def Login():
    print("login")

def ManageUsersPanel(data): 
    print(platform.system())
    ConsoleClear()
    print(  " ********************","\n",
            "* INICIO DE SESIÓN *", "\n"
            " ********************","\n",
            " - R para registrarse", "\n",
            " - L para iniciar sesión", "\n",  
            " - X para salir", "\n",          
          )
    response = input()
    if response == 'R':
        Register(data)
    elif response == 'L':
        Login()
    elif response == 'X':
        sys.exit()
    else: ManageUsersPanel()
        
if __name__ == "__main__":
    
    data = DataController()
    User("1",1,data)
    User("2",2,data)
    User("3",3,data)
    User("4",4,data)
    # ManageUsersPanel(data)
    
