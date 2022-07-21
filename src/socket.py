import socket
from typing import Any, Optional


class UDPSocket:
    def __init__(self, addr: str, port: int) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.setblocking(False)
        self.sock.bind((addr, port))

    def readData(self) -> Optional[str]:
        try:
            data = self.sock.recv(1024)
            return data.decode()
        except BlockingIOError:
            return None

    def sendData(self, data: Any, addr: str, port: int) -> None:
        buf = str(data).encode()
        self.sock.sendto(buf, (addr, port))

    def parseCommand(self):
        data = self.readData()

        if not data:
            return "", None

        cmd, val = data.split(" ")
        return cmd, float(val)
