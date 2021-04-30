

class User:
    def __init__(self, username, status):
        self.username = username
        self.status = status
        self.usersList = []

    def changeStatus(self, newStatus):
        if newStatus == self.status:
            return

        #manda msg para o servidor

    def getActiveUsersList(self, msg):
        #pega a msg recebido do sevidor com o dicionario de usuarios ativos
        #se o usuario já está na dicionario do user, apenas atualiza seu status
        #se não, cria um novo user

        return

    def add_new_user(self, username, status, address):
        user = OtherUser(username, status, address)
        