import socket
import urllib.parse

HOST="httpbin.org"
PORT=80

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    sock.connect((HOST, PORT))

    data = ""

    customer_name = input("Name: ")
    customer_phone = input("Phone: ")
    customer_email = input("Email: ")
    size = input("Size (small|medium|large): ")
    delivery_time = input("Delivery time: ")
    comments = input("Comments: ")
    toppings = []
    topping = ""
    while True:
        topping = input("Topping (bacon|cheese|onion|mushroom|empty to stop): ")
        if topping:
            toppings.append(topping)
        else:
            break

    toppings = "&topping=".join(toppings)

    data = f"custname={customer_name}&custtel={customer_phone}&custemail={customer_email}&size={size}&topping={toppings}&delivery={delivery_time}&comments={comments}"
    data = urllib.parse.quote_plus(data)

    sock.send(f"POST /post HTTP/1.1\r\nHOST: {HOST}\r\nContent-Length: {len(data)}\r\nContent-Type: application/x-www-form-urlencoded\r\n\r\n{data}".encode())
    resp = b""

    try:
        while True:
            chunk = sock.recv(4096)
            if len(chunk) == 0:
                break
            resp += chunk
    except socket.timeout:
        pass

    print(resp.decode('utf-8', errors='ignore'))

    sock.close()

if __name__ == "__main__":
    main()
