# Uncomment this to pass the first stage
import re
import socket

compile = re.compile(r"\/echo\/([a-z0-9])+")


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    conn, _ = server_socket.accept()  # wait for client
    data = conn.recv(1024).decode("utf-8")
    with conn:
        message_parts = parse_http_message(data)

        if message_parts["url"] == "/":
            conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
            conn.close()
        if compile.match(message_parts["url"]):
            echo_message = message_parts["url"].split("/")[2]
            headers = f"Content-Type: text/plain\r\nContent-Length: {len(echo_message)}"
            response = f"HTTP/1.1 200 OK\r\n{headers}\r\n\r\n{echo_message}"
            conn.sendall(response.encode("utf-8"))
            conn.close()
        if message_parts["url"] == "/user-agent":
            message = message_parts["headers"]["User-Agent"]
            headers = f"Content-Type: text/plain\r\nContent-Length: {len(message)}"
            response = f"HTTP/1.1 200 OK\r\n{headers}\r\n\r\n{message}"
            conn.sendall(response.encode("utf-8"))
            conn.close()
        else:
            conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")


def parse_http_message(data) -> dict:
    message_parts = data.split("\r\n")

    return {
        "verb": message_parts[0].split(" ")[0],
        "url": message_parts[0].split(" ")[1],
        "http_version": message_parts[0].split(" ")[2],
        "headers": parse_http_headers(message_parts[1:-2]),
        "body": message_parts[-1],
    }


def parse_http_headers(header_part) -> dict:
    headers = {}
    for i in header_part:
        key_value = i.split(": ")
        headers[key_value[0]] = key_value[1]

    return headers


if __name__ == "__main__":
    main()
