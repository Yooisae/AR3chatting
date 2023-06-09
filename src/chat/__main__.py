import sys
from chat import ChatServer, ChatClient

HELP_MESSAGE = """사용법:  __main__.py COMMAND

COMMANDs:
  serve       특정 포트로 채팅 서버를 엽니다. __main__.py serve [PORT] 로 실행하세요.
  connect     채팅 서버로 연결합니다. __main__.py connect [IP] [PORT] [NAME] 으로 실행하세요.
  help        이 메시지를 출력합니다.
"""

def main():
    if len(sys.argv) < 2:
        sys.stderr.write(HELP_MESSAGE)
        return

    if sys.argv[1] == 'serve':
        if len(sys.argv) == 3:
            port = int(sys.argv[2])
            server = ChatServer(port)
            server.serve()
        else:
            sys.stderr.write("사용법: __main__.py serve [PORT]\n")
    elif sys.argv[1] == 'connect':
        if len(sys.argv) == 4 or len(sys.argv) == 5:
            ip = sys.argv[2]
            port = int(sys.argv[3])
            # 채팅 아이디를 지정하지 않았을 경우
            if len(sys.argv) == 4:
                client = ChatClient(ip, port)
            # 채팅 아이디를 지정했을 경우
            else:
                name = sys.argv[4]
                client = ChatClient(ip, port, name)
            client.connect()
        else:
            sys.stderr.write("사용법: __main__.py connect [IP] [PORT] [NAME]\n")
    elif sys.argv[1] == 'help':
        sys.stderr.write(HELP_MESSAGE)
    else:
        sys.stderr.write("사용법: __main__.py [COMMAND]\n")
        sys.stderr.write("COMMANDs: serve, connect, help\n")

if __name__ == '__main__':
    main()