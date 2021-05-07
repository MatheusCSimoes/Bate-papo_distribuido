import json
import rpyc
import threading
from rpyc.utils.server import ThreadedServer
from userServer import UserServer

SERVER_ADDRESS = 'localhost'
SERVER_PORT = 10000

user_server_port = -1
user_server = None

class User:
    def __init__(self, username="", uid=-1, activeUsers=dict(), status=0):
        self.id = uid
        self.username = username
        self.usersList = activeUsers
        self.status = status
        self._server_thread = None

        self.chatAddUserMsg = None
        self.mainScreenAddUser = None
        self.mainScreenDisableUser = None

    def __changeStatus(self, newStatus):
        if newStatus == self.status:
            return

        #manda msg para o servidor

    def connect(self, username=None):
        #envia msg ao servidor para conectar
        #caso o username já exista, vai retornar erro
        #se nao user conectado e atualiza os dados

        self._server_thread = threading.Thread(target=create_server, args=(self.id, self.addUserMsg, self.updateActiveUsers))
        self._server_thread.start()

        central_server = rpyc.connect(SERVER_ADDRESS, SERVER_PORT)
        self.id = central_server.root.exposed_connect_user(username, ('', user_server_port))
        central_server.close()
        
        if self.id == -1:
            print('ERRO!')
            stop_server()
            return False
        
        if username is None:
            username = self.username
        else:
            self.username = username

        return True #retorna True se conectado e False se não conectou

    def disconnect(self):
        if self._server_thread is None: #or self.id == -1:
            return True
        
        central_server = rpyc.connect(SERVER_ADDRESS, SERVER_PORT)
        disconnected = central_server.root.exposed_disconnect_user(self.id)
        central_server.close()

        if not disconnected:
            return False

        stop_server()
        print('thread is alive: ', self._server_thread.is_alive())
        return True #retorna True se conectado e False se não conectou

    def getActiveUsers(self):
        #pega a msg recebido do sevidor com o dicionario de usuarios ativos
        #se o usuario não está no dicionario do servidor, coloca seu status como inativo
        #se o usuario não está no dicionario de users, cria um novo user
        print('INSIDE getActiveUsers')

        central_server = rpyc.connect(SERVER_ADDRESS, SERVER_PORT)
        activeUsers = central_server.root.exposed_get_users_list()
        central_server.close()

        print('self.usersList:', self.usersList)
        print('activeUsers:', activeUsers)
        #activeUsers = dict({"1": '{ "name":"User1", "address":["",10001]}', "2": '{ "name":"User2", "address":["",10002]}'})

        activeUsers = dict(json.loads(activeUsers))
        for userId, userInfo in activeUsers.items():
            if userId in self.usersList:
                self.usersList[userId].updateData(userInfo["name"], userInfo["address"], 1)
                #self.usersList[userId].updateData(userInfo.name, userInfo.address, 1)
            else:
                self.usersList[userId] = UserInfo(userId, userInfo["name"], userInfo["address"], 1)
                #self.usersList[userId] = userInfo

        for userId in self.usersList.keys():
            if userId not in activeUsers:
                self.usersList[userId].updateStatus(0)

        return activeUsers

    def updateActiveUsers(self, activeUsers=None):
        print('INSIDE updateActiveUsers')

        if activeUsers is None:
            print('activeUsers is None')
            central_server = rpyc.connect(SERVER_ADDRESS, SERVER_PORT)
            activeUsers = central_server.root.exposed_get_users_list()
            central_server.close()

        print(activeUsers)

        activeUsers = dict(json.loads(activeUsers))
        for userId, userInfo in activeUsers.items():
            if userId in self.usersList:
                self.usersList[userId].updateData(userInfo["name"], userInfo["address"], 1)
            else:
                self.usersList[userId] = UserInfo(userId, userInfo["name"], userInfo["address"], 1)
                #chama callback para adicionar botao
                if self.mainScreenAddUser is not None:
                    print('mainScreenAddUser')
                    self.mainScreenAddUser(self.usersList[userId])

        for userId in self.usersList.keys():
            if userId not in activeUsers:
                self.usersList[userId].updateStatus(0)
                #chama callback para desativar chat
                if self.mainScreenDisableUser is not None:
                    self.mainScreenDisableUser(userId)

        return activeUsers

    def sendMsgToUser(self, userId, msg):
        userAddress = self.usersList[userId].address
        
        print('User server address:', userAddress[0], userAddress[1])
        user_server_conn = rpyc.connect(userAddress[0], userAddress[1])
        user_server_conn.root.exposed_receive_msg(self.id, msg)
        user_server_conn.close()
        
        return True

    def addUserMsg(self, userId, msg):
        print('addUserMsg:', userId, msg)
        print(self.chatAddUserMsg)
        if self.chatAddUserMsg is not None:
            self.chatAddUserMsg(userId, msg)

        return

class UserInfo:
    def __init__(self, userId, userName, userAddress, userStatus):
        self.id = userId
        self.name = userName
        self.address = userAddress
        self.status = userStatus

    def updateData(self, userName, userAddress, userStatus):
        self.name = userName
        self.address = userAddress
        self.status = userStatus
    
    def updateStatus(self, userStatus):
        self.status = userStatus

    def to_dict(self):
        return {"name": self.name, "address": self.address}

def stop_server():
    global user_server
    global user_server_port

    if user_server is not None:
        user_server.close()

    user_server = None
    user_server_port = -1

def create_server(userId, callback_addUserMsg, callback_updateUsersList):
    global user_server 
    global user_server_port

    user_server = ThreadedServer(UserServer(userId, callback_addUserMsg, callback_updateUsersList))
    user_server_port = user_server.port
    
    print('server created with port:', user_server_port)

    user_server.start()

    print("server stopped and thread end")