# -*- coding: utf-8 -*-
import time
import multiprocessing
import socket
from logging import getLogger,FileHandler,DEBUG,Formatter
import re
import sys

# マルチプロセスTCPサーバ
class MultiprocessingSocketStreamServer(object):
    # 待ち受けポートとworkerプロセスの数を指定する 
    def __init__(self, ipaddress, port, max_processes):
        #ロガーの初期化
        self._logger = getLogger('server')
        self._logger.setLevel(DEBUG)
        formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler = FileHandler(filename = 'server.log', encoding = 'utf-8')
        handler.setLevel(DEBUG)
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

        # IPv4 / TCP のソケットを用意する
        self._serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # TIME_WAIT等で同じポートのコネクションが残っていても上書き利用する
        self._serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._serversocket.bind((ipaddress, port))
        self._serversocket.listen(5)
        self._max_processes = max_processes

    # 接続を処理するハンドラを指定する 
    def start(self, handler):
        while True:
            conn, address = self._serversocket.accept()
            process = multiprocessing.Process(target=handler, args=(conn, address))
            process.daemon = True
            process.start()
            self._logger.debug("プロセス数：" + str(len(multiprocessing.active_children())))
            while len(multiprocessing.active_children()) >= self._max_processes :
                self._logger.debug("プロセス数が最大値に達しました。プロセス数：" + str(len(multiprocessing.active_children())))
                time.sleep(1)

# TCP を処理するハンドラ 
class SocketStreamHandler(object):
    def __init__(self):
        #ロガーの初期化
        self._logger = getLogger('handler')
        self._logger.setLevel(DEBUG)
        formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler = FileHandler(filename = 'server.log', encoding = 'utf-8')
        handler.setLevel(DEBUG)
        handler.setFormatter(formatter)
        self._logger.addHandler(handler)

        self._sock = None 
        self._address = None

    def __call__(self, sock, address): 
        try :
            # 接続を受ける
            (self._sock, self._address) = (sock, address)
            with self:
                self.handle()
        except BrokenPipeError:
            #例外を雑に処理
            self._logger.debug("BrokenPipeError")
        except OSError:
            #例外を雑に処理
            self._logger.debug("OSError")

    def __enter__(self): 
        self._logger.debug("IPアドレス'" + str(self._address[0]) + "'とコネクションを接続しました。")

    def __exit__(self, exc_type, exc_value, traceback):
        self._logger.debug("IPアドレス'" + str(self._address[0]) + "'とコネクションを切断しました。")
        self._sock.shutdown(socket.SHUT_RDWR) 
        self._sock.close()

    def getState():
        return self._state
        
    def handle(self):
        raise NotImplementedError

# 文字列を送信するハンドラ
class EchoHandler(SocketStreamHandler): 
    def __init__(self, echo_string):
        self._echo_string = echo_string
        super().__init__()

    def handle(self):
        string_length = len(self._echo_string)
        string_index = 0
        send_number = 1
        send_index = 0

        while send_index < send_number * string_length:
            data = self._echo_string[string_index]
            self._sock.send(data.encode('utf-8'))              
            time.sleep(0.5)
            if string_index >= string_length - 1:
                string_index = 0
            else:
                string_index += 1
            send_index += 1

if __name__ == '__main__':
    argvs = sys.argv 
    argc = len(argvs)
    ipaddress = "0.0.0.0"
    port = 56789
    max_processes = 10
    echo_string = "Hello world\n"
    if (argc > 5):
        print("引数が多すぎます")
        quit()
    elif (argc == 5):
        ipaddress = argvs[1]
        pattern="((?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))"
        if not re.search(pattern,ipaddress):
            print("第一引数のIPアドレスはXXX.XXX.XXX.XXXの形式で入力してください")
            quit()
        try:
            port = int(argvs[2])
            max_processes = int(argvs[3])
            if (port < 1) or (max_processes < 1):
                print("第二引数、第三引数の数字は1以上で入力してください")
                quit()
            else:
                pass
        except ValueError:
            print("第二引数、第三引数は数字で入力してください")
            quit()
        echo_string = argvs[4]
    elif (argc == 1):
        pass
    else:
        print("引数が少なすぎます")
        quit()

    print("以下の通りででサーバを起動します")
    print("IPアドレス\t：{0}".format(ipaddress))
    print("ポート\t\t：{0}".format(port))
    print("最大プロセス数\t：{0}".format(max_processes))
    print("エコー文言\t：{0}".format(echo_string))


    server = MultiprocessingSocketStreamServer(ipaddress, port, max_processes) # 接続を処理するハンドラ
    handler = EchoHandler(echo_string)
    server.start(handler)

