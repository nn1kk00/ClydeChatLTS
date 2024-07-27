print('Enabling servers...')

import socket, json, time, asyncio, random, os
from datetime import timezone, date, datetime

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
now = datetime.now()

class db:
    def __init__():
        print('''ClydeChat version - 1.00''')
        while True:
            try:
                exec('>>> ')
            except Exception as ex: print(f'Error: {ex}')
    def get():
        try:
            with open('utils/js/accounts.json', 'r', encoding='utf-8') as file:
                req = json.load(file)
                dataacc = req.json()
                print('Accounts is loaded!')
            with open('utils/js/messages.json', 'r', encoding='utf-8') as file:
                req = json.load(file)
                datamsg = req.json()
                print('Messages is loaded!')
            with open('utils/js/chats.json', 'r', encoding='utf-8') as file:
                req = json.load(file)
                datachat = req.json()
                print('Chats is loaded!')
            with open('utils/js/conf.json', 'r', encoding='utf-8') as file:
                req = json.load(file)
                dataconf = req.json()
                print('Config is loaded!')
            print('All data is loaded!')
        except Exception as ex:
            print(f'In your data files has been a error: {ex}')
    def create_account(dataconf, addr, name):
        with open('utils/js/accounts.json', 'a', encoding='utf-8') as file:
            data = {
                str(addr): str(name)
            }
            json_result = json.dump(data, file)
        with open('utils/js/conf.json', 'a', encoding='utf-8') as file:
            data = {
                "all_users": dataconf['all_users']+1
            }
            json_conf = json.dump(data, file)
            dataconf['all_users'] += 1
    def create_chat(conn, datachat, dataconf, addr, name):
        id = f'{random.randint(1000, 9999)}CLDCH{random.randint(1000, 9999)}'
        with open(f'utils/data/js/{id}.json', 'w', encoding='utf-8') as file:
            data = {"id": id,
                    "name": str(name),
                    "admin": str(addr),
                    "all_msgs": 1,
                    "members": f"members{id}.json"
                    }
            json_aa = json.bump(data, file)
            file.close()
        conn.send(id.encode('utf-8'))
        with open('utils/js/conf.json', 'a', encoding='utf-8') as file:
            data = {
                'all_chats': dataconf['all_chats']+1
            }
            json_conf = json.dump(data, file)
            dataconf['all_chats'] += 1
        with open('utils/js/chats.json', 'a', encoding='utf-8') as file:
            data = {
                int(dataconf['all_chats']): str(id)
            }
            json_chats = json.dump(data, file)
        with open(f'utils/chats/txt/{id}.txt', 'w', encoding='utf-8') as file:
            global now
            file.write(f'({now.year}.{now.month}.{now.day}/{now.strftime("%H:%M:%S")})[Clyde]: Welcome to the "ClydeChat"! There chat created for chatting, another talks, and more. Enjoy!\n')
            file.close()
        conn.send(b'0')
    def add_message(datachats, dataacc, datamsg, srvid, addr, msg):
        global now
        with open(f'utils/chats/txt/{srvid}.txt', 'a', encoding='utf-8') as file:
            name = dataacc[addr]
            file.write(f'({now.year}.{now.month}.{now.day}/{now.strftime("%H:%M:%S")})[{name}]: {msg}\n')
            file.close()
        with open(f'utils/data/js/{srvid}.json', 'r', encoding='utf-8') as file:
            dat = json.load(file)
        with open(f'utils/data/js/{srvid}.json', 'a', encoding='utf-8') as file:
            data = {
                'all_msgs': dat['all_msgs']+1
            }
            json_a = json.dump(data, file)
    def join(conn, datachats, dataacc, srvid, addr):
        with open(f'utils/data/js/members{srvid}.json', 'a', encoding='utf-8') as f:
            data = {
                str(addr): str(dataacc(addr))
            }
            json_b = json.dump(data, file)
        with open(f'utils/data/js/{srvid}.json', 'r', encoding='utf-8') as file:
            dat = json.load(file)
        with open(f'utils/data/js/{srvid}.json', 'a', encoding='utf-8') as file:
            data = {
                'all_msgs': dat['all_msgs']+1
            }
            json_a = json.dump(data, file)
        with open(f'utils/chats/txt/{srvid}.txt', 'a', encoding='utf-8') as file:
            name = dataacc[addr]
            file.write(f'({now.year}.{now.month}.{now.day}/{now.strftime("%H:%M:%S")})[{name}] Has joined the room.\n')
            file.close()
        with open(f'utils/chats/txt/{srvid}.txt', 'r', encoding='utf-8') as file:
            srs = file.read()
            conn.send(srs.encode('utf-8'))
        conn.send(b'0')
    def update_msg(conn, text):
        text = text.split('|')
        with open(f'utils/chats/txt/{text[1]}.txt', 'r', encoding='utf-8') as file:
            srs = file.read()
            file.close()
        conn.send(srs.encode('utf-8'))
class Server:
    async def restart(): 
        print('The system has restarted from 5 seconds')
        await asyncio.sleep(5)
        os.open('main.py')
        exit(0)
    async def freeze():
        print('The system is freezed in 10 minutes.')
        time.sleep(600)
        print('The system is unfreezed!')
    async def stop():
        print('The system has shutdown from 30 seconds')
        await asyncio.sleep(30)
        exit(0)
    def start():
        db.get()
        s.bind((socket.gethostbyname(socket.gethostname()), 2013))
        s.listen()
        try:
            print(f'Done! Server is started. IP: {socket.gethostbyname(socket.gethostname())} ; port: 2013')
            while True:
                addr, conn = s.accept()
                conn.send(b'0')
                data = s.recv(1024).decode('utf-8')
                if not data: return
                elif data == 'toplist':
                    with open('utils/js/conf.json', 'r', encoding='utf-8') as file:
                        data_conf = json.load(file)
                    with open('utils/js/chats.json', 'r', encoding='utf-8') as file:
                        data_chat = json.load(file)
                    if data_chat == {}: 
                        send = f'All chats: 0\n\n'
                        for i in range(1, data_conf['all_chats']):
                            send = send+f'Nothing... Create chat in button "Create Chat"\n'
                    else:
                        send = f'All chats: {data_conf['all_chats']}\n\n'
                        for i in range(1, data_conf['all_chats']):
                            send = send+f'{i}| {data_chat[str(i)]}\n'
                    conn.send(send.encode('utf-8'))
                elif data == 'Connect to chat':
                    data = s.recv(1024).decode('utf-8')
                    db.join(addr=addr, srvid=data)
                    with open(f'utils/chats/txt/{data}.txt', 'r', encoding='utf-8') as f:
                        hist = f.read() # hist go v gs
                        f.close()
                    conn.send(hist.encode('utf-8'))
                    conn.send(b'0')
                elif data == 'Create chat':
                    data = s.recv(1024).decode('utf-8')
                    db.create_chat(addr=addr, name=data)
                    conn.send(b'0')
                elif data == 'Create user':
                    data = s.recv(1024).decode('utf-8')
                    #with open('utils/js/accounts.json', 'r', encoding='utf-8') as file:
                    #    dataacc = json.load(file)
                    #if data in dataacc[]
                    db.create_account(addr=addr, name=data)
                    conn.send(b'0')
                elif data.find('Send msg|') == 1:
                    data = data.split('|')
                    if data[2].find('>>>') == 1:
                        b = data[2]
                        exec(b[2:len(b)])
                    else:
                        db.add_message(srvid=data[1], msg=data[2], addr=addr)
                        conn.send(b'0')
                elif data.find('Update msg|') == 1:
                    db.update_msg(text=data)
        except Exception as ex:
            with open('logs.txt', 'a') as f:
                f.write(f'Error: {ex}\n------\n')
                f.close()
            return
        
Server.start()