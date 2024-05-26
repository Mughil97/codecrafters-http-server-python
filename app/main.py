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
        message_parts = extract_http_message(data)

        if message_parts["url"] == "/":
            conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
            conn.close()
        if compile.match(message_parts["url"]):
            echo_message = message_parts["url"].split("/")[2]
            headers = f"Content-Type: text/plain\r\nContent-Length: {len(echo_message)}"
            response = f"HTTP/1.1 200 OK\r\n{headers}\r\n\r\n{echo_message}"
            conn.sendall(response.encode("utf-8"))
            conn.close()
        else:
            conn.sendall(b"HTTP/1.1 404 Not Found\r\n\r\n")


def extract_http_message(http_packet) -> dict:
    http_lines = http_packet.split("\r\n")
    start_line_items = http_lines[0].split(" ")
    return {
        "verb": start_line_items[0],
        "url": start_line_items[1],
        "version": start_line_items[2],
        "headers": http_lines[1],
        "body": http_lines[3],
    }


if __name__ == "__main__":
    main()
