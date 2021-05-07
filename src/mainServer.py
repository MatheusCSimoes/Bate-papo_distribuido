import rpyc
import json
import threading
from rpyc.utils.server import ThreadedServer
from user import UserInfo

usersList = dict()
counter = 0

lock = threading.Lock()

class CentralServer(rpyc.Service):
    def on_connect(self, conx):
        print("Conexao estabelecida.")
    def on_disconnect(self, conx):
        print("Conexao encerrada.")
        
    def exposed_connect_user(self, username, userAddress):
        global usersList
        global counter

        userNames = [items[1].name for items in usersList.items()]
        
        if username in userNames:
            return -1

        lock.acquire()
        userId = counter
        usersList[userId] = UserInfo(userId, username, userAddress, 1)
        counter = counter + 1
        lock.release()

        for uid, uInfo in usersList.items():
            print(uid, ':', uInfo.id, ',', uInfo.name, ',', uInfo.address)

        list_to_send = {k: v.to_dict() for k, v in usersList.items()}
        list_to_send = json.dumps(list_to_send)
        for uid, udata in usersList.items():
            if uid == userId:
                continue
            user_server = rpyc.connect(udata.address[0], udata.address[1])
            user_server.root.exposed_update_user_list(list_to_send)
            user_server.close()

        return str(userId)

    def exposed_disconnect_user(self, userId):
        global usersList

        userId = int(userId)

        print('exposed_disconnect_user', userId)
        print(type(userId))
        if userId not in usersList.keys():
            return False
        
        lock.acquire()
        del usersList[userId]
        lock.release()

        print(usersList)

        #enviar msg aos users para atualizar lista
        return True

    def exposed_get_users_list(self):
        global usersList

        print('INSIDE exposed_get_users_list')

        list_to_send = {k: v.to_dict() for k, v in usersList.items()}
        return json.dumps(list_to_send) 

mainServer = ThreadedServer(CentralServer, port=10000)
mainServer.start()