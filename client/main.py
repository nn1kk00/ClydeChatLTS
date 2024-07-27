print('Starting client...')

import json, socket, random, time, asyncio, os

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

class db:
    def get():
        with open('utils/js/conf.json', 'r', encoding='utf-8') as file:
            data = json.load(file)
            print('Config is loaded!')
            return data
    def create_chat(data, name: str):
        s.send(name.encode('utf-8'))
        id = s.recv(1024).decode('utf-8')
        with open('utils/js/conf.json', 'a', encoding='utf-8') as file:
            temp = {
                "name_chat": name,
                "id_chat": id
            }
            json_result = json.dump(temp, file)
        data["name_chat"] = name
        data["id_chat"] = id
        dat = s.recv(1024).decode('utf-8')
        if dat == '0': return
        else: print('Error Server')
    def edit_ip_server(data, ip: str):
        s.close()
        data["server_ip"] = ip
        with open('utils/js/conf.json', 'a', encoding='utf-8') as file:
            temp = {
                "server_ip": ip
            }
            json_result = json.dump(temp, file)
        print('Done, ip adress has edited to DB.')
        s.connect((data["server_ip"], 2013))
    def edit_id_chat(data, id: str):
        s.send(b'Connect to chat')
        data["id_chat"] = id
        with open('utils/js/conf.json', 'a', encoding='utf-8') as file:
            temp = {
                "id_chat": id
            }
            json_result = json.dump(temp, file)
        s.send(id.encode('utf-8'))
        srs = s.recv(1024).decode('utf-8')
        dat = s.recv(1024).decode('utf-8')
        if dat == '0': return srs
        else: print('Server Error')
    def create_account(data, name: str):
        s.send(b'Create user')
        try:
            data["ip"] = str(socket.gethostbyname(socket.gethostname))
            with open('utils/js/conf.json', 'a', encoding='utf-8') as file:
                temp = {
                    "ip": str(socket.gethostbyname(socket.gethostname)),
                    "name": name
                }
                json_result = json.dump(temp, file)
                return json_result
        except Exception as ex:
            with open('logs.txt', 'a', encoding='utf-8') as file:
                file.write(f'[Console] DataBase Error, output: {ex};\n')
                file.close()
            print(f'[Logs] DataBase Error, output: {ex};')
        s.send(name.encode('utf-8'))
        dat = s.recv('1024').decode('utf-8')
        if dat == '0': return
        else: print('Error Server')

class Client:
    def stop():
        print('Client is shutdown from 5 seconds')
        time.sleep(5)
        exit(0)
    def restart():
        print('Client is restarting from 10 seconds')
        time.sleep(10)
        os.open('main.py')
        exit(0)
    def freeze():
        print('Client is freezed in 10 minutes')
        time.sleep(600)
        print('Client is unfreezed')
    def update_msgs(srvid):
        s.send(f'Update msg|{srvid}'.encode('utf-8'))
        srs = s.recv(1024).decode('utf-8')
        return srs
    def send_message(srvid, text):
        temp = f'Send msg|{srvid}|{text}'.encode('utf-8')
        s.send(temp)
    def start():
        db.get()
        print('Hello from ClydeChatLTS Developers. Thanks what you downloaded our messeger.\nFor help type "help".')
        while True:
            try:
                inp = input('>>> ')
                if inp == 'help':
                    print('''===Help===
Create acc = creaing account (reg in our IP adress)
Create chat = creating a chat in server
Add chat, edit chat = joining to chat in ID (Example id: 1249CHATCL3523):
    > - pole for message ( quit: >>exit.chat );
Top chats = top chats in server
Edit IP = editing IP adress server ( in console server ip adress is exist )
''')
                    time.sleep(5)
                elif inp == "Top chats":
                    s.send(b'toplist')
                    dat = s.recv(1024).decode('utf-8')
                    print(dat)
                    time.sleep(15)
                elif inp == 'Edit IP':
                    db.edit_ip_server(ip=input('Type IP adress your PC when connected to RadminVPN: '))
                    print('Done!')
                    time.sleep(5)
                elif inp == 'Create acc':
                    db.create_account(name=input('Type name for account( Your name has been linked to your IP ): '))
                    print('Done!')
                    time.sleep(5)
                elif inp == 'Create chat':
                    global data
                    db.create_chat(name=input('Type name for your chat: '))
                    print(f'Your chatname: {data["name_chat"]}, IDchat: {data["id_chat"]};')
                    time.sleep(5)
                elif inp == "Add chat" or inp == "edit chat":
                    db.edit_id_chat(id=input('Type ID for connecting: '))
                    while True:
                        global srs
                        print('\n'*1000+f'''-------------------------Chat--------------------------
{srs}
------------------------------------------------------''')
                        with open('utils/js/conf.json', 'r', encoding='utf-8') as file:
                            data = json.load(file)
                            file.close()
                        inp = input(data["name"]+': ')
                        if inp == '>>exit.chat':
                            break
                        else:
                            Client.send_message(srvid=data["id_chat"], text=inp)
                            Client.update_msgs(srvid=data["id_chat"])
            except Exception as ex:
                with open('logs.txt', 'a', encoding='utf-8') as file:
                    file.write(f'[Console] Client Err: {ex}')
                    file.close()
                print(f'[Logs] Client Err: {ex}')
