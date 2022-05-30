import base64
import socket
import ssl
from configparser import ConfigParser
from client import Smtp

config = ConfigParser()
with open('config.cfg', 'r', encoding='utf-8') as f:
    config.read_file(f)
user_data = config['UserData']
connection_data = config['Connection']
message = config['Message']
HOST_ADDR = connection_data['SmtpAddress']
PORT = connection_data.getint('Port')
TIMEOUT = connection_data.getint('Timeout')

b64_mail = base64.b64encode(user_data['Mail'].encode()).decode()
b64_password = base64.b64encode(user_data['Password'].encode()).decode()


def _send(sock: socket.socket, data: str) -> str:
    sock.send(f'{data}\n'.encode())
    return sock.recv(65535).decode()


def _get_message():
    smtp = Smtp(user_data['Mail'])
    for attachment in filter(lambda x: len(x.strip()) > 0,
                             message['Attachments'].split(', ')):
        smtp.attach(attachment)
    text = ''
    with open(message['MessageFile'], 'r', encoding='utf-8') as msg_f:
        text = msg_f.read()
    return smtp.get_smtp_data(message['Title'], text, message['Mail'])


def log(str):
    pass


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST_ADDR, PORT))
        sock = ssl.wrap_socket(sock)
        sock.settimeout(TIMEOUT / 1000)
        log(sock.recv(1024).decode())
        log(_send(sock, f'ehlo {user_data["Mail"]}'))
        log(_send(sock, 'AUTH LOGIN'))
        log(_send(sock, b64_mail))
        log(_send(sock, b64_password))
        log(_send(sock, f'MAIL FROM: {user_data["Mail"]}'))
        for r in message["Mail"].split(';'):
            log(_send(sock, f'RCPT TO: {r}'))
        log(_send(sock, f'DATA'))
        log(_send(sock, _get_message()))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(e)
