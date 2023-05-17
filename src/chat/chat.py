import socket
from threading import Thread

class ChatClient:
    def __init__(self, host, port, name='익명'):
        # 연결할 서버의 IP, 포트 번호, 채팅 아이디
        self.host = host
        self.port = port
        self.name = name

        self.s = socket.socket()
        print(f"[*] {self.host}:{self.port} 로 연결시도")
        # 서버로 연결
        self.s.connect((self.host, self.port))
        print("[+] 연결 완료")

    def communication_with_server(self):
        while True:
            message = self.s.recv(1024).decode()
            print(message)

    def connect(self):
        t = Thread(target=self.communication_with_server, daemon = True)
        t.start()

        while True:
            # 서버로 보낼 채팅 입력받기
            message = input()
            message = f"{self.name}: {message}"
            # 채팅 보내기
            self.s.send(message.encode())

        self.s.close()

class ChatServer:
    def __init__(self, port):
        self.host = '0.0.0.0'
        self.port = port

        # 클라이언트 소켓을 저장할 리스트
        self.client_sockets = []

        self.s = socket.socket()
        # 재사용 가능한 주소로 설정
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # IP:PORT 주소를 소켓에 등록
        self.s.bind((self.host, self.port))
        # 통신을 대기하기
        self.s.listen()
        print(f"[*] {self.host}:{self.port} 주소에서 통신 대기중")

    def communication_with_client(self, cs):
        while True:
            try:
                # 클라이언트로부터 채팅 메시지 받기
                message = cs.recv(1024).decode()
            except Exception as e:
                print(f"[!] 에러발생: {e}")
                # 에러가 발생하면 클라이언트와 연결 끊어주기
                self.client_sockets.remove(cs)
                break
            else:
                # 모든 클라이언트들에게 채팅 뿌려주기
                for client_socket in self.client_sockets:
                    if cs != client_socket:
                        client_socket.send(message.encode())

    def serve(self):
        while True:
            client_socket, client_address = self.s.accept()
            print(f"[+] 연결완료: {client_address}")
            # 클라이언트 소켓 리스트에 연결된 클라이언트 소켓 저장
            self.client_sockets.append(client_socket)
            # 클라이언트와 통신할 스레드 생성
            t = Thread(target=self.communication_with_client, args=(client_socket,), daemon=True)
            t.start()

        # 클라이언트 소켓 종료하기
        for cs in self.client_sockets:
            cs.close()
        # 서버 소켓 종료하기
        self.s.close()