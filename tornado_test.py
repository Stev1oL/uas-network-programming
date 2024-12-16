import tornado.ioloop
import tornado.web
import tornado.httpclient
import time
import asyncio

def main_server():
    class MainHandler(tornado.web.RequestHandler):
        def get(self):
            self.write("Hello, Tornado Server is Running!")

    app = tornado.web.Application([
        (r"/", MainHandler),
    ])
    app.listen(8888)
    print("Server started on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()

async def simulate_load(target_url, requests_count):
    http_client = tornado.httpclient.AsyncHTTPClient()
    start_time = time.time()
    
    tasks = []
    for _ in range(requests_count):
        tasks.append(http_client.fetch(target_url))

    responses = await asyncio.gather(*tasks, return_exceptions=True)
    
    success = sum(1 for r in responses if isinstance(r, tornado.httpclient.HTTPResponse))
    failed = requests_count - success
    end_time = time.time()

    print(f"Total Requests: {requests_count}")
    print(f"Successful: {success}, Failed: {failed}")
    print(f"Total Time Taken: {end_time - start_time} seconds")

if __name__ == "__main__":
    import sys
    import threading

    if len(sys.argv) < 2:
        print("Usage: python tornado_test.py [server|load] [requests_count (optional)]")
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "server":
        main_server()

    elif mode == "load":
        if len(sys.argv) < 3:
            print("Please specify the number of requests to send.")
            sys.exit(1)
        
        requests_count = int(sys.argv[2])
        target_url = "http://localhost:8888/"
        
        asyncio.run(simulate_load(target_url, requests_count))

    else:
        print("Invalid mode. Use 'server' or 'load'.")
