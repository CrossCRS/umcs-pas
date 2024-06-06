import select, socket, Queue

if __name__ == "__main__":

    HOST = '127.0.0.1'
    PORT = 50000
    SERVER = (HOST, PORT)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setblocking(0)
    server_socket.bind(SERVER)
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
                message_queues[client_socket] = Queue.Queue()

            else:

                data = s.recv(1024)

                if data:
                    message_queues[s].put(data)
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
            except Queue.Empty:
                outputs.remove(s)
            else:
                s.send(next_msg)

        for s in exceptional:
            inputs.remove(s)
            if s in outputs:
                outputs.remove(s)
            s.close()
            del message_queues[s]
