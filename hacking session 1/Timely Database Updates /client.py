#!/usr/bin/env python3

import hashlib
import socket
import time

HOST = "cns-test.idlab.uantwerpen.be"
PORT = 50012
def md5(s):
    return hashlib.md5(s.encode()).hexdigest()

def recv_until(sock, marker):

    data = b""

    while marker.encode() not in data:

        chunk = sock.recv(1024)

        if not chunk:
            break

        data += chunk

    return data.decode()


def main():


    with socket.create_connection(
        (HOST, PORT)
    ) as sock:


        print(recv_until(
                sock,
                "required"
            ),
            end="\n")

        username = input("Username: ")
        password = input("Password: ")


        digest = hashlib.md5(
            (password + username).encode()
        ).hexdigest()

        sock.sendall(
            (digest + "\n").encode()
        )
        mark = time.time()
        data = recv_until(
            sock,
            "ctfdb=> "
        )
        
        print(f"Login took {(time.time()-mark)*1000} ms")
        print(data, end="")
        while True:


            if (
                "authentication failed" in data.lower()
                or "bye." in data.lower()
            ):
                return

            command = input()

            sock.sendall(
                (command + "\n").encode()
            )

            data = recv_until(
                sock,
                "ctfdb=> "
            )
            print(data, end="")


if __name__ == "__main__":
    main()
