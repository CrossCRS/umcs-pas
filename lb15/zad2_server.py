import select, socket, ssl
import queue

HOST = 'localhost'
PORT = 10000

OPENWEATHER_API_KEY = "d4af3e33095b8c43f1a6815954face64"
OPENWEATHER_LAT = "51.250559"
OPENWEATHER_LON = "22.5701022"

def get_weather():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.load_verify_locations(capath="/etc/ssl/certs")

    if ssl.HAS_SNI:
        secure_sock = context.wrap_socket(sock, server_hostname="api.openweathermap.org")
    else:
        secure_sock = context.wrap_socket(sock)

    secure_sock.connect(("api.openweathermap.org", 443))

    request = f"GET /data/2.5/weather?lat={OPENWEATHER_LAT}&lon={OPENWEATHER_LON}&appid={OPENWEATHER_API_KEY} HTTP/1.1\r\nHost: api.openweathermap.org\r\n\r\n"
    secure_sock.sendall(request.encode())

    response = secure_sock.recv(8192).decode()
    secure_sock.close()

    response = response.split("\r\n\r\n")[1]

    return response

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setblocking(0)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    inputs = [server_socket]
    outputs = []

    message_queues = {}

    while inputs:
        readable, writable, exceptional = select.select(inputs, outputs, inputs)

        for s in readable:
            if s is server_socket:
                client_socket, client_address = s.accept()
                client_socket.setblocking(0)
                inputs.append(client_socket)
                message_queues[client_socket] = queue.Queue()

            else:
                data = s.recv(4096)

                if data:
                    if data.decode() == "WEATHER\r\n":
                        weather = get_weather()
                        message_queues[s].put(weather.encode())
                    else:
                        message_queues[s].put("Invalid command".encode())

                    if s not in outputs:
                        outputs.append(s)
                else:
                    if s in outputs:
                        outputs.remove(s)
                    inputs.remove(s)
                    s.close()
                    del message_queues[s]

        for s in writable:
            try:
                next_msg = message_queues[s].get_nowait()
            except queue.Empty:
                outputs.remove(s)
            else:
                s.send(next_msg)

        for s in exceptional:
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            del message_queues[s]


if __name__ == "__main__":
    main()
