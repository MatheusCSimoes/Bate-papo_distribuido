import json
import rpyc
import threading
from tkinter import messagebox
from rpyc.utils.server import ThreadedServer
from userServer import UserServer

SERVER_ADDRESS = 'localhost'
SERVER_PORT = 10000

user_server_port = -1
user_server = None

class User:
    def __init__(self, username=""):
        self.id = -1
        self.username = username
        self.usersList = dict()
        self.status = 0
        self._server_thread = None

        self.chatAddUserMsg = None
        self.mainScreenAddUser = None
        self.mainScreenDisableUser = None

    def connect(self, username=None):
        #envia msg ao servidor para conectar
        #caso o username já exista, vai retornar erro
        #se nao user conectado e atualiza os dados
        self._server_thread = threading.Thread(target=create_server, args=(self.id, self.addUserMsg, self.updateActiveUsers))
        self._server_thread.start()

        try:
            central_server = rpyc.connect(SERVER_ADDRESS, SERVER_PORT)
            self.id = central_server.root.exposed_connect_user(username, ('', user_server_port))
            central_server.close()
        except:
            messagebox.showerror(title='Erro servidor', message='Não foi possível conectar ao servidor.')
            stop_server()
            return False
        
        if self.id == -1:
            print('ERRO!')
            stop_server()
            return False
        
        self.username = username
        return True #retorna True se conectado e False se não conectou

    def disconnect(self):
        if self._server_thread is None: #or self.id == -1:
            return True
        
        disconnect = False
        try:
            central_server = rpyc.connect(SERVER_ADDRESS, SERVER_PORT)
            disconnected = central_server.root.exposed_disconnect_user(self.id)
            central_server.close()
        except:
            messagebox.showerror(title='Erro servidor', message='Não foi possível enviar mensagem ao servidor.')

        if not disconnected:
            return False

        stop_server()
        print('thread is alive: ', self._server_thread.is_alive())
        return True #retorna True se conectado e False se não conectou

    def getActiveUsers(self):
        #pega a msg recebido do sevidor com o dicionario de usuarios ativos
        #se o usuario não está no dicionario do servidor, coloca seu status como inativo
        #se o usuario não está no dicionario de users, cria um novo user
        try:
            central_server = rpyc.connect(SERVER_ADDRESS, SERVER_PORT)
            activeUsers = central_server.root.exposed_get_users_list()
            central_server.close()
        except:
            messagebox.showerror(title='Erro servidor', message='Não foi possível enviar mensagem ao servidor.')

        #activeUsers = dict({"1": '{ "name":"User1", "address":["",10001]}', "2": '{ "name":"User2", "address":["",10002]}'})
        activeUsers = dict(json.loads(activeUsers))
        for userId, userInfo in activeUsers.items():
            if userId in self.usersList:
                self.usersList[userId].updateData(userInfo["name"], userInfo["address"], 1)
            else:
                self.usersList[userId] = UserInfo(userId, userInfo["name"], userInfo["address"], 1)

        for userId in self.usersList.keys():
            if userId not in activeUsers:
                self.usersList[userId].updateStatus(0)

        return activeUsers

    def updateActiveUsers(self, activeUsers=None):
        if activeUsers is None:
            try:
                central_server = rpyc.connect(SERVER_ADDRESS, SERVER_PORT)
                activeUsers = central_server.root.exposed_get_users_list()
                central_server.close()
            except:
                messagebox.showerror(title='Erro servidor', message='Não foi possível enviar mensagem ao servidor.')
                return

        activeUsers = dict(json.loads(activeUsers))
        for userId, userInfo in activeUsers.items():
            if userId in self.usersList:
                self.usersList[userId].updateData(userInfo["name"], userInfo["address"], 1)
            else:
                self.usersList[userId] = UserInfo(userId, userInfo["name"], userInfo["address"], 1)
                #chama callback para adicionar botao
                if self.mainScreenAddUser is not None:
                    self.mainScreenAddUser(self.usersList[userId])

        for userId in self.usersList.keys():
            if userId not in activeUsers:
                self.usersList[userId].updateStatus(0)
                #chama callback para desativar chat
                if self.mainScreenDisableUser is not None:
                    self.mainScreenDisableUser(userId)

        return

    def sendMsgToUser(self, userId, msg):
        userAddress = self.usersList[userId].address
        
        try:
            user_server_conn = rpyc.connect(userAddress[0], userAddress[1])
            user_server_conn.root.exposed_receive_msg(self.id, msg)
            user_server_conn.close()
        except:
            messagebox.showerror(title='Erro usuário', message='Não foi possível enviar mensagem ao usuário.')
            return False
        
        return True

    def addUserMsg(self, userId, msg):
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