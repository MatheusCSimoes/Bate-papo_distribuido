import rpyc
from rpyc.utils.server import ThreadedServer

class UserServer(rpyc.Service):
    def __init__(self, uid, addUserMsg, updateUsersList):
        self.userId = uid
        self.callback_addUserMsg = addUserMsg
        self.callback_updateUsersList = updateUsersList

    def on_connect(self, conx):
        print("Conexao estabelecida.")
    def on_disconnect(self, conx):
        print("Conexao encerrada.")

    def exposed_receive_msg(self, clientUserId, msg):
        return self.callback_addUserMsg(clientUserId, msg)

    def exposed_update_user_list(self, userList):
        return self.callback_updateUsersList(userList)
