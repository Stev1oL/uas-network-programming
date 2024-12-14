import socket
import threading
from collections import defaultdict
import time
import random

class DDosServer:
    def __init__(self, host="127.0.0.1", port=8080):
        self.host = host
        self.port = port
        self.request_count = defaultdict(int)
        self.banned_ips = set()
        self.challenge_ips = set()
        self.lock = threading.Lock()

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.settimeout(10)  # 10 detik timeout
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        print(f"Server running on {self.host}:{self.port}")

        while True:
            try:
                client_socket, client_address = server_socket.accept()
                threading.Thread(target=self.handle_client, args=(client_socket, client_address)).start()
            except socket.timeout:
                print("Socket timeout, waiting for new connections...")


    def handle_client(self, client_socket, client_address):
        ip, _ = client_address
        try:
            with self.lock:
                if ip in self.banned_ips:
                    client_socket.close()
                    return

            self.request_count[ip] += 1

            if self.request_count[ip] > 100:  # Threshold for banning IPs
                with self.lock:
                    self.banned_ips.add(ip)
                    print(f"IP {ip} banned for excessive requests")
                client_socket.close()
                return

            # if ip not in self.challenge_ips:
            #     self.send_challenge(client_socket, ip)
            #     return

            data = client_socket.recv(1024).decode()
            if data:
                print(f"Received from {ip}: {data}")
                client_socket.send(b"Request received")
        except (ConnectionResetError, socket.error) as e:
            print(f"Error: {e}")
        finally:
            client_socket.close()

    # def send_challenge(self, client_socket, ip):
    #     challenge = random.randint(1000, 9999)
    #     client_socket.send(f"Solve this challenge: {challenge} + 1 = ?".encode())
    #     response = client_socket.recv(1024).decode()

    #     if response.strip() == str(challenge + 1):
    #         with self.lock:
    #             self.challenge_ips.add(ip)
    #         client_socket.send(b"Challenge passed. Welcome!")
    #     else:
    #         client_socket.send(b"Challenge failed. Connection closed.")
    #     client_socket.close()

    def log_requests(self):
        while True:
            time.sleep(10)
            print("Current request counts:")
            with self.lock:
                for ip, count in self.request_count.items():
                    print(f"IP {ip}: {count} requests")
            self.visualize_logs()

    def visualize_logs(self):
        with self.lock:
            print("\n--- Log Visualization ---")
            for ip, count in sorted(self.request_count.items(), key=lambda x: x[1], reverse=True):
                print(f"{ip}: {'#' * (count // 5)} ({count})")

if __name__ == "__main__":
    server = DDosServer()
    threading.Thread(target=server.log_requests, daemon=True).start()
    server.start()
