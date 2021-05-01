import json

class User:
    def __init__(self, username="", id=-1, activeUsers=dict(), status=0):
        self.id = id
        self.username = username
        self.usersList = activeUsers
        self.status = status

    def __changeStatus(self, newStatus):
        if newStatus == self.status:
            return

        #manda msg para o servidor

    def connect(self, username=None):
        #envia msg ao servidor para conectar
        #caso o username já exista, vai retornar erro
        #se nao user conectado e atualiza os dados

        if username is None:
            username = self.username
        else:
            self.username = username

        return True #retorna True se conectado e False se não conectou

    def getActiveUsers(self):
        #pega a msg recebido do sevidor com o dicionario de usuarios ativos
        #se o usuario não está no dicionario do servidor, coloca seu status como inativo
        #se o usuario não está no dicionario de users, cria um novo user

        activeUsers = {"1": '{ "name":"User1", "Address":('', 1)}', "2": '{ "name":"User2", "Address":('', 2)}'}

        return activeUsers

    def sendMsgToUser(self, userId, msg):
        #send message

        return True

        