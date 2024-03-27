import socket
from timeit import default_timer as timer

# TCP Echo Time: 0.0004139790007684496
# UDP Echo Time: 0.00016513900027348427
#
# UDP jest szybsze ze względu na mniejszy overhead
# z powodu brak konieczności handshake'u i sprawdzania sum kontrolnych
#
# Zalety TCP:
#   - wiedza czy klient jest wciąż "podłączony"
#   - weryfikacja czy pakiety zostały dostarczone poprawnie
# Wady TCP:
#   - większy overhead w porównaniu do UDP

HOST = "127.0.0.1"
PORT_TCP = 2914
PORT_UDP = 2915

def main():
    start = timer()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT_TCP))

    sock.send(b"PING")
    sock.recv(1024)

    sock.close()
    end = timer()

    print("TCP Echo Time:", end - start)

    start = timer()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    sock.sendto(b"PING", (HOST, PORT_UDP))
    sock.recv(1024)

    sock.close()
    end = timer()

    print("UDP Echo Time:", end - start)

if __name__ == "__main__":
    main()
