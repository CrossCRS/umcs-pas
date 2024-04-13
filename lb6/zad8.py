import socket

HOST="dsmka.wintertoad.xyz"
PORT=587

LOGIN="dGVzdDFAd2ludGVydG9hZC54eXo="
PASS="UEBzc3cwcmQ="

FILE="/9j/4AAQSkZJRgABAQEBLAEsAAD//gATQ3JlYXRlZCB3aXRoIEdJTVD/4gKwSUNDX1BST0ZJTEUAAQEAAAKgbGNtcwRAAABtbnRyUkdCIFhZWiAH5wAFABAACgArAANhY3NwQVBQTAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA9tYAAQAAAADTLWxjbXMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA1kZXNjAAABIAAAAEBjcHJ0AAABYAAAADZ3dHB0AAABmAAAABRjaGFkAAABrAAAACxyWFlaAAAB2AAAABRiWFlaAAAB7AAAABRnWFlaAAACAAAAABRyVFJDAAACFAAAACBnVFJDAAACFAAAACBiVFJDAAACFAAAACBjaHJtAAACNAAAACRkbW5kAAACWAAAACRkbWRkAAACfAAAACRtbHVjAAAAAAAAAAEAAAAMZW5VUwAAACQAAAAcAEcASQBNAFAAIABiAHUAaQBsAHQALQBpAG4AIABzAFIARwBCbWx1YwAAAAAAAAABAAAADGVuVVMAAAAaAAAAHABQAHUAYgBsAGkAYwAgAEQAbwBtAGEAaQBuAABYWVogAAAAAAAA9tYAAQAAAADTLXNmMzIAAAAAAAEMQgAABd7///MlAAAHkwAA/ZD///uh///9ogAAA9wAAMBuWFlaIAAAAAAAAG+gAAA49QAAA5BYWVogAAAAAAAAJJ8AAA+EAAC2xFhZWiAAAAAAAABilwAAt4cAABjZcGFyYQAAAAAAAwAAAAJmZgAA8qcAAA1ZAAAT0AAACltjaHJtAAAAAAADAAAAAKPXAABUfAAATM0AAJmaAAAmZwAAD1xtbHVjAAAAAAAAAAEAAAAMZW5VUwAAAAgAAAAcAEcASQBNAFBtbHVjAAAAAAAAAAEAAAAMZW5VUwAAAAgAAAAcAHMAUgBHAEL/2wBDAAMCAgMCAgMDAwMEAwMEBQgFBQQEBQoHBwYIDAoMDAsKCwsNDhIQDQ4RDgsLEBYQERMUFRUVDA8XGBYUGBIUFRT/2wBDAQMEBAUEBQkFBQkUDQsNFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBT/wgARCACAAIADAREAAhEBAxEB/8QAGgABAAMBAQEAAAAAAAAAAAAAAAUGBwQCA//EABQBAQAAAAAAAAAAAAAAAAAAAAD/2gAMAwEAAhADEAAAAd8AAAAAAAAAAAAAAAAAAPBXiJBLFhPYAAABzGekeACQNCOkAAAGeEOAACYNDAAAOIzEAAAGnHaAACFM+AAABoJNAAAjDNwAAAaQSYAABmJxAAA7TTgAAAVYpoAALMXUAAAgSiHkAAAtBcwADiM0PAAAABeiwgAoxXQAAAAdZqAAMqPiAAAAAaUSIPBk4AAAAANBJoAyQAAAAAGiEuf/xAAiEAABBAICAgMBAAAAAAAAAAAEAQIDBSAwExQAEhARNFD/2gAIAQEAAQUC/iuejGzXcTPFu51RLudEhu4n+Nej26Z52DRlmyFvwENkEfBOwmPRZl9kjKsL6xGZk3XF0BzdgXK3VUB0VCqoOVkxZAdFaxYwczB1FIyDHUojRdSQuZlUmQwaLKyQVFVXLnWWfHkYQgo73K92mnL5ocLqf3I1CT9YjCZ/LLrr38gXw93o3ZUO+wd9V+Dz/8QAFBEBAAAAAAAAAAAAAAAAAAAAgP/aAAgBAwEBPwEAf//EABQRAQAAAAAAAAAAAAAAAAAAAID/2gAIAQIBAT8BAH//xAAwEAABAgQDBQUJAAAAAAAAAAABAhEDITBBACAxECNRYXESIjNCoRMyQFBSgZGxsv/aAAgBAQAGPwL5K6iEjicbtJiegxogc2xog82xvEmH6jDpIUOIpFayww6iybIsMrpLpuixwFoLiiw8NEk52PhrkqhEXcCVGGu5E862D6PyoocNq3PPFA4PRhA8HoKRa3TOlFr9KIQTvk6AZ1IX3FK850NDsInF/nDmZoCDGPd8quGZS7264KjMmZpezV7yNOmUQ/opoiatlWtm7RdqkEs0m/G0liWsKqJEM/wEL7/vZ//EACkQAQABAgUCBQUBAAAAAAAAAAERMUEAICEwYVGhcYGxwfAQQJHR8VD/2gAIAQEAAT8h/wAVsc1SAwtC81f7dsPQclCk74Oi4KlL3wtC81P7dsFnmiSO1GWbXXoYRIl0H4POUEiXUfg84nLNrj0dlmQUYL9XOxICElujsMHJqAUXQ77LJy6glU0e+cihKFNE19Dz2SKEIU0TX1PLPCIJV4Z9tmERWjyz77CjmDLb2ZxHMmWWu2WgrTaDWfk0zlyEGpPQOK+uwhcU8uXjxhyijKtXY8AFe149PTKo4gQW9mFdlqdXaRmIwsm38frLF5oa9Vh/W3oPB6nFHLdQeKXct6e29vrQclhlfDdi2oiUrrOn5+w+Zy+n/9oADAMBAAIAAwAAABAAAAAAAAAAAAAAAAAAACAQAAAACCSQQAAACSSSQAAASSSSSAAASSSSSAAASSSSSAAAASSSAAAAASSSQAAAQSSSQAACCSSSSQACSSSSSQAASSSSSQACSSSSSSACSSSSSSD/xAAUEQEAAAAAAAAAAAAAAAAAAACA/9oACAEDAQE/EAB//8QAFBEBAAAAAAAAAAAAAAAAAAAAgP/aAAgBAgEBPxAAf//EACQQAQEAAgEEAgEFAAAAAAAAAAERIUFRIDAxYQCB0RBAUKGx/9oACAEBAAE/EP4WW149DCrjynx0QDNQlUUaHERvPK7cBXOSsp7E+DtwNc5YSvoD4aYFmgSioFLiC1ni2148DGJjyPa8fkgzpBtfysBfmZwzcCxm8m+WdEDos4Zbgys1gTyxso+PyVY2g0n4SiPZdWpAyxnFopjUDFvW6tSBlnOpAXOouLOwoaUCVQscQQvrnsqGFAhUrDEQp6468Mj5GC4byQPbXZwyPk5LhrLB9t9aLAUvEJ/cU99lFkIXiMfuC++wCS5hWVYV0zFHjrBIcQrKsY6Lipz2RoMopJ6YgM2rwvWWC4pQKQDEyrTKUgdjIGc+QdjfD7OIKD3L1HKrt7HrzZ+jf0f8dRElzCsCUptmYPHzD/UQo1YY8vaUumAKEwuWIs8Pkr04sc9GRpvxDUzfXbpmq1VjDJmLM+Z0+23lyGXcvc1gMW2m/vL7/X0PdjLBtdHd4Ljoz1yPC8ia/Zb/AP/Z"

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    sock.recv(1024)
    sock.send(b"EHLO test1\r\n")
    sock.recv(1024)
    sock.send(b"AUTH LOGIN\r\n")
    sock.recv(1024)
    sock.send((LOGIN + "\r\n").encode())
    sock.recv(1024)
    sock.send((PASS + "\r\n").encode())
    resp = sock.recv(1024)

    print(resp)

    if resp.decode() == "235 2.7.0 Authentication successful\r\n":
        print("Logged in")

        subject = input("Subject: ")
        recipients = []

        recp = "."
        while recp != "":
            recp = input("Recipient (empty to end adding): ")
            if recp != "":
                recipients.append(recp)

        email_from = input("From: ")
        email_body = input("Body: ")

        sock.send(b"MAIL FROM: <" + email_from.encode() + b">\r\n")
        sock.recv(1024)
        for recp in recipients:
            sock.send(b"RCPT TO: <" + recp.encode() + b">\r\n")
            sock.recv(1024)

        sock.send(b"DATA\r\n")
        sock.recv(1024)
        sock.send(b"Subject: " + subject.encode() + b"\r\n")
        sock.send(b"From: " + email_from.encode() + b">\r\n")
        sock.send(b"To: <" + recipients[0].encode() + b">\r\n")
        if len(recipients) > 1:
            sock.send(b"CC: <" + ",".join(recipients[1:]).encode() + b">\r\n")

        sock.send(b"MIME-Version: 1.0\r\n")
        sock.send(b"Content-Type: multipart/mixed; boundary=sep\r\n")
        sock.send(b"--sep\r\n")
        sock.send(email_body.encode())
        sock.send(b"--sep\r\n")
        sock.send(b"Content-Type: image/jpeg; name=\"plik.jpg\"\r\n")
        sock.send(b"Content-Disposition: attachment; filename=\"plik.jpg\"\r\n")
        sock.send(b"Content-Transfer-Encoding: base64\r\n")
        sock.send(FILE.encode() + b"\r\n")
        sock.send(b"--sep--\r\n")

        sock.send(b"\r\n.\r\n")
        print(sock.recv(1024))
    else:
        print("Login failed")

    sock.close()

if __name__ == "__main__":
    main()
