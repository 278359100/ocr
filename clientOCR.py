import socket

def send_image_path(img_path, host='localhost', port=12345):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    client_socket.send(img_path.encode('utf-8'))

    response = client_socket.recv(1024).decode('utf-8')
    print(f"Server response: {response}")

    client_socket.close()

if __name__ == "__main__":
    image_paths = [
        r"pic\screenshot1.png",
        r"pic\screenshot2.png",
        r"pic\screenshot4.png",
        r"pic\5.png",
        r"pic\6.png"

    ]

    for img_path in image_paths:
        send_image_path(img_path)

